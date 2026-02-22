import logging
from os import getenv
from typing import Optional
from fastapi import HTTPException, Header
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = getenv("API_TOKEN")

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

log_format = (
    "[%(asctime)s] [%(levelname)s] [%(name)s] "
    "%(message)s"
)

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


async def verify_api_token(
    api_key: Optional[str] = Header(default=""),
) -> Optional[HTTPException]:
    if api_key != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid Access")