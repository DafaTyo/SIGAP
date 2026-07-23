# 📌 Module Task Tracker: Tests Package (backend/app/tests)

## 🎯 Core Objective & Responsibility
- Menjamin kualitas backend melalui automated tests: unit, integration, security, dan contract compliance.

## 📋 Development Checklist
- [ ] **Test setup** – `conftest.py` menyiapkan app client, DB session, dan Redis mock.
- [ ] **Core tests** – `test_core.py` untuk config, logger, exceptions.
- [ ] **Dependency tests** – `test_dependencies.py` untuk auth, RLS context, Redis cache.
- [ ] **Middleware tests** – `test_middleware.py` untuk audit, rate-limit, idempotency, OPA.
- [ ] **Domain tests** – `test_vendor.py`, `test_distribution.py`, `test_complaint.py`.
- [ ] **API contract tests** – `test_api.py` validasi semua endpoint sesuai OpenAPI.
- [ ] **Security tests** – RLS bypass attempt, PII leak scan, idempotency replay.

## 🔒 Constraints & Best Practices
- Minimum coverage target: core modules 80%.
- Gunakan `respx` untuk mock HTTP eksternal (OSS/BPOM/OPA).
- Jangan mengandalkan aiosqlite untuk menguji PostGIS/RLS; pakai PostgreSQL testcontainer untuk hal itu.

## 📄 References
- `docs/DESIGN.md` – architecture.
- `api-contract.yaml` – source of truth untuk endpoint contract.
- `docs/DATA_GOVERNANCE.md` – audit & retention.
