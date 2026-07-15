# 📌 Module Task Tracker: Dependencies Package (backend/app/dependencies)

## 🎯 Core Objective & Responsibility
- Menyediakan **dependency‑injection** untuk FastAPI:
  - Database session (SQLAlchemy)
  - JWT authentication / current user extraction
  - Redis cache client
  - Global settings loader (from env / config file)
- Memastikan semua dependensi dapat **mock** di test dengan mudah.

## 📋 Development Checklist
- [ ] **Package init** – `__init__.py` yang men‑export fungsi `get_db`, `get_current_user`, `get_redis`.
- [ ] **DB Session Dependency** – `db_session.py`
  - **Function:** `def get_db() -> Generator[Session, None, None]` (yield session, rollback on exception).
- [ ] **JWT Auth Dependency** – `jwt_auth.py`
  - **Function:** `def get_current_user(token: str = Depends(oauth2_scheme)) -> User` – verifikasi JWT, raise `401` bila tidak valid.
- [ ] **Redis Cache Dependency** – `redis_cache.py`
  - **Function:** `def get_cache() -> redis.Redis` – singleton client.
- [ ] **Settings Loader** – `settings.py`
  - **Class:** `Settings` (pydantic BaseSettings) membaca env vars (`DATABASE_URL`, `REDIS_URL`, `JWT_SECRET_KEY`, `OPA_URL`).
  - **Export:** `settings = Settings()` untuk di‑import di seluruh modul.
- [ ] **Write Dependency README** – contoh penggunaan di router (`Depends(get_db)`) dan mock tips untuk pytest (`override_get_db`).

## 🔒 Constraints & Best Practices
- **Connection pooling:** SQLAlchemy engine harus dibuat sekali di module‑level, bukan per request.
- **Secure JWT:** Algoritma HS256 dengan secret kuat, expiry 1 hour.
- **Redis TTL:** untuk idempotency keys gunakan TTL 24h (configurable).
- **Testing:** Semua fungsi harus dapat di‑override dengan `app.dependency_overrides` dalam FastAPI.

## 📄 References
- `docs/DESIGN.md` – bagian *Infrastructure Layer* (settings, cache).
- `api-contract.yaml` – requirement header `Authorization` dan `X‑Idempotency‑Key`.

---

**Instruksi Eksplisit:** Tidak ada kode python yang boleh ditulis sebelum semua checklist di atas di‑centang sebagai selesai.
