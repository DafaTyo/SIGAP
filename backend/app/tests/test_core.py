"""Tests for app.core — config, logger, exceptions."""

from __future__ import annotations

import json
import pytest
from app.core.config import settings


class TestSettings:
    def test_defaults_present(self):
        assert settings.DATABASE_URL
        assert settings.JWT_ALGORITHM == "HS256"
        assert settings.OPA_POLICY_PATH == "v1/data/sigap/auth/allow"

    def test_idempotency_ttl_24h(self):
        assert settings.IDEMPOTENCY_TTL_SECONDS == 86400  # 24 h per kontrak


class TestLogger:
    def test_logger_binds_fields(self):
        from app.core.logger import configure_logging, get_logger
        configure_logging()
        log = get_logger("test_core")
        bound = log.bind(module="test")
        assert bound is not None


class TestExceptions:
    def test_unauthorized_has_401(self):
        from app.core.exceptions import Unauthorized
        exc = Unauthorized()
        assert exc.status_code == 401
        assert exc.detail == "Token tidak ada atau tidak valid"

    def test_permission_denied_403(self):
        from app.core.exceptions import PermissionDenied
        exc = PermissionDenied("Custom message")
        assert exc.status_code == 403
        assert exc.detail == "Custom message"

    def test_vendor_not_found_404(self):
        from app.core.exceptions import VendorNotFound
        exc = VendorNotFound()
        assert exc.status_code == 404

    def test_idempotency_conflict_409(self):
        from app.core.exceptions import IdempotencyConflict
        exc = IdempotencyConflict()
        assert exc.status_code == 409

    def test_rate_limit_exceeded_429(self):
        from app.core.exceptions import RateLimitExceeded
        exc = RateLimitExceeded()
        assert exc.status_code == 429

    def test_document_validation_failed_422(self):
        from app.core.exceptions import DocumentValidationFailed
        exc = DocumentValidationFailed()
        assert exc.status_code == 422
