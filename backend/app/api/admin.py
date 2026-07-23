"""Admin router — /admin endpoints per api-contract.yaml.

Endpoints:
- POST /users (admin create user)
- GET /users (list users)
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.dependencies.jwt_auth import UserPayload
from app.core.exceptions import PermissionDenied
from app.domains.user.models import User
from app.domains.user.schemas import UserCreate as UserCreateSchema, UserRead
from app.domains.user.repositories import create_user, list_users, get_user_by_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


@router.post("/users", response_model=UserRead, status_code=201)
async def create_user_endpoint(
    dto: UserCreateSchema,
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
) -> UserRead:
    if user.role != "admin":
        raise PermissionDenied(detail="Hanya admin yang dapat membuat user baru")

    existing = await get_user_by_email(db, dto.email)
    if existing:
        from fastapi import HTTPException
        raise HTTPException(status_code=409, detail="Email sudah terdaftar")

    new_user = User(
        email=dto.email,
        name=dto.name,
        hashed_password=pwd_context.hash(dto.password),
        role=dto.role,
        scope_value=",".join(dto.scope_value) if dto.scope_value else None,
    )
    await create_user(db, new_user)
    await db.commit()

    return UserRead(
        id=new_user.id,
        email=new_user.email,
        name=new_user.name,
        role=new_user.role,
        scope_value=dto.scope_value,
        is_active=new_user.is_active,
        created_at=new_user.created_at,
    )


@router.get("/users", response_model=list[UserRead])
async def list_users_endpoint(
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
) -> list[UserRead]:
    if user.role != "admin":
        raise PermissionDenied(detail="Hanya admin yang dapat melihat daftar user")

    users = await list_users(db)
    return [
        UserRead(
            id=u.id,
            email=u.email,
            name=u.name,
            role=u.role,
            scope_value=u.scope_value.split(",") if u.scope_value else [],
            is_active=u.is_active,
            created_at=u.created_at,
        )
        for u in users
    ]
