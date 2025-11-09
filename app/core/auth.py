"""
Middleware for validating incoming bearer tokens.

This file implements:
- get_jwks(): fetch JWKS from openid-configuration (cached)
- verify_jwt(token): verify signature, expiry, audience if provided
- fastapi dependency: get_current_user (returns token payload dict)
"""

import time
import logging
from typing import Dict, Optional
from jose import jwt
import httpx
from fastapi import Request, HTTPException, status
from app.core.config import settings

logger = logging.getLogger(__name__)
_jwks_cache: Optional[Dict] = None
_jwks_fetched_at: Optional[float] = None
JWKS_TTL = 60 * 60  # 1 hour (Time To Live)

async def fetch_openid_config():
    """
    Fetch the OpenID Connect configuration document (well-known endpoint)
    from Azure AD using the AZURE_OPENID_CONFIG_URL.
    """
    if not settings.AZURE_OPENID_CONFIG_URL:
        raise RuntimeError("AZURE_OPENID_CONFIG_URL is not set in configuration.")
    async with httpx.AsyncClient() as client:
        r = await client.get(settings.AZURE_OPENID_CONFIG_URL, timeout=10)
        r.raise_for_status()
        return r.json()

async def get_jwks():
    """
    Fetch JWKS (public keys) and cache them in memory to avoid network calls.
    Returns cached keys if not expired.
    """
    global _jwks_cache, _jwks_fetched_at
    now = time.time()
    if _jwks_cache and _jwks_fetched_at and now - _jwks_fetched_at < JWKS_TTL:
        return _jwks_cache

    config = await fetch_openid_config()
    jwks_uri = config.get("jwks_uri")
    if not jwks_uri:
        raise RuntimeError("openid-configuration did not include jwks_uri")

    async with httpx.AsyncClient() as client:
        r = await client.get(jwks_uri, timeout=10)
        r.raise_for_status()
        jwks = r.json()
        _jwks_cache = jwks
        _jwks_fetched_at = now
        return jwks



async def verify_jwt(token: str, audience: Optional[str] = None) -> Dict:
    """
    Verify a JWT using JWKS and python-jose.
    Returns the token payload if valid; raises an exception if invalid.
    """
    jwks = await get_jwks()
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")
    if not kid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token header")

    key = None
    for jwk in jwks.get("keys", []):
        if jwk.get("kid") == kid:
            key = jwk
            break
    if key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token key not found")

    # Build public key and verify
    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=key.get("alg", ["RS256"]),
            audience=audience,
            options={"verify_at_hash": False},
        )
        return payload
    except Exception as exc:
        logger.exception("JWT verification failed")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))

async def get_current_user(request: Request, audience: Optional[str] = None):
    """
    Extract Bearer token from Authorization header, verify it with Azure public keys,
    and return the decoded JWT payload representing the current user.
    """
    auth = request.headers.get("authorization")
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    parts = auth.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")
    token = parts[1]
    payload = await verify_jwt(token, audience=audience)
    return payload
