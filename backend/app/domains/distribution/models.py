"""Distribution domain model — matches api-contract.yaml DistributionReport."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Integer, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.domains.vendor.models import Base


class DistributionReport(Base):
    __tablename__ = "distributions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vendor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("vendors.id"), nullable=False)
    jumlah_porsi: Mapped[int] = mapped_column(Integer, nullable=False)
    lokasi_sekolah: Mapped[str | None] = mapped_column(String(255))
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    foto_url: Mapped[str | None] = mapped_column(Text)
    reported_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    photo_taken_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    tampering_suspicion: Mapped[bool] = mapped_column(Boolean, default=False)
