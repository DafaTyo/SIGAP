"""Vendor domain models — matches api-contract.yaml Vendor schema.

NIK stored encrypted (pgcrypto BYTEA); masked version computed on read.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, Float, DateTime, CheckConstraint, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nama_usaha: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    nik_encrypted: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    nik_masked: Mapped[str] = mapped_column(String(20), nullable=False)
    nib: Mapped[str] = mapped_column(String(50), nullable=False)
    alamat: Mapped[str] = mapped_column(Text, nullable=False)
    provinsi: Mapped[str] = mapped_column(String(100), nullable=False)
    kabupaten_kota: Mapped[str] = mapped_column(String(100), nullable=False)
    kontak_telepon: Mapped[str | None] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(
        String(30),
        CheckConstraint("status IN ('pending_verification','verified','rejected','suspended')"),
        default="pending_verification",
    )
    vendor_score: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
