"""
SIGAP Development Seed — run ONCE after setting up the project.

Creates tables (if not exist) and seeds:
  - admin@sigap.gov / admin123 (role: admin, scope: nasional)

Usage:
  cd /mnt/c/SIGAP/backend
  python scripts/seed_dev.py

Requires .env with DATABASE_URL pointing to a file-based SQLite (not :memory:).
"""

from __future__ import annotations

import asyncio
import os
import sys
import uuid
from datetime import datetime, timezone

# Ensure backend dir is on sys.path so 'app' is importable
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db_session import engine, _SessionLocal
from app.domains.vendor.models import Base as VendorBase
from app.domains.distribution.models import Base as DistributionBase
from app.domains.complaint.models import Base as ComplaintBase
from app.domains.user.models import Base as UserBase, User

BASES = [VendorBase, DistributionBase, ComplaintBase, UserBase]

SEED_USERS = [
    {
        "email": "admin@sigap.gov",
        "name": "Admin SIGAP",
        "password": "admin123",
        "role": "admin",
        "scope_type": "nasional",
    },
    {
        "email": "verifikator@sigap.gov",
        "name": "Budi Verifikator",
        "password": "verifikator123",
        "role": "verifikator_bgn",
        "scope_type": "provinsi",
        "scope_value": "DKI Jakarta",
    },
    {
        "email": "vendor@warungberkah.id",
        "name": "Warung Berkah Sejahtera",
        "password": "vendor123",
        "role": "vendor",
        "scope_type": "provinsi",
        "scope_value": "DKI Jakarta",
    },
]


async def create_tables() -> None:
    """Create all tables if they don't exist (idempotent)."""
    async with engine.begin() as conn:
        for base in BASES:
            await conn.run_sync(base.metadata.create_all)
    print("  ✅ Tables ready")


async def seed_users(db: AsyncSession) -> int:
    """Insert seed users if table is empty. Returns count."""
    from sqlalchemy import select, func

    result = await db.execute(select(func.count(User.id)))
    existing = result.scalar() or 0
    if existing > 0:
        print(f"  ⏭️  Users table already has {existing} row(s) — skipping seed")
        return 0

    pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
    created = 0
    for data in SEED_USERS:
        user = User(
            id=uuid.uuid4(),
            email=data["email"],
            name=data["name"],
            hashed_password=pwd.hash(data["password"]),
            role=data["role"],
            scope_type=data.get("scope_type", "provinsi"),
            scope_value=data.get("scope_value"),
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(user)
        created += 1
    await db.commit()
    print(f"  ✅ {created} user(s) seeded")
    return created


async def main() -> None:
    print("🌱 SIGAP Dev Seed\n")

    await create_tables()

    async with _SessionLocal() as session:
        await seed_users(session)

    print("\n🎉 Done! Users seeded:")
    print("   admin@sigap.gov      / admin123        (admin)")
    print("   verifikator@sigap.gov / verifikator123  (verifikator_bgn)")
    print("   vendor@warungberkah.id / vendor123       (vendor)")
    print()
    print("👉 Start server:  python -m uvicorn app.main:app --reload --port 8000")


if __name__ == "__main__":
    asyncio.run(main())
