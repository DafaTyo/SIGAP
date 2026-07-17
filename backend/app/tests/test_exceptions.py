"""Tests for custom exception hierarchy."""

from __future__ import annotations

import json
from app.core.exceptions import (
    VendorNotFound,
    PermissionDenied,
    RateLimitExceeded,
    IdempotencyConflict,
    DocumentValidationFailed,
    Unauthorized,
    NotFoundError,
)


def test_exception_to_json():
    exc = VendorNotFound(detail="Vendor 123 tidak ditemukan")
    data = json.loads(json.dumps({"detail": exc.detail, "status_code": exc.status_code}))
    assert data["detail"] == "Vendor 123 tidak ditemukan"
    assert data["status_code"] == 404


def test_exception_with_extra_headers():
    exc = RateLimitExceeded(headers={"Retry-After": "60"})
    assert exc.headers["Retry-After"] == "60"


def test_permission_denied_default_text():
    exc = PermissionDenied()
    assert "tidak memiliki izin" in exc.detail


def test_idempotency_conflict_default():
    exc = IdempotencyConflict()
    assert exc.status_code == 409


def test_all_exceptions_are_json_serializable():
    for cls in (
        VendorNotFound, PermissionDenied, RateLimitExceeded,
        IdempotencyConflict, DocumentValidationFailed, Unauthorized, NotFoundError
    ):
        exc = cls("test")
        json.dumps({"detail": exc.detail})
