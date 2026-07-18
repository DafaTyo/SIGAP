"""Complaint router — /complaints endpoints per api-contract.yaml."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.domains.complaint.schemas import ComplaintCreate, ComplaintRead, ComplaintUpdate
from app.domains.complaint import services

router = APIRouter()


@router.post("", response_model=ComplaintRead, status_code=201)
async def submit_complaint(dto: ComplaintCreate, db: AsyncSession = Depends(get_db)):
    return await services.submit_complaint(db, dto)


@router.get("/{complaint_id}", response_model=ComplaintRead)
async def get_complaint(complaint_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await services.get_detail(db, complaint_id)


@router.patch("/{complaint_id}", response_model=ComplaintRead)
async def patch_complaint(complaint_id: uuid.UUID, dto: ComplaintUpdate, db: AsyncSession = Depends(get_db)):
    return await services.patch_complaint(db, complaint_id, dto)


@router.get("", response_model=list[ComplaintRead])
async def list_complaints(status: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    return await services.list_complaints(db, status=status)
