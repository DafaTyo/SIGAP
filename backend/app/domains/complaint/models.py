"""Complaint domain model — matches api-contract.yaml Complaint schema."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy import String, Text, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.domains.vendor.models import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    vendor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    nama_pelapor: Mapped[str | None] = mapped_column(String(255))
    kategori: Mapped[str] = mapped_column(
        String(30),
        CheckConstraint("kategori IN ('keracunan','keterlambatan','kekurangan_porsi','kualitas_makanan','lainnya')"),
    )
    deskripsi: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(
        String(10),
        CheckConstraint("severity IN ('rendah','sedang','tinggi','kritis')"),
        default="rendah",
    )
    status: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint("status IN ('baru','diproses','ditindaklanjuti','ditutup')"),
        default="baru",
    )
    resolution_notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    sla_deadline: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(days=3),
    )
