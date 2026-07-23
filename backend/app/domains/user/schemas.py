"""User schemas — 1:1 with api-contract.yaml admin/user endpoints."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str = Field(..., min_length=8)
    role: str = Field(..., pattern="^(vendor|verifikator_bgn|pengawas_dinas|admin)$")
    scope_value: list[str] | None = None


class UserRead(BaseModel):
    id: UUID
    email: str
    name: str
    role: str
    scope_value: list[str] | None = None
    is_active: bool
    created_at: datetime


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
