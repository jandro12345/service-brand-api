# services/vision_service.py

import os
import json
from dotenv import load_dotenv
from google import genai
from PIL import Image
from tool import logger

from langfuse import Langfuse
from langfuse import observe

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST"),
)

MODEL = "gemini-3-flash-preview"


@observe(name="audit-image-gemini")
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
        response = client.models.generate_content(
            model=MODEL,
            contents=[prompt, image]
        )

        # logger.info(f"audit_image_response:\n{response.text}")

        clean_text = (
            response.text
            .replace("json", "")
            .replace("```", "")
            .strip()
        )

        parsed = json.loads(clean_text)

        return parsed

    except Exception as error:
        logger.error(f"Error audit_image: {str(error)}")
        return {
            "approved": False,
            "reason": "No se pudo interpretar la respuesta del modelo."
        }