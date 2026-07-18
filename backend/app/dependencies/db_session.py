"""Database session dependency with RLS hook.

References:
  - DESIGN.md §2.1: SET LOCAL app.current_user_id / app.current_scope
  - DATA_GOVERNANCE.md §7: RLS Reset — clear at end of request
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# ponytail: single engine = aiosqlite only, zero conditional driver logic.
engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    pool_pre_ping=True,
)
_SessionLocal: async_sessionmaker[AsyncSession] | None = None


def _get_session_factory() -> async_sessionmaker[AsyncSession]:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
    return _SessionLocal


async def set_rls_context(session: AsyncSession, user_id: str, scope: str) -> None:
    await session.execute(text("SET LOCAL app.current_user_id = :uid"), {"uid": user_id})
    await session.execute(text("SET LOCAL app.current_scope = :scope"), {"scope": scope})


async def reset_rls_context(session: AsyncSession) -> None:
    await session.execute(text("RESET app.current_user_id"))
    await session.execute(text("RESET app.current_scope"))


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with _get_session_factory()() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
