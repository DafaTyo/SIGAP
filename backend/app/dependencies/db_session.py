
from collections.abc import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.dependencies.jwt_auth import get_current_user
from fastapi import Depends, Request

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)
_SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)

async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with _SessionLocal() as session:
        # RLS Injection (if request.state.user set by auth middleware)
        user = getattr(request.state, "user", None)
        if user:
            # Set per‑session RLS variables
            await session.execute(text("SET LOCAL app.current_user_id = :uid"), {"uid": user.id})
            scope_val = ",".join(user.scope_value) if isinstance(user.scope_value, list) else str(user.scope_value)
            await session.execute(text("SET LOCAL app.current_scope = :scope"), {"scope": scope_val})
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
