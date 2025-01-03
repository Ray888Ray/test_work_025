from fastapi import APIRouter, HTTPException, Header
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()


def api_key_auth(authorization: str = Header(None)):
    if authorization != f"ApiKey {os.getenv("API_KEY")}":
        raise HTTPException(status_code=401, detail="Invalid API Key")
