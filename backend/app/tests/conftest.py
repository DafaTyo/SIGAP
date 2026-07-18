"""Shared pytest fixtures for SIGAP backend tests.

Fixtures:
  - settings_env: override env vars with safe test values
  - client: async httpx.AsyncClient wired to FastAPI test app
  - db_session: in-memory SQLite async session (unit tests)
  - mock_opa: respx mock that returns OPA allow=True by default
"""

from __future__ import annotations

import os
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

# Override env before any SIGAP import
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/99")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")
os.environ.setdefault("OPA_URL", "http://opa-mock:8181")
os.environ.setdefault("ENV", "test")


@pytest.fixture(scope="session", autouse=True)
def settings_env():
    """Ensures env vars are set for the whole test session."""
    yield


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all SQLite tables in memory before tests run."""
    import asyncio
    from app.dependencies.db_session import engine
    from app.domains.vendor.models import Base as VendorBase
    from app.domains.distribution.models import Base as DistBase
    from app.domains.complaint.models import Base as CompBase

    async def create_tables():
        async with engine.begin() as conn:
            # Drop/Create is safe for in-memory DB
            await conn.run_sync(VendorBase.metadata.create_all)
            await conn.run_sync(DistBase.metadata.create_all)
            await conn.run_sync(CompBase.metadata.create_all)

    asyncio.run(create_tables())
    yield


@pytest.fixture
async def client():
    """Async HTTP client pointing to the FastAPI test app."""
    from app.main import app  # lazy import after env override
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
