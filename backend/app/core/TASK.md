# 📌 Module Task Tracker: Core Package (backend/app/core)

## 🎯 Core Objective & Responsibility
- Menyediakan konfigurasi aplikasi global, logger, dan utilitas dasar yang dapat di‑import oleh seluruh modul backend.
- Tidak mengandung logika bisnis domain spesifik.

## 📋 Development Checklist
- [ ] **Create package init** – `__init__.py` (placeholder, akan berisi `logger = logging.getLogger(__name__)`).
- [ ] **Add configuration loader** – file `config.py` yang membaca variabel environment (`DATABASE_URL`, `REDIS_URL`, `JWT_SECRET`).
- [ ] **Add logger utility** – file `logger.py` dengan standar format JSON log.
- [ ] **Add generic exception base** – `exceptions.py` yang menurunkan `HTTPException` untuk reuse.
- [ ] **Write documentation** – `README.md` singkat di dalam folder menjelaskan apa yang harus di‑import.

## 🔒 Constraints & Best Practices
- Semua fungsi harus **stateless** dan tidak membuka koneksi DB; koneksi dikelola di `dependencies/`.
- Logger harus dapat di‑override dalam testing (handler `NullHandler`).
- Tidak menulis kode yang berinteraksi dengan framework FastAPI di sini.

## 📄 References
- `docs/DESIGN.md` (section *Technical Architecture*).
- `api-contract.yaml` untuk memastikan endpoint‑endpoint memakai konfigurasi yang didefinisikan.

---

**Instruksi Eksplisit:** Implementasi kode (Python) baru **boleh** dimulai hanya setelah semua item checklist di atas ditandai selesai.
