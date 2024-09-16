import time

from utils import download_and_save_image_file


def generate_image_dall_e(prompt, project_name):
    from openai_gpt import generate_image_dalle
    start_time = time.time()
    response = generate_image_dalle(prompt)

    # Read the last number in the files and save an image with a next number in the sequence
    time_elapsed = time.time() - start_time
    print(f"Image generated in {time_elapsed:.2f} seconds")
    download_and_save_image_file(response.data[0].url, prompt, project_name)
