from groq import Groq
import os
import json
from dotenv import load_dotenv
from tool import logger
from langfuse import Langfuse
from langfuse import observe

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST"),
)

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

# ----------------- MÓDULO I -----------------
@observe(name="generate-brand-manual")
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
    try:
        content = res.choices[0].message.content
        return json.loads(content)
    except json.JSONDecodeError:
        logger.error(f"generate_brand_manual_content_error\n{content}\n")
        raise ValueError("El modelo no devolvió JSON válido")


# ----------------- MÓDULO II -----------------
@observe(name="generate-creative-asset")
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
    
    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    content = res.choices[0].message.content
    return content
