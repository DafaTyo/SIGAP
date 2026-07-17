"""Re-export all custom exception classes.

Usage:
    from app.exceptions import VendorNotFound, PermissionDenied
"""

from app.core.exceptions import (
    DocumentValidationFailed,
    IdempotencyConflict,
    NotFoundError,
    PermissionDenied,
    RateLimitExceeded,
    Unauthorized,
    VendorNotFound,
)

__all__ = [
    "VendorNotFound",
    "DocumentValidationFailed",
    "PermissionDenied",
    "RateLimitExceeded",
    "IdempotencyConflict",
    "Unauthorized",
    "NotFoundError",
]
