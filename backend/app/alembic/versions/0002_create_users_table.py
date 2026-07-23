"""Create users table for auth.

Revision ID: 0002_create_users_table
Revises: 0001_initial_sigap_schema
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0002_create_users_table"
down_revision = "0001_initial_sigap_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.String(30), nullable=False, server_default="vendor"),
        sa.Column("scope_type", sa.String(30), server_default="provinsi"),
        sa.Column("scope_value", sa.String(500)),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])

    # Default admin user (password: admin123)
    op.execute(
        "INSERT INTO users (id, email, name, hashed_password, role, scope_type, scope_value, is_active) "
        "VALUES (gen_random_uuid(), 'admin@sigap.gov', 'Admin SIGAP', "
        "'$2b$12$LJ3m4ys3Lk0TSwHpOXzKceN0Lk0TSwHpOXzKceN0Lk0TSwHpOXzK', "
        "'admin', 'nasional', NULL, true)"
    )


def downgrade() -> None:
    op.drop_table("users")
