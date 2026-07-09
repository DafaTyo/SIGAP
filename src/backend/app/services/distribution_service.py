from sqlalchemy.orm import Session

from app.models.distribution import DistributionReport


def create_distribution_report(
    db: Session,
    *,
    vendor_id: str,
    jumlah_porsi: int,
    latitude: float,
    longitude: float,
    lokasi_sekolah: str | None = None,
    radius: float | None = None,
    foto_url: str | None = None,
    anomaly: dict | None = None,
) -> DistributionReport:
    report = DistributionReport(
        vendor_id=vendor_id,
        jumlah_porsi=jumlah_porsi,
        lokasi_sekolah=lokasi_sekolah,
        latitude=latitude,
        longitude=longitude,
        radius=radius,
        foto_url=foto_url,
        anomaly=anomaly,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report
