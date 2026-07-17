# 📌 Module Task Tracker: Dependencies Package (backend/app/dependencies)

## 🎯 Core Objective & Responsibility
- Centralize dependency injection for FastAPI: DB session, JWT authentication, Redis cache, and settings re‑export.

## 📋 Development Checklist
- [x] **Package init** – `__init__.py` exposing helpers.
- [x] **DB Session** – `db_session.py` implemented with async SQLAlchemy, RLS helpers, and safe teardown.
- [x] **JWT Auth** – `jwt_auth.py` implemented (token decode, expiration check, `UserPayload`).
- [x] **Redis Cache** – `redis_cache.py` singleton client.
- [x] **Settings Export** – `settings.py` re‑exports `Settings`.

## 🔒 Constraints & Best Practices
- DB engine must adapt to SQLite for tests (conditional pool args).
- JWT must be validated on every request; expired tokens raise `Unauthorized`.
- Redis client is created once per process; `decode_responses=True`.

## 📄 References
- `api-contract.yaml` – `bearerAuth` security scheme.
- `docs/DESIGN.md` – dependency layer diagram.
- `docs/DATA_GOVERNANCE.md` – idempotency window definition.
