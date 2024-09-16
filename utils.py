import glob
import json
import os
import re
import shutil

import requests
import tiktoken
from PIL.PngImagePlugin import PngInfo
from deep_translator import GoogleTranslator



output_folder = "output"
output_final_folder = "output-final"
audio_chunks_folder = "audio-chunks"


def process_text_into_ai(text):
    pass


def save_image_file(image, prompt, project_name):
    folder = f"{output_folder}/{project_name}/images"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder):
        os.mkdir(folder)

    files = glob.glob(f"{folder}/*.png")
    files.sort(key=os.path.getmtime)
    last_file = files[-1] if len(files) else f"{folder}/000000.png"

    # Extract only the number from the files, not in the folder name
    last_number = int(re.findall(r"\d+", last_file.split("/")[-1])[0])
    next_number = last_number + 1
    file_name = f"{folder}/{next_number:06d}.png"
    print(f"Saving image to: {file_name}")

    metadata = PngInfo()
    metadata.add_text("Description", prompt)
    image.save(file_name, pnginfo=metadata)
    return file_name


def download_and_save_image_file(image_url, prompt, project_name):
    folder = f"{output_folder}/{project_name}"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder):
        os.mkdir(folder)

    files = glob.glob(f"{folder}/*.png")
    files.sort(key=os.path.getmtime)
    last_file = files[-1] if len(files) else f"{folder}/000000.png"

    # Extract only the number from the files, not in the folder name
    last_number = int(re.findall(r"\d+", last_file.split("/")[-1])[0])
    next_number = last_number + 1
    file_name = f"{folder}/{next_number:06d}.png"
    print(f"Saving image to: {file_name}")

    # metadata = PngInfo()
    # metadata.add_text("Description", prompt)

    response = requests.get(image_url)
    with open(file_name, "wb") as f:
        f.write(response.content)

    # image.save(file_name, pnginfo=metadata)


def clean_up_audio_chunks(project_name):
    folder_name = f"{audio_chunks_folder}/{project_name}"
    # create a directory to store the audio chunks
    if os.path.isdir(folder_name):
        shutil.rmtree(folder_name)


def check_folder(project_name):
    # create a directory to store the audio chunks
    if not os.path.isdir(audio_chunks_folder):
        os.mkdir(audio_chunks_folder)

    folder_name = f"{audio_chunks_folder}/{project_name}"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    return folder_name


def count_tokens(response):
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(enc.encode(response))


def split_text_at_period(text, word_limit):
    words = text.split()
    segments = []
    current_count = 0
    last_period_index = 0
    start_index = 0

    for i, word in enumerate(words):
        current_count += 1
        if word.endswith('.'):
            last_period_index = i
        if current_count >= word_limit:
            if last_period_index == 0 or last_period_index == start_index:
                # No period found within the word limit, split at the word limit.
                segments.append(' '.join(words[start_index:i]))
                start_index = i
            else:
                # Split at the last period found within the word limit.
                segments.append(' '.join(words[start_index:last_period_index + 1]))
                start_index = last_period_index + 1
            current_count = 0

    # Add the last segment if there is any remaining text
    if start_index < len(words):
        segments.append(' '.join(words[start_index:]))

    return segments


def split_text_limit_tokens(text, split_limit=1000):
    # if the text is greater than 4000 tokens, split it in two or more
    tks = count_tokens(text)

    if tks > int(split_limit):
        return split_text_at_period(text, int(int(split_limit) * 0.8))
    return [text]


def split_text_limit_characters(text, split_limit=1000):
    # split the text in chunks of 1000 characters and return a list of chunks
    if len(text) > int(split_limit):
        return [text[i:i + int(split_limit)] for i in range(0, len(text), int(split_limit))]


def save_text(text, project_name, file_name="text.txt"):
    # create a directory to store the audio chunks
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    folder = f"{output_folder}/{project_name}"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder):
        os.mkdir(folder)

    file = f"{folder}/{file_name}"
    print(f"Saving text to: {file}")

    with open(file, "w") as f:
        f.write(text)


def check_text_exists(project_name, file_name="text.txt"):
    file = f"{output_folder}/{project_name}/{file_name}"

    return os.path.isfile(file)


def check_audio_files_exists(project_name):
    # check if the audio chunks exists, count the existent files
    folder_name = f"{audio_chunks_folder}/{project_name}"
    return os.path.isdir(folder_name) and len(os.listdir(folder_name)) > 0


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def natural_keys(text):
    """
    A helper function to turn a string into a list of text and number chunks.
    E.g. "chunk_0_120.0.wav" -> ["chunk_", 0, "_", 120.0, ".wav"]
    """
    return [int(c) if c.isdigit() else c for c in re.split('(\d+)', text)]


def get_chunks_audio(project_name):
    folder_name = f"{audio_chunks_folder}/{project_name}"
    files = os.listdir(folder_name)
    files.sort(key=natural_keys)

    result = []
    for file in files:
        # Extract the start time from the filename
        parts = file.split('_')
        if len(parts) >= 3:
            try:
                start_time = float(f"{parts[2].split('.')[0]}.{parts[2].split('.')[1]}") # Extracts the start time (e.g. "120.32" from "chunk_0_120.32.wav")
                result.append([start_time, f"{folder_name}/{file}"])
            except ValueError:
                try:
                    start_time = float(
                        f"{parts[2].split('.')[0]}")  # Extracts the start time (e.g. "120" from "chunk_0_120.wav")
                    result.append([start_time, f"{folder_name}/{file}"])
                except ValueError:
                    # Handle the case where the conversion to float fails
                    print(f"Warning: Could not extract start time from '{file}'")
                    continue
    return result


