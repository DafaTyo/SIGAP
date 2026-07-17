"""JWT authentication dependency.

References:
  - api-contract.yaml: securitySchemes > bearerAuth (JWT)
  - dependencies/TASK.md: get_current_user, verify JWT, raise 401
"""

from __future__ import annotations

from datetime import datetime, timezone
from functools import lru_cache
from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from pydantic import BaseModel

from app.core.config import settings
from app.core.exceptions import Unauthorized

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/v1/auth/login",
    auto_error=True,
)


class UserPayload(BaseModel):
    """Decoded JWT claims — injected as Depends(get_current_user)."""

    id: str
    role: str
    scope_type: str = ""
    scope_value: list[str] = []


def _decode_token(token: str) -> dict[str, Any]:
    """Decode and validate JWT. Raises Unauthorized on any failure."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except JWTError as exc:
        raise Unauthorized(detail=f"Token tidak valid: {exc}") from exc

    exp = payload.get("exp")
    if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(
        tz=timezone.utc
    ):
        raise Unauthorized(detail="Token sudah kedaluwarsa")

    return payload


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> UserPayload:
    """Extract and validate user from JWT bearer token."""
    payload = _decode_token(token)

    user_id = payload.get("sub") or payload.get("id")
    if not user_id:
        raise Unauthorized(detail="Token tidak mengandung user ID")

    return UserPayload(
        id=str(user_id),
        role=payload.get("role", ""),
        scope_type=payload.get("scope_type", ""),
        scope_value=payload.get("scope_value", []),
    )
