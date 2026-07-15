# 📌 Module Task Tracker: Tests Package (backend/app/tests)

## 🎯 Core Objective & Responsibility
- Menyediakan **test suite** untuk seluruh backend menggunakan **pytest**.
- Memastikan masing‑masing domain, middleware, dan utilitas memiliki coverage minimal **80 %**.
- Menggunakan **fixtures** untuk DB transaction rollback, mock OPA server, dan mock Redis.

## 📋 Development Checklist
- [ ] **Package init** – `__init__.py` (men‑export pytest fixtures jika diperlukan).
- [ ] **Create conftest.py** – global fixtures:
  - `engine`, `SessionLocal`, `db` (transactional, rollback after each test).
  - `mock_opa` (HTTPX mock server).
  - `mock_redis` (fakeredis).
- [ ] **Domain Tests Subfolders** – `vendor/`, `distribution/`, `complaint/`
  - **Each folder** berisi test unit untuk `models`, `schemas`, `services`, `repositories`.
- [ ] **Middleware Tests** – `middleware/`
  - Test audit log insertion, RLS setter (assert `SET LOCAL` executed), OPA decision (allow/deny), idempotency (duplicate key returns stored response), rate‑limit (exceed limit raises 429).
- [ ] **Utils Tests** – `utils/`
  - Test masking functions, pagination, crypto helpers.
- [ ] **Integration Tests** – `integration/`
  - Spin up FastAPI app with in‑memory SQLite, hit endpoints via `httpx.AsyncClient`.
- [ ] **Coverage Report** – configure `pytest-cov` in `pyproject.toml` and generate `coverage.xml`.
- [ ] **Write Tests README** – menjelaskan cara menjalankan `pytest -x -vv` dan menghasilkan laporan HTML.

## 🔒 Constraints & Best Practices
- **Isolation:** Set `autouse=True` fixture to start a transaction before each test and rollback after.
- **No external network:** OPA and Redis calls must be mocked; CI harus offline.
- **Deterministic:** Gunakan seed random (`random.seed(0)`) untuk reproducibility.
- **Naming:** Test files harus berakhiran `_test.py` atau `test_*.py`.

## 📄 References
- `api-contract.yaml` – untuk memverifikasi request/response schema dalam integration tests.
- `backend/app/middleware/` – tiap middleware memiliki unit‑test spesifik.

---

**Instruksi Eksplisit:** Kode test (Python) **tidak boleh** ditulis sebelum semua checklist di atas ditandai selesai.
