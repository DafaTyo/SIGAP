# TASK.md – Master To‑Do List untuk SIGAP

---

## Frontend (`TASK-FE-###`)

| ID | Ringkasan | Goals | Verification Criteria | Status |
|----|-----------|-------|-----------------------|--------|
| **TASK‑FE‑001** | **Setup UI project (Next.js)** | • Inisialisasi monorepo Frontend dengan Next.js 14<br>• Konfigurasi TypeScript, ESLint, Prettier | • `[ ]` `npm init` berhasil<br>• `[ ]` `next build` lint‑free<br>• `[ ]` CI pipeline lulus lint step | `[ ]` |
| **TASK‑FE‑002** | **Desain halaman Dashboard Vendor** | • Membuat layout responsif untuk menampilkan data vendor (list, detail, filter)<br>• Integrasi dengan API BFF | • `[ ]` Halaman menampilkan tabel vendor<br>• `[ ]` Responsif pada *mobile* (≤ 576 px)<br>• `[ ]` Mock data ter‑render dengan benar | `[ ]` |
| **TASK‑FE‑003** | **Implementasi autentikasi UI (OAuth2 / OIDC)** | • Login/Logout UI yang terhubung ke FastAPI Auth<br>• Penyimpanan token aman (http‑only, same‑site) | • `[ ]` Form login muncul<br>• `[ ]` Token disimpan di cookie & diperbaharui otomatis<br>• `[ ]` Akses endpoint yang dilindungi berhasil | `[ ]` |

---

## Backend (`TASK-BE-###`)

| ID | Ringkasan | Goals | Verification Criteria | Status |
|----|-----------|-------|-----------------------|--------|
| **TASK‑BE‑001** | **Setup FastAPI project skeleton** | • Buat struktur paket (`app/`, `api/`, `core/`)<br>• Konfigurasi Pydantic settings, logging, dan dependensi | • `[ ]` `uvicorn` dapat dijalankan<br>• `[ ]` Unit test starter (`pytest`) berhasil<br>• `[ ]` Dockerfile build success | `[ ]` |
| **TASK‑BE‑002** | **Implementasi endpoint CRUD Vendor** | • API RESTful untuk `GET /vendors`, `POST`, `PUT`, `DELETE`<br>• Validasi dengan Pydantic schema | • `[ ]` Semua endpoint mengembalikan **200/201/204** sesuai aksi<br>• `[ ]` Validasi error handling (400, 404) tercakup<br>• `[ ]` Dokumentasi OpenAPI otomatis ter‑generate | `[ ]` |
| **TASK‑BE‑003** | **Integrasi OPA / CASL untuk ABAC** | • Aturan kebijakan untuk kontrol akses per‑peran dan per‑tenant<br>• Middleware FastAPI yang mengecek policy | • `[ ]` Policy file (`policy.rego`) ter‑load<br>• `[ ]` Request yang tidak berizin mengembalikan **403**<br>• `[ ]` Unit test policy coverage ≥ 90 % | `[ ]` |

---

## DevOps & Infrastruktur (`TASK-DO-###`)

| ID | Ringkasan | Goals | Verification Criteria | Status |
|----|-----------|-------|-----------------------|--------|
| **TASK‑DO‑001** | **Provisioning environment dengan Docker Compose** | • Semua service (frontend, backend, postgres, opa) dapat dijalankan secara lokal | • `[ ]` `docker compose up -d` selesai tanpa error<br>• `[ ]` Health‑check untuk tiap service lulus<br>• `[ ]` Data persisten (PostgreSQL volume) berfungsi | `[ ]` |
| **TASK‑DO‑002** | **CI/CD pipeline (GitHub Actions)** | • Build, test, dan deploy otomatis ke staging environment | • `[ ]` Workflow `build.yml` lulus lint & test<br>• `[ ]` Deploy ke Heroku/Render berhasil (verifikasi URL)<br>• `[ ]` Badge status muncul di README | `[ ]` |
| **TASK‑DO‑003** | **Observability (Prometheus + Grafana)** | • Monitoring metrik aplikasi, alert untuk error rate > 1 % | • `[ ]` Prometheus scrapes semua endpoint<br>• `[ ]` Dashboard Grafana menampilkan request latency<br>• `[ ]` Alert rule ter‑trigger pada simulasi error | `[ ]` |

---

## Quality Assurance (`TASK-QA-###`)

| ID | Ringkasan | Goals | Verification Criteria | Status |
|----|-----------|-------|-----------------------|--------|
| **TASK‑QA‑001** | **Testing strategy & coverage** | • Definisikan unit, integration, dan end‑to‑end test suite | • `[ ]` `pytest --cov=app` ≥ 80 % coverage<br>• `[ ]` CI menolak PR bila coverage < 80 %<br>• `[ ]` Dokumentasi testing strategy ada di `TESTING.md` | `[ ]` |
| **TASK‑QA‑002** | **Static analysis & linting** | • Enforce code quality dengan `flake8`, `black`, `isort` | • `[ ]` Semua commit melewati pre‑commit hook<br>• `[ ]` Linting error = 0 pada pipeline CI<br>• `[ ]` Laporan lint tersimpan sebagai artifact | `[ ]` |
| **TASK‑QA‑003** | **Performance testing (Load / Stress)** | • Simulasi beban 200 concurrent users pada endpoint vendor list | • `[ ]` Response time ≤ 300 ms pada 95 % request<br>• `[ ]` No memory leak after 1 h run<br>• `[ ]` Hasil laporan (`k6` atau `locust`) disimpan di `reports/` | `[ ]` |

---

## Database / Data (`TASK-DB-###`)

| ID | Ringkasan | Goals | Verification Criteria | Status |
|----|-----------|-------|-----------------------|--------|
| **TASK‑DB‑001** | **Schema design & migrations (Alembic)** | • Definisikan tabel `vendors`, `contracts`, `users` dengan RLS policies | • `[ ]` Migration script berhasil `alembic upgrade head`<br>• `[ ]` RLS policy memfilter data per‑tenant<br>• `[ ]` ER diagram tersimpan di `docs/ERD.png` | `[ ]` |
| **TASK‑DB‑002** | **Data governance (DAMA‑DMBOK)** | • Implementasi data lineage, katalog, dan audit trail | • `[ ]` Tabel audit (`vendor_audit`) ter‑isi otomatis via trigger<br>• `[ ]` Data quality rules (unik vendor_id, email format) ter‑enforced<br>• `[ ]` Dokumentasi data governance ada di `GOVERNANCE.md` | `[ ]` |
| **TASK‑DB‑003** | **Backup & restore strategy** | • Jadwalkan nightly backup, tes restore otomatis | • `[ ]` Backup script (`pg_dump`) berjalan via cron<br>• `[ ]` Restore test berhasil pada environment staging<br>• `[ ]` Retention policy (30 days) ter‑verifikasi | `[ ]` |

---

### Cara Membaca & Memperbarui ✅

1. **Status Header** – `[ ]` = Pending, `[/]` = In Progress, `[x]` = Completed.  
2. **Verification Criteria** – centang (`[x]`) hanya bila kriteria sudah terpenuhi secara terukur (unit test lulus, build sukses, dll.).  
3. **Automasi** – ketika *semua* criteria dalam sebuah tugas ber‑centang `[x]`, ubah status header menjadi `[x]` secara manual atau melalui skrip CI yang meng‑update file ini.

*(File `TASK.md` kini berada di repositori `C:\SIGAP\` dan dapat di‑track dengan Git untuk kolaborasi.)*