# 📌 Module Task Tracker: Infra Scripts (infra/scripts)

## 🎯 Core Objective & Responsibility
- Menyediakan **script automation** untuk setup, migrasi database, health‑check, dan deployment ke environment staging/production.
- Semua script ditulis dalam **bash** (POSIX compatible) untuk Linux‑based container runtime.

## 📋 Development Checklist
- [ ] **Package init** – `README.md` dengan deskripsi tiap script.
- [ ] **bootstrap.sh** – men‑setup Docker network, pull images, dan `docker compose up -d`.
- [ ] **migrate.sh** – menjalankan Alembic migrations (`alembic upgrade head`).
- [ ] **healthcheck.sh** – curl `/health` endpoint backend, return exit code 0/1.
- [ ] **seed.sh** – load seed data JSON ke DB via FastAPI endpoint (`/admin/seed`).
- [ ] **deploy.sh** – wrapper untuk production deploy (docker compose pull, down, up). 
- [ ] **Write Scripts README** – contoh pemanggilan, requirement (bash, docker), dan troubleshooting.

## 🔒 Constraints & Best Practices
- **Idempotent:** tiap script dapat dijalankan berulang kali tanpa menimbulkan duplikasi.
- **Error handling:** `set -euo pipefail`; output log ke stdout.
- **Permissions:** file mode `0755`.
- **Testing:** unit‑test bash scripts dengan `bats` (optional).

## 📄 References
- `infra/docker/TASK.md` – definisi layanan yang akan dijalankan.
- `docs/DESIGN.md` – deployment diagram.

---

**Instruksi Eksplisit:** Tidak menulis script apapun sebelum semua checklist di atas di‑centang selesai.
