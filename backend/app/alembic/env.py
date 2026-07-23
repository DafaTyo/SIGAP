"""Alembic configuration file."""
from __future__ import annotations

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine

# Add the backend to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in terms of env_vars.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from app.domains.vendor.models import Vendor, SIODigital
from app.domains.distribution.models import DistributionReport
from app.domains.complaint.models import Complaint
from app.domains.user.models import User

target_metadata = Vendor.metadata
target_metadata.tables.update(SIODigital.metadata.tables)
target_metadata.tables.update(DistributionReport.metadata.tables)
target_metadata.tables.update(Complaint.metadata.tables)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = AsyncEngine(
        engine_from_config(
            config.get_main_option("sqlalchemy.url"),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    with connectable.connect() as connection:
        connection = connection.sync()

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()