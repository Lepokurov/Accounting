from fastapi import Header, HTTPException, status, Depends
from app.core.config import settings
from typing import Optional

async def auth_bearer(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token")
    token = authorization.split(" ", 1)[1]
    if token != settings.api_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"sub": "api", "token": token}

class Pagination:
    def __init__(self, limit: int = 50, offset: int = 0):
        self.limit = min(max(limit, 1), 500)
        self.offset = max(offset, 0)

async def get_pagination(limit: int = 50, offset: int = 0) -> Pagination:
    return Pagination(limit=limit, offset=offset)