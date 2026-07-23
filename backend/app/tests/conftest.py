"""Shared pytest fixtures for SIGAP backend tests.

Fixtures:
  - settings_env: override env vars with safe test values
  - client: async httpx.AsyncClient wired to FastAPI test app
  - db_session: in-memory SQLite async session (unit tests)
  - test_user: seeded test user for auth
  - auth_headers: bearer token for test user
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone, timedelta

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from jose import jwt
from passlib.context import CryptContext

# Override env before any SIGAP import
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/99")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")
os.environ.setdefault("NIK_ENCRYPTION_KEY", "dGVzdC1lbmNyeXB0aW9uLWtleS0zMi1jaGFycy0tCg==")
os.environ.setdefault("OPA_URL", "http://opa-mock:8181")
os.environ.setdefault("ENV", "test")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="session", autouse=True)
def settings_env():
    """Ensures env vars are set for the whole test session."""
    yield


@pytest_asyncio.fixture(scope="session")
async def setup_database():
    """Create all SQLite tables in memory before tests run."""
    from app.dependencies.db_session import engine
    from app.domains.vendor.models import Base as VendorBase
    from app.domains.distribution.models import Base as DistBase
    from app.domains.complaint.models import Base as CompBase
    from app.domains.user.models import Base as UserBase

    async with engine.begin() as conn:
        await conn.run_sync(VendorBase.metadata.create_all)
        await conn.run_sync(DistBase.metadata.create_all)
        await conn.run_sync(CompBase.metadata.create_all)
        await conn.run_sync(UserBase.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def client(setup_database):
    """Async HTTP client pointing to the FastAPI test app."""
    from app.main import app
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def db_session(setup_database):
    """Provide a clean SQLAlchemy async session per test."""
    from app.dependencies.db_session import _SessionLocal
    async with _SessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def test_user(db_session):
    """Create a test admin user and return credentials."""
    from app.domains.user.models import User
    from app.domains.user.repositories import create_user

    user = User(
        id=uuid.uuid4(),
        email="test@test.com",
        name="Test User",
        hashed_password=pwd_context.hash("testpass123"),
        role="admin",
        scope_type="nasional",
        scope_value=None,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    await create_user(db_session, user)
    await db_session.commit()
    return {"email": "test@test.com", "password": "testpass123", "id": str(user.id)}


@pytest_asyncio.fixture
async def auth_headers(client, test_user):
    """Obtain JWT token and return Authorization headers."""
    response = await client.post(
        "/v1/auth/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
