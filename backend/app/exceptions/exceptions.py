"""Domain-level exception factory — thin re-export layer.

All exception classes are defined in app.core.exceptions.
This module exists so that:
  1. TASK.md has a dedicated folder.
  2. Future domain-specific exceptions (VendorDomainException, etc.)
     can be added here without polluting core.
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
