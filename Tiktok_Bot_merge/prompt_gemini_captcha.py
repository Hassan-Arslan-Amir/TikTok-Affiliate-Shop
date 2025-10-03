
import json
import google.generativeai as genai
import requests
import logging
from PIL import Image
from io import BytesIO
import time

genai.configure(api_key="AIzaSyCuYS7VOWYmCeQU3oZ9Ryj6tvDzXkYNVyY")


def prompt_gemini_captcha(img_url, type):
    response = requests.get(img_url)
    if response.status_code != 200:
        print("Failed to download captcha image")
        return False
    model = genai.GenerativeModel(model_name=('gemini-1.5-pro'))
    
    image = Image.open(BytesIO(response.content))
    prompt_message = None
    
    # response = model.generate_content("Explain how AI works")
    if type == 'slider':
        prompt_message = """
        Task: Find the puzzle piece

            Important analysis steps:
            1. Find the EXACT center (centroid) of the puzzle piece.
            2. Return ONLY this center coordinate as a JSON with exact format:
            {
                "coord": {"x": 0.X, "y": 0.Y}
            }

            Response requirements:
            - X and Y must be float values between 0-1
            - (0,0) is top-left, (1,1) is bottom-right
            - Center coordinate only
            - The X and Y values must be unique. Meaning X from 0.X and Y from 0.Y are different.
            - NO explanatory text, ONLY the JSON
            - Must find exactly ONE coord as there will only be one puzzle piece
        """
    elif type == 'shapes':
        prompt_message = """
        Task: Find EXACTLY TWO matching elements, where elements can be either:
            a) Two identical 3D shapes
            OR
            b) Two identical characters (letters/numbers)

            Important analysis steps:
            1. Look for identical 3D geometric shapes first
            2. If no matching shapes found, look for identical characters/text
            3. Calculate the center coordinates of the matching pair
            4. Return ONLY a JSON with exact format:
            {
                "matches": [
                    {
                        "shape1": {"x": 0.X, "y": 0.Y, "type": "TYPE"},
                        "shape2": {"x": 0.X, "y": 0.Y, "type": "TYPE"}
                    }
                ]
            }

            Response requirements:
            - TYPE must be either "shape" or "character"
            - X and Y must be float values between 0-1
            - (0,0) is top-left, (1,1) is bottom-right
            - Center coordinates only
            - The X and Y values across both shapes bust be all unique. Meaning (a, b), (c, d) are all different.
            - NO explanatory text, ONLY the JSON
            - Must find exactly ONE pair (either shapes or characters)
        """
    
    logging.info(f"Prompting Gemini with image and message")
    start_time = time.time()
    response = model.generate_content([image, prompt_message])
    end_time = time.time()
    logging.info(f"Prompting took {end_time - start_time} seconds")
    
    raw_response = response.text.strip('```json\n').strip('```').strip()
    return json.loads(raw_response)