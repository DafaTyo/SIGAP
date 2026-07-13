# TASK.md – SIGAP Master Project To‑Do List (Modular Monolith)

> **Catatan otomatis**: Setiap *Verification Criteria* yang dipenuhi oleh CI/CD pipeline akan men‑trigger skrip kecil (mis. `scripts/update_task_status.py`) yang mem‑parse file ini, meng‑ganti `[ ]` menjadi `[x]` pada baris yang bersangkutan, serta memperbarui status header tugas utama.  Dengan begitu, **status mencerminkan real‑time** tanpa harus meng‑edit manual.

---

## 1. Project Setup & Governance

| ID | Goals | Verification Criteria | Status |
|----|-------|-----------------------|--------|
| **TASK‑PRJ‑001** | • Inisialisasi repository Git, setup virtual‑env, dan buat file konfigurasi dasar (`.env.example`, `pyproject.toml`, `package.json`).<br>• Pastikan semua tim memakai **DAMA‑DMBOK** dan **Satu Data Indonesia** sebagai pedoman data‑governance.<br>• Definisikan `README.md` dengan badge CI, kontribusi, dan petunjuk quick‑start. | - [ ] Repo ter‑clone tanpa error.<br>- [ ] Virtual‑env (`python -m venv .venv`) berhasil dibuat dan di‑aktivasi.<br>- [ ] `make lint`, `make test` lulus di mesin lokal.<br>- [ ] `README.md` berisi badge CI (GitHub Actions) dan panduan **setup**.<br>- [ ] Dokumentasi strategi data governance (`docs/DATA_LINEAGE.md`) ada. | [ ] Pending |
| **TASK‑PRJ‑002** | • Buat *project scaffold* dengan folder‑folder modular (frontend, backend, infra, docs, data, scripts).<br>• Tambahkan file `TASK.md` pada tiap folder dengan ID unik. | - [ ] Semua folder ter‑buat sesuai struktur yang tercantum di `docs/ARCHITECTURE.md`.<br>- [ ] Setiap folder memiliki `TASK.md` yang mengandung **ID**, **Goals**, **Verification Criteria**, **Status**.<br>- [ ] CI pipeline menjalankan lint atas semua `TASK.md` (cek format). | [ ] Pending |
---

## 2. Frontend (Next.js BFF)

| ID | Goals | Verification Criteria | Status |
|----|-------|-----------------------|--------|
| **TASK‑FE‑001** | • Setup proyek Next.js dengan TypeScript, Tailwind, ESLint, Prettier.<br>• Pastikan build dapat di‑run dalam Docker. | - [ ] `npm ci` selesai tanpa error.<br>- [ ] `npm run dev` men‑jalankan server pada `http://localhost:3000`.<br>- [ ] Dockerfile.frontend berhasil dibuild (`docker build -f Dockerfile.frontend .`).<br>- [ ] Lint (`npm run lint`) lulus. | [ ] Pending |
| **TASK‑FE‑002** | • Implementasi *pages* (Dashboard, Vendor Detail, Login, Error).<br>• Setiap halaman harus memiliki unit test dengan coverage ≥ 80 %. | - [ ] `tests/pages` berisi test untuk masing‑halaman.
- [ ] `npm test` menghasilkan coverage ≥ 80 %.
- [ ] Halaman men‑render tanpa error (cek via `curl` atau `Playwright`). | [ ] Pending |
| **TASK‑FE‑003** | • Buat komponen UI reusable (Button, Table, Modal, Card) dengan Storybook.
• Pastikan setiap komponen memiliki **snapshot test**. | - [ ] Storybook (`npm run storybook`) men‑jalankan semua cerita.
- [ ] Snapshot test lulus (`npm test`).
- [ ] Dokumentasi komponen di `frontend/src/components/README.md`. | [ ] Pending |
| **TASK‑FE‑004** | • Implementasi custom React hooks (`useAuth`, `useVendorData`). | - [ ] Unit test untuk setiap hook (< 90 % coverage).
- [ ] Hooks dapat dipakai di halaman tanpa menyebabkan memory leak. | [ ] Pending |
| **TASK‑FE‑005** | • Integrasi dengan backend API melalui `axios` interceptor yang men‑inject `X‑Request‑ID` dan token JWT. | - [ ] Semua request mengirim header `Authorization: Bearer <token>`.
- [ ] Interceptor men‑log request‑id ke console (dev). | [ ] Pending |
---

## 3. Backend (FastAPI Core Service)

