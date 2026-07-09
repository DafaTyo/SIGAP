import pytest
from sqlalchemy import create_engine, inspect
from app.db.base_class import Base

# Import semua model yang akan kita buat nanti (akan gagal di sini karena belum ada)
try:
    from app.models.user import User
    from app.models.vendor import Vendor
    from app.models.distribution import DistributionReport
    from app.models.complaint import Complaint
    from app.models.audit_log import AuditLog
except ImportError:
    pass

@pytest.fixture(scope="module")
def db_inspector():
    # Setup in-memory sqlite untuk testing schema creation
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    return inspector

def test_user_table_exists(db_inspector):
    tables = db_inspector.get_table_names()
    assert "users" in tables

def test_vendor_table_exists_with_fields(db_inspector):
    tables = db_inspector.get_table_names()
    assert "vendors" in tables
    
    columns = [col["name"] for col in db_inspector.get_columns("vendors")]
    assert "id" in columns
    assert "nama_usaha" in columns
    assert "nik_penanggung_jawab" in columns
    # Tidak perlu nik_penanggung_jawab_masked di DB, itu computed logic di schema Pydantic/API
    assert "status" in columns

def test_distribution_table_has_radius(db_inspector):
    tables = db_inspector.get_table_names()
    assert "distribution_reports" in tables
    
    columns = [col["name"] for col in db_inspector.get_columns("distribution_reports")]
    assert "radius" in columns
    assert "latitude" in columns
    assert "longitude" in columns

def test_complaint_table_has_distribution_id_and_date(db_inspector):
    tables = db_inspector.get_table_names()
    assert "complaints" in tables
    
    columns = [col["name"] for col in db_inspector.get_columns("complaints")]
    assert "distribution_id" in columns
    assert "tanggal_kejadian" in columns

def test_audit_log_table_exists(db_inspector):
    tables = db_inspector.get_table_names()
    assert "audit_logs" in tables
    
    columns = [col["name"] for col in db_inspector.get_columns("audit_logs")]
    assert "action" in columns
    assert "entity_type" in columns
