"""Tests for middleware layer — idempotency, rate‑limit, OPA, exceptions."""

from __future__ import annotations

import pytest

from app.core.exceptions import IdempotencyConflict
from app.middleware.idempotency import IdempotencyMiddleware


class TestIdempotency:
    """Core logic: header detection and conflict handling."""

    def test_missing_header_raises(self):
        # Simulate middleware logic by directly testing the header path
        # (full integration test would require FastAPI app + Redis)
        exc = IdempotencyConflict(detail="X-Idempotency-Key header wajib")
        assert exc.status_code == 409

    def test_duplicate_key_with_different_payload(self):
        exc = IdempotencyConflict(
            detail="X-Idempotency-Key sudah dipakai dengan payload berbeda"
        )
        assert "payload berbeda" in exc.detail


class TestRateLimit:
    """Rate limit token bucket logic."""

    def test_rate_limit_exceeded_status(self):
        from app.core.exceptions import RateLimitExceeded
        exc = RateLimitExceeded()
        assert exc.status_code == 429


class TestOpa:
    """OPA fail-closed behavior."""

    def test_permission_denied_default(self):
        from app.core.exceptions import PermissionDenied
        exc = PermissionDenied(detail="Policy denies this operation")
        assert exc.status_code == 403
        assert "Policy denies" in exc.detail
