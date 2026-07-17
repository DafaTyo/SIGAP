# 📌 Module Task Tracker: Middleware Package (backend/app/middleware)

## 🎯 Core Objective & Responsibility
- Implement request‑level cross‑cutting concerns in the order required by the security model:
  1. Row‑Level Security context injection.
  2. OPA policy enforcement.
  3. Idempotency key handling.
  4. Rate‑limit token bucket.
  5. Global audit logging.

## 📋 Development Checklist
- [x] **Package init** – `__init__.py` exporting middleware classes.
- [x] **RLS Setter** – `rls_setter.py` (sets `app.current_user_id`/`app.current_scope`).
- [x] **OPA Policy** – `opa_policy.py` (calls OPA, fail‑closed).
- [x] **Idempotency** – `idempotency.py` (stores/replays responses in Redis).
- [x] **Rate Limit** – `rate_limit.py` (per‑user/IP token bucket).
- [x] **Audit Log** – `audit_log.py` (writes rows to `audit_logs`).

## 🔒 Constraints & Best Practices
- Middleware must be added to FastAPI **in the exact order** listed above.
- RLS variables are always cleared (`RESET`) after the request to avoid leakage.
- OPA failures must result in a 403 (`PermissionDenied`).
- Idempotency keys are stored for 24 h (`IDEMPOTENCY_TTL_SECONDS`).
- Audit entries are immutable (append‑only table, trigger prevents UPDATE/DELETE).

## 📄 References
- `api-contract.yaml` – required `X‑Idempotency‑Key` header.
- `docs/DESIGN.md` – security middleware stack.
- `docs/DATA_GOVERNANCE.md` – audit‑log requirements.
