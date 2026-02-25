from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

# In a real system this would be stored in environment variables
API_KEY = "secret123"

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)):

    if api_key and api_key == API_KEY:
        return api_key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API key",
        headers={"WWW-Authenticate": "API-Key"},
    )