def read_txt_file(project_name, file_name="text.txt"):
    file = f"{output_folder}/{project_name}/{file_name}"

    if not os.path.isfile(file):
        return ""

    with open(file, "r") as f:
        return f.read()


def increment_file_text(project_name, content, file_name="gpt.txt"):
    file = f"{output_folder}/{project_name}/{file_name}"

    # increment the file or create if it does not exist
    with open(file, "a+") as f:
        f.write(content + "\n")


def get_prompt(theme, style_prompt):
    return ('''Imagine a service that transforms user-provided image descriptions into coherent, detailed prompts for a text-to-image AI model. Your role is to summarize and refine descriptions into clear, concise prompts, focusing on the scene, mood, key elements, and interactions. Break into several parts considering the context and situations, and remove any not useful information for the image generations. Use always the '{style_prompt}' style and keep in mind the '{theme}' theme. Special attention should be paid to the details that enhance the image's quality, adjusting any unclear or unsatisfactory elements. Limit each prompt to a maximum of 70 tokens. Generate the maximum of prompts using the context passed.  
The result should be a JSON list. example: [{\"index\":0, \"image_prompt\": \"<text>\", "secs": 123}, {\"index\":1, \"image_prompt\": \"<text>\", "secs": 234}, ...], Try to not exceed 70 tokens in each image_prompt result. Don't return any additional information, just the image_prompt.
The original text contains some seconds from the original audio, try to return in the response the closest number of seconds to the phrases used to generate the prompt. 
e.g: 
```
0.0:Hi you're on the hipsters out of control podcast. 240.0: Finally, focus on just one thing, artificial intelligence and its applications. 1440.0: Hello hipsters welcome and welcome to Pinocchio's latest spin-off episode of your favorite podcast.1680.0: This is the out-of-control hipster where we explore different forms of tools and studies and what's next. 1920.0: From the world of AI that we have seen with interviews too. 
```
example of response:
[{\"index\":0, \"image_prompt\": \"A podcast focus on artificial intelligence and its applications.\", "secs": 0.0}, {\"index\":1, \"image_prompt\": \"Discuss the impact of AI in everyday life.Interview with Fabrício Carraro, a multilingual traveler discussing AI.\", "secs": 1680.0}, ...]''')


def translate_text(original_text, original_language='auto'):
    return GoogleTranslator(source=original_language, target='en').translate(original_text)


def read_and_parse(project_name, file_name):
    file = f"{output_folder}/{project_name}/{file_name}"
    with open(file, 'r') as f:

        return [(float(line.split(':')[0].strip().replace(" ", "")), line.split(':', 1)[1].strip()) for line in f.readlines()]


def merge_and_format(gpt_data, text_data):
    merged_data = []
    i, j = 0, 0
    while i < len(gpt_data) and j < len(text_data):
        if gpt_data[i][0] == text_data[j][0]:
            merged_data.append({"secs": gpt_data[i][0], "data": {"text": text_data[j][1], "gpt": gpt_data[i][1]}})
            i += 1
            j += 1
        elif gpt_data[i][0] < text_data[j][0]:
            merged_data.append({"secs": gpt_data[i][0], "data": {"text": "", "gpt": gpt_data[i][1]}})
            i += 1
        else:
            merged_data.append({"secs": text_data[j][0], "data": {"text": text_data[j][1], "gpt": ""}})
            j += 1

    while i < len(gpt_data):
        merged_data.append({"secs": gpt_data[i][0], "data": {"text": "", "gpt": gpt_data[i][1]}})
        i += 1

    while j < len(text_data):
        merged_data.append({"secs": text_data[j][0], "data": {"text": text_data[j][1], "gpt": ""}})
        j += 1

    return merged_data

def count_gpt_without_image(json_data):
    count = 0
    for entry in json_data:
        if 'gpt' in entry['data'] and entry['data']['gpt'] and 'image_file' not in entry['data']:
            count += 1
    return count


def split_long_lines(text):
    # Split the text into lines
    lines = text.strip().split('\n')

    # List to hold the processed lines
    processed_lines = []

    for i in range(len(lines)):
        # Split each line into time and text
        time, line_text = lines[i].split(':', 1)
        time = float(time)
        words = line_text.split()

        # Check if the line has more than 20 words
        if len(words) > 20:
            # Calculate time for the next line
            next_time = float(lines[i + 1].split(':')[0]) if i + 1 < len(lines) else time + 10  # default 10 seconds if it's the last line

            # Calculate time interval per word
            time_interval = (next_time - time) / len(words)

            # Split the line into smaller parts
            for j in range(0, len(words), 20):
                part = ' '.join(words[j:j + 20])
                part_time = time + j * time_interval
                processed_lines.append(f"{part_time:.3f}:{part}")
        else:
            processed_lines.append(f"{time:.3f}:{line_text}")

    return '\n'.join(processed_lines)


def process_text_chunk(text, session_id, timeout):
    from openai_gpt import prepare_text_for_image_generation
    try:
        response = json.loads(prepare_text_for_image_generation(text, session_id, timeout))
        return response
    except Exception as e:
        raise Exception(f"Failed to process text: {e}")


def zip_folder(project_name):

    if not os.path.isdir(output_final_folder):
        os.mkdir(output_final_folder)

    # zip the output folder
    zip_file = shutil.make_archive(project_name, 'zip', output_folder, base_dir=project_name)

    #move the zip file to output_final_folder
    shutil.move(zip_file, output_final_folder)

    print(f"Zipped the output folder to {output_final_folder}.zip")
