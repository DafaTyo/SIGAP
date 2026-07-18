"""Application configuration loaded from environment variables.

References:
  - api-contract.yaml: server URLs, security schemes
  - DATA_GOVERNANCE.md §11: idempotency window 24h
  - DESIGN.md §2.1: RLS via SET LOCAL
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central settings — all values come from env / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Database ──────────────────────────────────────────────
    # ponytail: aiosqlite for dev/test — swap to asyncpg via env DATABASE_URL in prod
    DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"

    # ── Redis ─────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── JWT ───────────────────────────────────────────────────
    JWT_SECRET_KEY: str = "CHANGE-ME-IN-PRODUCTION"
    NIK_ENCRYPTION_KEY: str = "CHANGE-ME-ENCRYPTION-KEY"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MINUTES: int = 60

    # ── OPA ───────────────────────────────────────────────────
    OPA_URL: str = "http://opa:8181"
    OPA_POLICY_PATH: str = "v1/data/sigap/auth/allow"

    # ── Rate Limiting ─────────────────────────────────────────
    RATE_LIMIT_DEFAULT: int = 60       # requests per window
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    # ── Idempotency ───────────────────────────────────────────
    IDEMPOTENCY_TTL_SECONDS: int = 86400  # 24 hours (DATA_GOVERNANCE §11)

    # ── Environment ───────────────────────────────────────────
    ENV: str = "dev"  # dev | staging | prod


settings = Settings()