| ID | Goals | Verification Criteria | Status |
|----|-------|-----------------------|--------|
| **TASK‑BE‑001** | • Setup FastAPI project dengan Pydantic, SQLAlchemy, Alembic, dan OPA integration.
• Pastikan semua dependensi tercantum di `pyproject.toml`. | - [ ] `pip install -r requirements.txt` selesai.
- [ ] `uvicorn backend.app.main:app --reload` berhasil start.
- [ ] OpenAPI docs (`/docs`) dapat diakses. | [ ] Pending |
| **TASK‑BE‑002** | • Definisikan ORM models & Pydantic schemas untuk `vendors`, `contracts`, `users`, `audit_log`.
• Terapkan **Row‑Level Security** (RLS) di PostgreSQL via migration. | - [ ] Migration `alembic upgrade head` berhasil.
- [ ] Unit test CRUD untuk setiap model (`pytest backend/tests/models`).
- [ ] RLS policies terbukti (test dengan dua user berbeda). | [ ] Pending |
| **TASK‑BE‑003** | • Implementasikan **service layer** (pure Python) untuk business logic (vendor CRUD, contract validation, audit). | - [ ] Setiap service memiliki unit test dengan coverage ≥ 90 %.
- [ ] Service dapat dipanggil tanpa FastAPI context (stand‑alone). | [ ] Pending |
| **TASK‑BE‑004** | • Buat **router API** (`backend/app/api/`) yang meng‑expose endpoint CRUD, auth, dan health.
• Pastikan semua endpoint mengembalikan response sesuai OpenAPI spec. | - [ ] `pytest backend/tests/api` lulus dan menghasilkan coverage ≥ 90 %.
- [ ] Response schema matches OpenAPI (checked via `fastapi-openapi-schema-validator`). | [ ] Pending |
| **TASK‑BE‑005** | • Integrasi **OPA / CASL** policy enforcement via middleware (`backend/app/middleware/opa_policy`). | - [ ] Policy decision `allow` → request proceeds.
- [ ] Decision `deny` → 403 response.
- [ ] Cache positive decisions 60 s (verified by mock OPA call count). | [ ] Pending |
| **TASK‑BE‑006** | **Modular Middleware Stack** (see detailed sub‑tasks `TASK‑BE‑006‑01` … `TASK‑BE‑006‑07`). | - Semua sub‑task (`TASK‑BE‑006‑0x`) berstatus **[x]**.
- End‑to‑end test `tests/middleware/test_full_stack.py` memverifikasi seluruh stack. | [ ] Pending |
| **TASK‑BE‑007** | • Buat **exception handling** terpusat (`backend/app/exceptions`) dengan kelas `AppError`, `AuthError`, dsb. | - [ ] Unit test memastikan konversi exception → HTTP status code.
- [ ] Semua endpoint menggunakan `raise AppError(...)` bila diperlukan. | [ ] Pending |
| **TASK‑BE‑008** | • Implementasi **dependency injection** (`backend/app/dependencies`) untuk DB session, Redis cache, dan JWT verifier. | - [ ] Middleware injects `request.state.db` dan `request.state.redis`.
- [ ] Test memastikan dependencies dapat dipanggil tanpa side‑effects. | [ ] Pending |
| **TASK‑BE‑009** | • Buat **schema / DTO** terpisah dari ORM (`backend/app/schemas`). | - [ ] Semua request/response menggunakan schema Pydantic yang tidak meng‑import SQLAlchemy.
- [ ] Unit test validasi schema (field types, constraints). | [ ] Pending |
| **TASK‑BE‑010** | • Buat **utils** (`backend/app/utils`) untuk pagination, datetime helper, UUID generator, error wrapper. | - [ ] Setiap util memiliki test coverage ≥ 90 %.
- [ ] Dokumentasi singkat di `backend/app/utils/README.md`. | [ ] Pending |
---

## 4. Infrastructure / DevOps

| ID | Goals | Verification Criteria | Status |
|----|-------|-----------------------|--------|
| **TASK‑DO‑001** | • Buat Dockerfile terpisah untuk **frontend**, **backend**, **postgres**, **opa** dengan multi‑stage build; ukuran image ≤ 300 MB. | - [ ] `docker build -f Dockerfile.frontend .` < 300 MB.
- [ ] `docker build -f Dockerfile.backend .` < 300 MB.
- [ ] Semua Dockerfile lulus lint dengan `hadolint`. | [ ] Pending |
| **TASK‑DO‑002** | • Definisikan **docker‑compose.yml** yang meng‑orchestrate semua service, health‑check, dan volume untuk Postgres. | - [ ] `docker compose up -d` men‑start semua container tanpa error.
- [ ] `docker compose ps` menunjukkan health status **healthy** untuk setiap service.
- [ ] Memungkinkan menjalankan *single* service (`docker compose up backend`). | [ ] Pending |
| **TASK‑DO‑003** | • Setup **GitHub Actions** workflow untuk lint, test, build Docker images, dan push ke registry. | - [ ] Workflow `ci.yml` men‑run pada setiap push ke `main`.
- [ ] Semua job lulus (lint, unit test, build image).
- [ ] Badge CI ditampilkan di `README.md`. | [ ] Pending |
| **TASK‑DO‑004** | • Konfigurasi **Prometheus** untuk scrape semua service (`frontend`, `backend`, `opa`, `postgres`). | - [ ] Prometheus berhasil meng‑scrape `/metrics` dari tiap service.
- [ ] Alert rule meng‑trigger ketika error‑rate > 1 % atau latency > 300 ms.
- [ ] Dashboard Grafana men‑display metric dengan benar. | [ ] Pending |
| **TASK‑DO‑005** | • Buat **backup & restore** script untuk PostgreSQL (`scripts/backup.sh`, `scripts/restore.sh`). | - [ ] Script menghasilkan file dump (`.sql`) dan menyimpannya ke volume backup.
- [ ] Restore script berhasil memulihkan data ke DB baru.
- [ ] CI menjalankan backup & restore pada database test. | [ ] Pending |
| **TASK‑DO‑006** | • Implementasi **audit‑log collector** (optional, bisa berupa side‑car container atau langsung log ke DB). | - [ ] Semua request backend menghasilkan entry di tabel `audit_log`.
- [ ] Log dapat di‑query dengan filter `user_id`, `path`, `date`. | [ ] Pending |
---

