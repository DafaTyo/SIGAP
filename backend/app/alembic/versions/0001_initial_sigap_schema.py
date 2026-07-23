# A generic, single database migration file.

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial_sigap_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Vendors table with encrypted NIK
    op.create_table(
        "vendors",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("nama_usaha", sa.String(255), nullable=False, unique=True),
        sa.Column("nik_encrypted", sa.LargeBinary(), nullable=False),
        sa.Column("nik_masked", sa.String(20), nullable=False),
        sa.Column("nib", sa.String(50), nullable=False),
        sa.Column("alamat", sa.Text(), nullable=False),
        sa.Column("provinsi", sa.String(100), nullable=False),
        sa.Column("kabupaten_kota", sa.String(100), nullable=False),
        sa.Column("kontak_telepon", sa.String(20)),
        sa.Column(
            "status",
            sa.String(30),
            nullable=False,
            server_default="pending_verification",
        ),
        sa.Column("vendor_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    # Unique constraint on masked NIK
    op.create_unique_constraint("uq_vendors_nik_masked", "vendors", ["nik_masked"])

    # Create index on provinsi for ABAC filtering
    op.create_index("ix_vendors_provinsi", "vendors", ["provinsi"])

    # SIO digital table
    op.create_table(
        "sio_digital",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("vendor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("vendors.id"), nullable=False, unique=True),
        sa.Column("sio_code", sa.String(50), nullable=False, unique=True),
        sa.Column("qr_image_path", sa.String(255)),
        sa.Column("issued_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=False),
        sa.Column("issued_by", postgresql.UUID(as_uuid=True), nullable=False),
    )

    # Distributions table (with geog column for PostGIS)
    op.create_table(
        "distributions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("vendor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("vendors.id"), nullable=False),
        sa.Column("jumlah_porsi", sa.Integer(), nullable=False),
        sa.Column("lokasi_sekolah", sa.String(255)),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("geog", sa.Text()),  # PostGIS geography(Point,4326) as WKT for now
        sa.Column("foto_url", sa.Text()),
        sa.Column("reported_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("photo_taken_at", sa.DateTime(timezone=True)),
        sa.Column("tampering_suspicion", sa.Boolean(), server_default="false"),
    )
    op.create_index("ix_distributions_reported_at", "distributions", ["reported_at"])
    op.create_index("ix_distributions_vendor_id", "distributions", ["vendor_id"])

    # Complaints table
    op.create_table(
        "complaints",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("vendor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("vendors.id"), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("photo_url", sa.Text()),
        sa.Column("latitude", sa.Float()),
        sa.Column("longitude", sa.Float()),
        sa.Column("province", sa.String(100), nullable=False),
        sa.Column("status", sa.String(30), nullable=False, server_default="submitted"),
        sa.Column("severity", sa.String(20), nullable=False, server_default="low"),
        sa.Column("ticket_number", sa.String(50), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index("ix_complaints_province", "complaints", ["province"])
    op.create_index("ix_complaints_status", "complaints", ["status"])

    # Idempotency table (DB-based)
    op.create_table(
        "idempotency_keys",
        sa.Column("key", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("response_body", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_idempotency_expires_at", "idempotency_keys", ["expires_at"])


def downgrade() -> None:
    op.drop_table("idempotency_keys")
    op.drop_table("complaints")
    op.drop_table("distributions")
    op.drop_table("sio_digital")
    op.drop_table("vendors")