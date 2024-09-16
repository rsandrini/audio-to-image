import os
import torch
from diffusers import DiffusionPipeline
from utils import save_image_file

pipe = DiffusionPipeline.from_pretrained(os.getenv("MODEL"),
                                         torch_dtype=torch.float16,
                                         use_safetensors=os.getenv("USE_SAFETENSORS", False))
pipe.to(os.getenv("PIPE_TO"))


def generate_image(prompt, project_name):
    image = pipe(prompt=prompt).images[0]

    # Read the last number in the files and save an image with a next number in the sequence
    return save_image_file(image, prompt, project_name)
