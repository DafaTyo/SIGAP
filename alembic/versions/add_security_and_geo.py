import uuid
import json
import os
from pathlib import Path
+
+from alembic import op
+import sqlalchemy as sa
@@
-    op.create_unique_constraint("uq_vendors_nik_encrypted", "vendors", ["nik_encrypted"]))
+    op.create_unique_constraint("uq_vendors_nik_encrypted", "vendors", ["nik_encrypted"])
*** End Patch
branch_labels = None
depends_on = None

def upgrade():
    # Ensure pgcrypto extension is available.
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    # Update vendors table to store encrypted NIK.
    op.add_column("vendors", sa.Column("nik_encrypted", sa.LargeBinary, nullable=False))
    op.drop_column("vendors", "nik_penanggung_jawab")
    op.alter_column("vendors", "nik_masked", new_column_name="nik_penanggung_jawab_masked")

    # Apply UNIQUE constraint on encrypted NIK.
    op.create_unique_constraint("uq_vendors_nik_encrypted", "vendors", ["nik_encrypted"]))

    # Add PostGIS extension for geospatial indexes.
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    # Create a geography point column for fast distance queries.
    op.add_column("distributions", sa.Column("geom", sa.Geography(geometry_type="POINT", srid=4326), nullable=True))
    # Populate geom from latitude/longitude for existing rows.
    op.execute(
        "UPDATE distributions SET geom = ST_MakePoint(longitude, latitude)::geography"
    )
    # Create spatial index.
    op.create_index("ix_distributions_geom", "distributions", ["geom"], postgresql_using="gist")

    # Idempotency table (optional – can be used instead of Redis).
    op.create_table(
        "idempotency_keys",
        sa.Column("key", sa.String, primary_key=True),
        sa.Column("response", sa.JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )
    # Index on expires_at for cleanup.
    op.create_index("ix_idempotency_expires", "idempotency_keys", ["expires_at"])

def downgrade():
    # Drop idempotency table.
    op.drop_table("idempotency_keys")
    # Drop spatial index and column.
    op.drop_index("ix_distributions_geom", table_name="distributions")
    op.drop_column("distributions", "geom")
    # Remove UNIQUE constraint and encrypted column.
    op.drop_constraint("uq_vendors_nik_encrypted", "vendors", type_="unique")
    op.drop_column("vendors", "nik_encrypted")
    # Re‑add plain NIK column (for rollback only – data loss possible).
    op.add_column("vendors", sa.Column("nik_penanggung_jawab", sa.String, nullable=False))
    # Restore original column name.
    op.alter_column("vendors", "nik_penanggung_jawab_masked", new_column_name="nik_masked")
    # Remove extensions (optional – they may be used elsewhere).
    op.execute("DROP EXTENSION IF EXISTS postgis")
    op.execute("DROP EXTENSION IF EXISTS pgcrypto")
