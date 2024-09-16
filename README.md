# About

Welcome to the cutting edge of AI innovation! 
This tool extracts text from spoken words and then uses that text to create images. 

audio -> audio chunks -> raw text -> image prompt -> image
   

The amount of images generated will be defined by the LLM model, after refine, summarize and split the text into sentences, considering the limit of 77 tokens per prompt.
All images contain the text used to generate them, and the text is also saved in a text file.


# Visualization of the process

Consider the following podcast file:

https://www.audacy.com/podcast/radio-headspace-6413e/episodes/mastering-mindfulness-transforming-time-perception-3a6f2

https://dcs.megaphone.fm/ADL5229004335.mp3

<audio controls="controls">
  <source type="audio/mov" src="readme-content/ADL5229004335.mov"></source>
  <p>Your browser does not support the audio element.</p>
</audio>

In the step one, the following audio will be break in a few chunks, and each audio chunks.

![audio-chunks.png](readme-content%2Faudio-chunks.png)

From those audio chunks, the following text will be extracted:

```
Hi everyone is kaesong. Just a reminder that you can listen to all of our. 
Headspace studios. Hi friends it's rosie here welcome to radiohead space and to monday. 
As a seasoned mindfulness teacher i've noticed how being present can change our perception of time and create a sense 
of spaciousness in our daily lives. Time was perpetually slipping through my fingers. 
And each day felt like a chaotic blur of events sound familiar. 
This was when i was an executive assistant with a full plate of tasks to further 
someone else's career and vision. I felt rushed hurried. And overwhelmed. 
A turning point arrived when i was gasping for some rest i missed my ceaseless whirlwind of responsibilities. 
Luckily i was also aware of the importance of reshaping my perception of time through mindfulness i developed tools to slow down 
during the day and take stock of what i was feeling so on that note today will dive into the transformative journey of 
mindfulness and how it has the power to alter our perception of time and will uncover how dwelling in the present moment can make us. 
Feel like we have abundant time even amidst the busiest days. 
To illustrate this let me share a story of my mindfulness student danny. Danny was a corporate worker always on the go juggling many resp. 
Abilities at work and home. He always felt short on time leading to chronic stress and fatigue. After introducing mindfulness into his life he began to experience a shift. 
His perception of time altered dramatically he became more present in each task leading to increased efficiency and a newfound sense 
of spaciousness in his day he did this by hiding his clock on his computer he had a ton of alarms to take breaks to do errands to go to bed 
so he did a sort of alarm detox only keeping the ones that were absolutely necessary we also changed the language around time for him. 
Instead of saying i have no time he said time moves at the pace it moves danny also began to understand the profound truth that time is indeed a construct just think about what it's like to watch the clock. 
Waiting for the hour to pass and time seems to stand still or those moments when you're so engrossed in an engaging conversation with friends or immersed in a thrilling project and ours just seemed to fly by.
Revealing our innate capacity to influence our perception of time. Does flexibility is not just a trick our minds play on us rather. 
It shows us that we can be present no matter what our day brings. For instance. 
Danny started to see that the same 24 hour day could feel very different based on his mindfulness and presence. He still had the same amount of hours. 
What is perception of those hours and how he could utilize them had transformed. With all this said. How can you bring more mindfulness. Your life and alter your perception of time. 
Here are some reflections and practices. First take one moment at a time. Make it a habit to bring your attention back to the present moment whenever you find your mind worrying about the future or dwelling on the past. 
And this can be as simple as noticing your wandering thoughts then guiding them back to the present moment. What you see in front of you what you hear.
Whatever your senses provide as an anchor to what's going on right now you can also do mindfulness activities. Incorporate mindful practices in your daily routine like mindful eating or walking. 
These activities bring awareness to the present moment and slower perception of time. And finally pause and breathe. Take short pauses throughout your day to focus on your breath. 
This can provide a sense of grounding and remind you to slow down. It's that simple. Remember. Mindfulness isn't an overnight transformation but a lifelong journey. 
A journey that allows us to perceive time differently and live in the present moment. Thus giving us a sense of having more than enough time. 
And if you're looking for more guidance. Check out the time for me meditation in the. With my dear friend eve. 
Thank you all for joining me today and i look forward to embarking on this mindfulness journey with you in our next episode. 
Until then. Take good care. 
```

This completes the seconds step, now we have the raw text, and we'll summarize, refine and split the text into sentences, considering the limit of 77 tokens per prompt.

After call the LLM model, the following text will be generated:

```
A person sitting at a desk, engrossed in work with a hidden clock on the computer.
A person embracing mindfulness, taking a break from work and feeling a sense of spaciousness in their day.
A person experiencing an altered perception of time through mindfulness, seeing time as a fluid construct.
A person sitting in a peaceful room, focusing on the present moment.
A person practicing mindful eating, savoring each bite they take.
A person taking a mindful walk, fully aware of their surroundings.
A person pausing in their busy day to take a deep breath and find a moment of calm.
```

And finally, the following images will be generated:

![000001.png](readme-content%2F000001.png)

A person sitting at a desk, engrossed in work with a hidden clock on the computer.

---

![000002.png](readme-content%2F000002.png)

A person embracing mindfulness, taking a break from work and feeling a sense of spaciousness in their day.

---

![000003.png](readme-content%2F000003.png)

A person experiencing an altered perception of time through mindfulness, seeing time as a fluid construct.

---

![000004.png](readme-content%2F000004.png)

A person sitting in a peaceful room, focusing on the present moment.

---

![000005.png](readme-content%2F000005.png)

A person practicing mindful eating, savoring each bite they take.

---

![000006.png](readme-content%2F000006.png)

