# Import seluruh SQLAlchemy model di sini agar Alembic dapat mendeteksi metadata.
from app.db.base_class import Base
from app.models.audit_log import AuditLog
from app.models.complaint import Complaint
from app.models.distribution import DistributionReport
from app.models.user import User
from app.models.vendor import Vendor

__all__ = ["Base", "AuditLog", "Complaint", "DistributionReport", "User", "Vendor"]
