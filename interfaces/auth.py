import os
from fastapi import Header, HTTPException


async def require_api_key(x_api_key: str | None = Header(None), authorization: str | None = Header(None)):
    """Require a matching API key if `OCEANIC_API_KEY` is set.

    Accepts `X-API-KEY: <key>` or `Authorization: Bearer <key>`.
    If `OCEANIC_API_KEY` is not set, the dependency allows all requests.
    """
    expected = os.getenv("OCEANIC_API_KEY")
    if not expected:
        return True

    provided = None
    if x_api_key:
        provided = x_api_key
    elif authorization and authorization.lower().startswith("bearer "):
        provided = authorization.split(None, 1)[1]

    if not provided or provided != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    return True
