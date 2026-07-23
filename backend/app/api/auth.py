"""Auth router — /auth endpoints per api-contract.yaml.

Endpoints:
- POST /login (issue JWT token)
- GET /me (current user info)
- GET /me/permissions (CASL permissions)
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, settings
from app.dependencies.jwt_auth import UserPayload
from app.domains.user.repositories import get_user_by_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    # Lookup user by email/username
    user = await get_user_by_email(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email atau password salah")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Akun tidak aktif")

    scope_list = user.scope_value.split(",") if user.scope_value else []
    payload = {
        "sub": str(user.id),
        "role": user.role,
        "scope_type": user.scope_type,
        "scope_value": scope_list,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRES_MINUTES),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": settings.JWT_EXPIRES_MINUTES * 60,
    }


@router.get("/me")
async def get_me(
    user: UserPayload = Depends(get_current_user),
) -> dict[str, Any]:
    return {
        "id": user.id,
        "role": user.role,
        "scope_type": user.scope_type,
        "scope_value": user.scope_value,
    }


@router.get("/me/permissions")
async def get_permissions(
    user: UserPayload = Depends(get_current_user),
) -> dict[str, Any]:
    permissions_map = {
        "vendor": [
            "vendor:read", "vendor:write",
            "distribution:write", "distribution:read",
            "complaint:read",
        ],
        "verifikator_bgn": [
            "vendor:read", "vendor:write", "vendor:verify",
            "distribution:read", "distribution:write",
            "complaint:read", "complaint:write",
            "audit:read",
        ],
        "pengawas_dinas": [
            "vendor:read",
            "distribution:read",
            "complaint:read", "complaint:write",
        ],
        "admin": [
            "vendor:read", "vendor:write", "vendor:verify",
            "distribution:read", "distribution:write",
            "complaint:read", "complaint:write",
            "audit:read", "audit:write",
            "user:read", "user:write",
        ],
    }
    return {
        "role": user.role,
        "permissions": permissions_map.get(user.role, []),
        "scope": {
            "type": user.scope_type,
            "value": user.scope_value,
        },
    }