## 5. Documentation & Data

| ID | Goals | Verification Criteria | Status |
|----|-------|-----------------------|--------|
| **TASK‑DOC‑001** | • Buat **README.md**, **ARCHITECTURE.md**, **PRD.md**, **DESIGN.md**, **CLAUDE.md** dengan link lintas‑referensi. | - [ ] Semua dokumen berada di folder `docs/`.
- [ ] `mkdocs build` menghasilkan site tanpa error.
- [ ] Link antar dokumen berfungsi (klik‑able). | [ ] Pending |
| **TASK‑DATA‑001** | • Siapkan seed data (`data/seed/`) yang mengikuti standar kualitas DAMA‑DMBOK (unik, valid, lineage). | - [ ] Script `scripts/init_db.sh` meng‑import seed data ke DB.
- [ ] Validasi data (unik vendor_id, email format) lulus.
- [ ] Dokumentasi lineage (`docs/DATA_LINEAGE.md`) ada. | [ ] Pending |
---

## 6. Automation of Status Updates

| ID | Goals | Verification Criteria | Status |
|----|-------|-----------------------|--------|
| **TASK‑AUT‑001** | • Buat skrip Python `scripts/update_task_status.py` yang membaca file `TASK.md`, memeriksa semua **Verification Criteria** (menggunakan output JSON dari CI), dan mengganti `[ ]` menjadi `[x]` bila terpenuhi. | - [ ] Skrip dijalankan sebagai langkah akhir dalam workflow CI (`after_success`).
- [ ] Skrip dapat men‑update file di repository (commit & push) secara aman.
- [ ] Log output men‑show task yang di‑update. | [ ] Pending |
| **TASK‑AUT‑002** | • Tambahkan hook ke GitHub Actions untuk **auto‑label** PR ketika semua top‑level tasks (`TASK‑PRJ‑001`, `TASK‑FE‑001`, `TASK‑BE‑001`, `TASK‑DO‑001`, `TASK‑DOC‑001`) sudah `[x]`. | - [ ] Workflow mem‑parse `TASK.md` dan men‑assign label `ready‑for‑release` bila semua header `[ ]` sudah berubah menjadi `[x]`. | [ ] Pending |
---

## 7. Acceptance & Release Checklist (Final Verification)

| ID | Goals | Verification Criteria | Status |
|----|-------|-----------------------|--------|
| **TASK‑REL‑001** | **Release readiness** – semua top‑level tasks harus `[x]`. | - [ ] Semua baris `Status` pada tabel di atas berstatus **[x]**.
- [ ] Laporan CI men‑show 100 % pass pada semua job.
- [ ] Deploy ke **staging** berhasil (docker‑compose up –env staging) tanpa error.
- [ ] Smoke test (cURL health endpoints) lulus. | [ ] Pending |

---

### Cara kerja otomatisasi status
1. **Setiap unit test** men‑output file `test_results.json` berisi mapping task‑id → `passed:true/false`.
2. **GitHub Action** `after_success` menjalankan `scripts/update_task_status.py` yang:
   - Membaca `test_results.json`.
   - Membuka `TASK.md`.
   - Mengganti `[ ]` menjadi `[x]` pada baris criteria yang `passed:true`.
   - Jika semua criteria pada sebuah *task* telah `[x]`, mengubah status header tugas menjadi `[x]`.
3. Skrip melakukan **commit** perubahan ke repo (push otomatis) sehingga file `TASK.md` selalu mencerminkan **status terkini**.

---

### Ringkasan
- **Master TASK.md** memuat seluruh ruang lingkup proyek SIGAP (setup, frontend, backend, infra, docs, data, automation, release).
- Setiap sub‑task memiliki **ID unik**, **Goals**, **Verification Criteria**, dan **Status**.
- **Automation** dengan skrip yang dijalankan di CI memastikan checklist ter‑update secara real‑time ketika semua kriteria verifikasi terpenuhi.
- Dengan pendekatan ini, tidak ada lagi "missed task"; seluruh tim dapat melihat progres terkini hanya dengan membuka file `TASK.md` di repository.

---

*Silakan sinkronkan file ini ke repository Anda; CI pipeline harus di‑update untuk menjalankan `scripts/update_task_status.py` pada tiap build.*