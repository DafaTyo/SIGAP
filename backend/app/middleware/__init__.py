"""Middleware package – ordered as required.

Import order (FastAPI app.add_middleware):
    1. RLSSetterMiddleware
    2. OPAPolicyMiddleware
    3. IdempotencyMiddleware
    4. RateLimitMiddleware
    5. AuditLogMiddleware
"""

from app.middleware.rls_setter import RLSSetterMiddleware
from app.middleware.opa_policy import OPAPolicyMiddleware
from app.middleware.idempotency import IdempotencyMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.audit_log import AuditLogMiddleware

__all__ = [
    "RLSSetterMiddleware",
    "OPAPolicyMiddleware",
    "IdempotencyMiddleware",
    "RateLimitMiddleware",
    "AuditLogMiddleware",
]
