import argparse
import json
import os
from shutil import copyfile

from dotenv import load_dotenv

from audio import get_large_audio_transcription_on_silence, audio_to_text, increment_file
from utils import zip_folder
from utils import (split_text_limit_tokens, check_text_exists, read_txt_file, check_audio_files_exists,
                   get_chunks_audio, translate_text, save_text, split_text_limit_characters, read_and_parse,
                   merge_and_format, count_gpt_without_image, process_text_chunk)

load_dotenv(".env")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
ORGANIZATION_ID = os.getenv("ORGANIZATION_ID")

# Audio related variables
MAX_TOKENS_SPLIT_TO_LLM = os.getenv("MAX_TOKENS_SPLIT_TO_LLM", 512)
MIN_SILENCE_LEN = os.getenv("MIN_SILENCE_LEN", 500)
KEEP_SILENCE = os.getenv("KEEP_SILENCE", 500)
CHUNK_LENGTH_MS = os.getenv("CHUNK_LENGTH_MS", 60000)

USE_DALLE = True if os.getenv("USE_DALLE", False) in ["1", "True", "TRUE"] else False
OPENAI_DALLE_MODEL = os.getenv("OPENAI_DALLE_MODEL", "dall-e-2")
OPENAI_DALLE_RESOLUTION = os.getenv("OPENAI_DALLE_RESOLUTION", "1024x1024")


def main(args):
    # Check if the text.txt file exists, the RAW text.
    if not check_text_exists(args.n):
        print("Text file not found, checking audio chunk folder...")
        if not check_audio_files_exists(args.n):
            print("Audio chunks not found, splitting audio file...")
            audio_chunks = get_large_audio_transcription_on_silence(file=args.f,
                                                                    project_name=args.n,
                                                                    min_silence_len=MIN_SILENCE_LEN,
                                                                    keep_silence=KEEP_SILENCE,
                                                                    chunk_length_ms=CHUNK_LENGTH_MS)
        else:
            print("Audio chunks found, using them...")
            audio_chunks = get_chunks_audio(args.n)

        full_raw_text = audio_to_text(args.n, audio_chunks, args.lang)
        print(f"Full raw text with {len(full_raw_text)} characters")

        if args.lang != "en-US":
            print(f"Translation in progress...")
            save_text(full_raw_text, args.n, "original-lang-text.txt")  # Copy the original final before translate

            # Validate if full_raw_text has more than 5000 characters, if so, split it
            if len(full_raw_text) > 5000:
                full_raw_text = split_text_limit_characters(full_raw_text, split_limit=4900)
                raw_text_list = []
                for i, text in enumerate(full_raw_text):
                    print(f"Translating text chunk [{i+1}/{len(full_raw_text)}]")
                    raw_text_list.append(translate_text(text, args.lang))
                full_raw_text = " ".join(raw_text_list)
            else:
                full_raw_text = translate_text(full_raw_text, args.lang)

            save_text(full_raw_text, args.n, "text.txt")  # Save again the file with the new translation
    else:
        print("GPT Text file found, using it...")
        full_raw_text = read_txt_file(args.n)

    if full_raw_text == "":
        print(f"The text file {args.n}/gpt.txt is empty, please check the audio file or the text file")
        return

    # Now check if the GPT file exists, the GPT file is the text that will be used to generate the images
    if not check_text_exists(args.n, file_name="gpt.txt"):
        text_chunks = split_text_limit_tokens(full_raw_text, split_limit=MAX_TOKENS_SPLIT_TO_LLM)

        print(f"Preparing {len(text_chunks)} text chunks for image generation...")

        for i, text_chunk in enumerate(text_chunks):
            print(f"Improving text with OpenAI [{i + 1}/{len(text_chunks)}]")
            attempt = 0
            attempt_limit = 3
            response = None

            while attempt < attempt_limit and response is None:
                attempt += 1
                try:
                    response = process_text_chunk(text_chunk, args.s, args.t)
                except Exception as e:
                    print(f"Attempt {attempt}. Error: {e}")

            if response:
                increment_file(args.n, response, "gpt.txt")
            else:
                print(f"Failed to process text chunk after {attempt_limit} attempts: \n{text_chunk}")

        #Generate a compiled json file with the gpt.txt and the text.txt
        print("Generating a compiled json file with the gpt.txt and the text.txt")

    if not check_text_exists(args.n, file_name="compiled.json"):
        # load the gpt.txt
        gpt_data = read_and_parse(args.n,'gpt.txt')
        text_data = read_and_parse(args.n,'text.txt')

        merged_data = merge_and_format(gpt_data, text_data)

        json_output = json.dumps(merged_data, indent=4)
        save_text(json_output, args.n, "compiled.json")


    # Load the results from the txt
    if not USE_DALLE:
        print("Using stable diffusion")
        from image_stable_diffusion import generate_image
    else:
        print("Using Dall-e")
        from image_dall_e import generate_image_dall_e as generate_image

    images_prompt = json.loads(read_txt_file(args.n, file_name="compiled.json"))
    image_pending = count_gpt_without_image(images_prompt)
    image_generated = 0
    for i, item in enumerate(images_prompt):
        if item['data']['gpt'] != "" and item['data'].get('image_file', "") == "":
            image_prompt = f"In '{args.s}' style, {item['data']['gpt']}"
            print(f"[{image_generated+1}/{image_pending}] Generating image for: {image_prompt}")
            image_generated += 1

            file_name = generate_image(image_prompt, args.n)
            item["data"]["image_file"] = file_name.replace("output/", "")  # remove the output from file path
            save_text(json.dumps(images_prompt, indent=4), args.n, "compiled.json")

    # copy the original audio to the output folder
    from utils import output_folder
    output_folder = f"{output_folder}/{args.n}"
    copyfile(args.f, f"{output_folder}/original_audio.mp3")

    zip_folder(args.n)

    print("Done!")

    # Clean up the audio chunks
    #clean_up_audio_chunks(args.n)


# create a __init__ function
if __name__ == "__main__":
    # Receive parameters from terminal
    parser = argparse.ArgumentParser(description='Extract text from audio file and generate images')
    parser.add_argument('-f', type=str, help='Audio file path')
    parser.add_argument('-s', type=str, help='Initial prompt to define style for the image generation', default="")
    parser.add_argument('-t', type=str, help='Theme, e.g. Dungeons and dragons, politics, humor', default="")
    parser.add_argument('-n', type=str, help='Project name (Used to create a output folder)', default="")
    parser.add_argument('-lang', type=str, help='Translation option. The recognition language is '
                                                'determined by ``language``, an RFC5646 language'
                                                ' tag like ``"en-US"``', default="en-US")

    args = parser.parse_args()
    main(args)
