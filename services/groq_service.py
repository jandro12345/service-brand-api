from groq import Groq
import os
import json
from dotenv import load_dotenv
from tool import logger

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

# ----------------- MÓDULO I -----------------

def generate_brand_manual(briefing: str):

    prompt = f"""
    Genera un Manual de Marca en JSON:

    {{
      "mission": "",
      "vision": "",
      "values": [],
      "tone": "",
      "do_not": [],
      "positioning": "",
      "messaging_pillars": []
    }}

    Si el briefing contiene "prohibido", "evitar", "no usar",
    agrégalo en "do_not".

    Briefing:
    {briefing}

    Devuelve SOLO JSON válido.
    """
    logger.info(f"generate_brand_manual_prompt\n{prompt}\n")
    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        response_format={"type": "json_object"},
    )
    
    content = res.choices[0].message.content
    logger.info(f"generate_brand_manual_content\n{content}\n")
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("El modelo no devolvió JSON válido")


# ----------------- MÓDULO II -----------------

def generate_creative_asset(manual: dict, instructions: str, asset_type: str, brand_name: str):

    prompt = f"""
    Nombre de Marca: {brand_name}

    Usa este Manual de Marca:

    {json.dumps(manual, indent=2)}

    Genera un {asset_type} siguiendo estrictamente:
    - El tono
    - Los messaging_pillars
    - Las restricciones en do_not

    Instrucciones adicionales:
    {instructions}
    """
    
    logger.info(f"generate_creative_asset_prompt\n{prompt}\n")
    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    content = res.choices[0].message.content
    logger.info(f"generate_creative_asset_content\n{content}\n")
    return content


# ----------------- MÓDULO III (Texto) -----------------

def audit_text(manual: dict, content: str):

    prompt = f"""
    Evalúa si el contenido cumple el Manual de Marca.

    Manual:
    {json.dumps(manual, indent=2)}

    Contenido:
    {content}

    Devuelve SOLO JSON:

    {{
      "approved": true/false,
      "reason": ""
    }}
    """

    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return json.loads(res.choices[0].message.content)