A person taking a mindful walk, fully aware of their surroundings.

---

![000007.png](readme-content%2F000007.png)

A person pausing in their busy day to take a deep breath and find a moment of calm.

---

# Features

* Audio Splitting: Easily split your audio files into smaller segments.
* Custom Start Point: Choose where in the audio file to begin processing.
* Image Generation: Generate images based on a defined style and theme.

## Dependencies and Requirements

* Internet connection to process audio to text using Google Speech-to-Text.
* External LLM to process the raw text into an image prompt.
* HuggingFace Diffusion model to generate images based on the prompt.
* ffmpeg to split the audio files.
* flac to convert the audio files to the correct format.
* Python libraries listed in requirements.txt.
* Python 3.8 or higher.

# Pre installation

## Linux

```bash
sudo apt update && sudo apt install flac ffmpeg
```

Install miniconda OR anaconda, check:

## Using Anaconda

https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html#

** If you are using zsh, you need to add the following line to your .zshrc file: **

```bash
export PATH="/home/your_user/anaconda3/bin:$PATH"
```

** Using zsh: `export PATH=~/anaconda3/bin:$PATH`

```bash
conda init zsh
```
* For changes to take effect, close and re-open your current shell.


## Using Miniconda

https://docs.conda.io/projects/miniconda/en/latest/

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```

## Mac

```bash
brew install flac ffmpeg
````

# Installation

Create a virtual environment using conda or venv.

```bash
conda create -n audio2image python=3.11
conda activate audio2image
```

Install the requirements:

```bash
pip3 install -r requirements.txt
```

Download the models:

Model that can be used:

https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/tree/main

# Copy and set environment variables

```bash
cp .env.example .env
```

OPENAI_TOKEN: Your OpenAI API token. You can find this in your OpenAI account settings.

ORGANIZATION_ID: Your OpenAI organization ID. You can find this in your OpenAI account settings.

PIPE_TO: The device to run the model on. This can be "cpu", "cuda", or "mps" (multi-processing service).

MODEL: The path to the model you want to use. This can be a local path or a HuggingFace model ID.

USE_DALLE: Whether to use the DALL-E model or not. This can be "true" or "false". Set false to use local Stable Diffusion model.

OPENAI_DALLE_MODEL: The dalle model, usually "dall-e-2" or "dall-e-3" - Check https://openai.com/pricing

OPENAI_DALLE_RESOLUTION: The resolution of the dall-e model, usually "512x512" or "1024x1024" - Check https://platform.openai.com/docs/guides/images


# Usage

Command-Line Arguments
-f: The path to the audio file to be processed.

-s: The style prompt to use for image generation.

-t: The theme to use for image generation.

-n: The name of the output folder.

-lang [optional]: The original language of the audio file, if needed for translation.


# Calling the script

Copy code
```bash
python main.py -f path/to/audio.mp3 -s "surreal landscapes" -t "fantasy" -n "MyProject"
```

This command splits the audio.mp3 based in the silence. 
It also sets the theme for image generation to "fantasy" with a style prompt of "surreal landscapes", and outputs the files to a folder named "MyProject".

## Output
The audio file will be split according to the specified parameters.
Images generated based on the provided style and theme will be saved in the designated output folder.

Expected output:

```
MyProject
├── images
       ├── 000002.png
       ├── 00000n.png
├── gpt.txt
├── text.txt
└── compiled.json
└── original_audio.mp3
```


Where the *.png files are the generated images
text.txt is the raw text, translated if needed. In case where the translation is needed, a file call original-lang.txt will be found with the original text. 

```text
0.000:For this week's podcast in english dot cam business podcast.  
8.857:We're talking about how technology has really changed the face of business.  
14.789:To be more specific we're really talking about the internet only nowadays richard every company whether they provide a service
23.987:or or sell a product.
```

gpt.txt is the refined text by the LLM model.

```text
0.0:Discuss how technology has transformed the face of business. Focus on the internet's impact and the rise of social media.
31.377:Explore the changes in communication for businesses. From professional emails to engaging on social media platforms like Twitter, Facebook, and LinkedIn.
68.45:Examine the effect of social media on both personal and professional aspects of everyday life.
```

and compiled.json is the json file with the text and images, ready to be used in the frontend.

```json

[
    {
        "secs": 0.0,
        "data": {
            "text": "For this week's podcast in english dot cam business podcast.",
            "gpt": "Discuss how technology has transformed the face of business. Focus on the internet's impact and the rise of social media.",
            "image_file": "eng-business/images/000001.png"
        }
    },
    {
        "secs": 8.857,
        "data": {
            "text": "We're talking about how technology has really changed the face of business.",
            "gpt": ""
        }
    },
    {
        "secs": 14.789,
        "data": {
            "text": "To be more specific we're really talking about the internet only nowadays richard every company whether they provide a service",
            "gpt": ""
        }
    }
]
```

The fields in the compiled.json are:

* secs: The time in seconds where the text was extracted from the audio file.
* data: The data extracted from the audio file.
  * text: The raw text extracted from the audio file.
  * gpt: The refined text extracted from the audio file. Can be empty
  * image_file: The image generated based on the text. Can not exist if gpt is empty.


and the zip file in the output-final folder:

```
MyProject.zip
```

This is the file that can be used in the `ui` folder, to load the audio and show the result synced.

The project can be found in the `ui` folder.


## Extra

Aesthetics and styles are not limited only to fashion. They have also manifestations in music, architecture, furniture, ceramic, graphic design, interior design, illustration, painting, sculpture and art in general.

https://aesthetics.fandom.com/wiki/List_of_Aesthetics