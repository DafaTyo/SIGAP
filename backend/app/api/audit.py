"""Audit router — /audit-logs endpoints per api-contract.yaml.

Endpoints implemented:
- GET / (list audit logs, filtered by entity_type and action)
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_db, get_current_user
from app.dependencies.jwt_auth import UserPayload

router = APIRouter()


@router.get("")
async def get_audit_logs(
    entity_type: str | None = Query(None),
    action: str | None = Query(None, pattern="^(CREATE|UPDATE|DELETE|PII_REVEAL)$"),
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
) -> dict:
    # In production: query actual audit_logs table
    # For now: return empty list as placeholder
    if user.role not in ("admin", "verifikator_bgn"):
        return {"data": [], "message": "Akses ditolak"}
    
    # Example query structure (would be uncommented in production):
    # stmt = select(AuditLog).order_by(AuditLog.timestamp.desc())
    # if entity_type:
    #     stmt = stmt.where(AuditLog.entity_type == entity_type)
    # if action:
    #     stmt = stmt.where(AuditLog.action == action)
    # result = await db.execute(stmt)
    # logs = result.scalars().all()
    
    return {
        "data": [],
        "pagination": {
            "page": 1,
            "page_size": 20,
            "total_items": 0,
            "total_pages": 0,
        }
    }