"""Distribution router — /distributions endpoints per api-contract.yaml."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.domains.distribution.schemas import DistributionCreate, DistributionRead
from app.domains.distribution import services

router = APIRouter()


@router.post("", response_model=DistributionRead, status_code=201)
async def submit_report(dto: DistributionCreate, db: AsyncSession = Depends(get_db)):
    return await services.submit_report(db, dto)


@router.get("/{report_id}", response_model=DistributionRead)
async def get_report(report_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await services.get_detail(db, report_id)


@router.get("", response_model=list[DistributionRead])
async def list_reports(vendor_id: uuid.UUID | None = Query(None), db: AsyncSession = Depends(get_db)):
    return await services.list_reports(db, vendor_id=vendor_id)
