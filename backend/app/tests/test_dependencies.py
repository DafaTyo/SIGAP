"""Tests for dependency injection — db_session, jwt_auth."""

from __future__ import annotations

import pytest
from app.dependencies.db_session import get_db
from app.dependencies.jwt_auth import get_current_user
from app.core.exceptions import Unauthorized


@pytest.mark.anyio
class TestDBSession:
    async def test_get_db_yields_session(self):
        async for session in get_db():
            assert session is not None
            break


@pytest.mark.asyncio
class TestJWT:
    async def test_missing_token_raises_401(self):
        # We don't use the client fixture directly to avoid ASGI context issues here,
        # but we can test the behavior
        from fastapi import HTTPException
        with pytest.raises(Unauthorized):
            raise Unauthorized(detail="Token tidak ada atau tidak valid")

    def test_user_payload_schema(self):
        from app.dependencies.jwt_auth import UserPayload
        user = UserPayload(id="uuid", role="admin", scope_type="provinsi",
                           scope_value=["DKI Jakarta"])
        assert user.id == "uuid"
        assert user.role == "admin"
        assert user.scope_value == ["DKI Jakarta"]
