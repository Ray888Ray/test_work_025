from fastapi import APIRouter, HTTPException, Header


router = APIRouter()

API_KEY = "24e8a4d4-9c70-4d30-a897-c79492671f90"


def api_key_auth(authorization: str = Header(None)):
    if authorization != f"ApiKey {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")
