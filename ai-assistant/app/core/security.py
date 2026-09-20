"""Optional API-key protection for the /agent endpoints."""

import secrets

from fastapi import Header, HTTPException, status

from app.core.config import get_settings


def require_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    expected = get_settings().api_key
    if not expected:
        return  # No key configured: open access (fine for local use, not for production).
    if not x_api_key or not secrets.compare_digest(x_api_key.encode(), expected.encode()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key. Send it in the X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )
