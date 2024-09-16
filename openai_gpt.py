import logging
from utils import get_prompt
from openai import OpenAI


def prepare_text_for_image_generation(original_text, style, theme):
    from main import OPENAI_TOKEN, ORGANIZATION_ID
    client = OpenAI(api_key=OPENAI_TOKEN, organization=ORGANIZATION_ID)

    #Create a retry option for the API call
    retry = 0
    success = False
    while retry < 3:
        response, success = call_openai_api(client, original_text, style, theme)
        if success:
            return response

        retry += 1
        print(f"[{retry}/3] Error. Response:{response}, trying again")

    return ""


def call_openai_api(client, original_text, style, theme):
    model_name = "gpt-3.5-turbo"
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": get_prompt(theme, style)},
                {"role": "user", "content": original_text}
            ]
        )

        # Return the first response
        return (response.choices[0].message.content, True)
    except Exception as e:
        logging.error(
            f"[OpenAI] Error occurred while processing chat {e}"
        )
        return str(e), False


def generate_image_dalle(prompt):
    from main import OPENAI_TOKEN, ORGANIZATION_ID, OPENAI_DALLE_MODEL, OPENAI_DALLE_RESOLUTION
    client = OpenAI(api_key=OPENAI_TOKEN, organization=ORGANIZATION_ID)
    image = client.images.generate(prompt=prompt,
                                   model=OPENAI_DALLE_MODEL,
                                   n=1,
                                   size=OPENAI_DALLE_RESOLUTION,
    )
    return image
