"""Base exception hierarchy for SIGAP.

Maps 1-to-1 with api-contract.yaml > components/responses:
  BadRequest(400), Unauthorized(401), Forbidden(403),
  NotFound(404), IdempotencyConflict(409),
  ValidationFailed(422), RateLimitExceeded(429).
"""

from __future__ import annotations

from fastapi import HTTPException


class SIGAPException(HTTPException):
    """Base for all SIGAP domain exceptions."""

    status_code: int = 500
    default_detail: str = "Internal server error"

    def __init__(
        self,
        detail: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            status_code=self.status_code,
            detail=detail or self.default_detail,
            headers=headers,
        )


class Unauthorized(SIGAPException):
    status_code = 401
    default_detail = "Token tidak ada atau tidak valid"


class PermissionDenied(SIGAPException):
    status_code = 403
    default_detail = "Anda tidak memiliki izin untuk resource ini"


class VendorNotFound(SIGAPException):
    status_code = 404
    default_detail = "Vendor tidak ditemukan"


class NotFoundError(SIGAPException):
    status_code = 404
    default_detail = "Resource tidak ditemukan"


class IdempotencyConflict(SIGAPException):
    status_code = 409
    default_detail = "Idempotency key sudah digunakan dengan payload berbeda"


class DocumentValidationFailed(SIGAPException):
    status_code = 422
    default_detail = "Validasi dokumen gagal"


class GeoValidationError(SIGAPException):
    status_code = 422
    default_detail = "Validasi geospasial gagal"


class RateLimitExceeded(SIGAPException):
    status_code = 429
    default_detail = "Terlalu banyak request — coba lagi nanti"
