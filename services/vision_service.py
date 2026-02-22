# services/vision_service.py

import os
import json
from dotenv import load_dotenv
from google import genai
from PIL import Image
from tool import logger

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL = "gemini-3-flash-preview"


def audit_image(manual: dict, image_path: str):

    image = Image.open(image_path)

    prompt = f"""
    Evalúa si esta imagen cumple el Manual de Marca:

    {json.dumps(manual, indent=2)}

    Devuelve SOLO JSON:

    {{
      "approved": true/false,
      "reason": ""
    }}
    """

    try:
        return_data = ""
        response = client.models.generate_content(
            model=MODEL,
            contents=[prompt, image]
        )
        logger.info(f"audit_image_response:\n{response.text}")
        return_data = (response.text).replace("json", "")
        return json.loads(return_data)
    except Exception:
        logger.error(f"Error audit_image: {return_data}")
        return {
            "approved": False,
            "reason": "No se pudo interpretar la respuesta del modelo."
        }