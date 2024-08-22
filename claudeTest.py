#Test code for using Claude over ChatGpt. Tested both at one point.


import os
import anthropic
from PIL import Image
import requests

import base64
import httpx


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')

# Example usage
image_path = "car.jpg"
base64_image = image_to_base64(image_path)



image1_url = "https://centurionlifestyle.com/wp-content/uploads/2020/05/lamborghini-huracan-white.jpg"
image1_media_type = "image/jpeg"
image1_data = base64.b64encode(httpx.get(image1_url).content).decode("utf-8")


# Anthropic Key
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image1_media_type,
                        "data": base64_image,
                    },
                },
                {
                    "type": "text",
                    "text": "Describe this image."
                }
            ],
        }
    ],
)
print(message)