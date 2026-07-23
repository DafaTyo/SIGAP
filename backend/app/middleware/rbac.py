"""Centralized RBAC decorator using OPA policy engine.

Usage:
    from app.middleware.rbac import require_permission

    @router.get("/vendors")
    @require_permission("vendors:read")
    async def list_vendors(user: UserPayload = Depends(get_current_user), ...):
        ...

Roles defined in PRD §2:
  - admin
  - verifikator_bgn
  - pengawas_dinas
  - vendor

Permission matrix (PRD §4.1 + OPA Rego):
  vendors:read    → admin, verifikator_bgn, pengawas_dinas
  vendors:write   → admin, vendor
  vendors:reveal  → admin, verifikator_bgn
  vendors:verify  → verifikator_bgn
  distributions:read   → admin, verifikator_bgn, pengawas_dinas, vendor
  distributions:write  → vendor
  distributions:metadata → admin, verifikator_bgn, pengawas_dinas
  distributions:appeal  → vendor
  complaints:read   → admin, verifikator_bgn, pengawas_dinas
  complaints:write  → admin, verifikator_bgn
  complaints:public → (no auth required)
"""
from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any

from app.core.exceptions import PermissionDenied
from app.dependencies.jwt_auth import UserPayload

# Static permission map: permission → set of allowed roles
PERMISSION_MAP: dict[str, set[str]] = {
    "vendors:read": {"admin", "verifikator_bgn", "pengawas_dinas"},
    "vendors:write": {"admin", "vendor"},
    "vendors:reveal": {"admin", "verifikator_bgn"},
    "vendors:verify": {"verifikator_bgn"},
    "distributions:read": {"admin", "verifikator_bgn", "pengawas_dinas", "vendor"},
    "distributions:write": {"vendor"},
    "distributions:metadata": {"admin", "verifikator_bgn", "pengawas_dinas"},
    "distributions:appeal": {"vendor"},
    "complaints:read": {"admin", "verifikator_bgn", "pengawas_dinas"},
    "complaints:write": {"admin", "verifikator_bgn"},
}


def require_permission(permission: str) -> Callable:
    """Decorator that enforces RBAC on a FastAPI endpoint.

    Must be used with `Depends(get_current_user)` named `user` in the
    function signature. The decorator checks `user.role` against the
    permission map.

    Args:
        permission: A string like "vendors:read", "distributions:write".

    Raises:
        PermissionDenied: If the user's role is not allowed.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Extract user from kwargs (FastAPI dependency injection)
            user: UserPayload | None = kwargs.get("user")
            if user is None:
                raise PermissionDenied(
                    detail="Autentikasi diperlukan untuk mengakses resource ini"
                )
            allowed_roles = PERMISSION_MAP.get(permission, set())
            if user.role not in allowed_roles:
                raise PermissionDenied(
                    detail=f"Role '{user.role}' tidak memiliki izin '{permission}'"
                )
            return await func(*args, **kwargs)

        return wrapper

    return decorator