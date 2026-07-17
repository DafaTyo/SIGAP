"""Database session dependency with RLS hook.

References:
  - DESIGN.md §2.1: SET LOCAL app.current_user_id / app.current_scope
  - DATA_GOVERNANCE.md §7: RLS Reset — clear at end of request
  - dependencies/TASK.md: get_db() generator
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

engine_kwargs = {"pool_pre_ping": True}
if not settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs["pool_size"] = 10
    engine_kwargs["max_overflow"] = 20

engine = create_async_engine(
    settings.DATABASE_URL,
    **engine_kwargs
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def set_rls_context(
    session: AsyncSession,
    user_id: str,
    scope: str,
) -> None:
    """Set RLS variables on the current DB connection.

    MUST be called inside an active transaction (SET LOCAL requires one).
    Called by RLSSetterMiddleware after JWT authentication.
    """
    await session.execute(
        text("SET LOCAL app.current_user_id = :uid"),
        {"uid": user_id},
    )
    await session.execute(
        text("SET LOCAL app.current_scope = :scope"),
        {"scope": scope},
    )


async def reset_rls_context(session: AsyncSession) -> None:
    """Reset RLS variables — prevents cross-tenant leakage on pooled connections.

    Reference: DATA_GOVERNANCE.md §7 — RLSResetMiddleware.
    """
    await session.execute(text("RESET app.current_user_id"))
    await session.execute(text("RESET app.current_scope"))


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a DB session; rollback on exception, always close."""
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
