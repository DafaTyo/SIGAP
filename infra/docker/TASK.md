# TASK.md – Infra/docker

## Goals
- Write **multi‑stage Dockerfiles** untuk setiap service (frontend, backend, db, opa).
- Set ukuran image < 300 MB masing‑masing, gunakan **alpine** atau **distroless** pada stage akhir.
- Pastikan Dockerfile memuat **health‑check** (`CMD curl -f http://localhost:8000/health || exit 1`).

## Verification Criteria
- [] `docker build -f Dockerfile.frontend .` selesai dalam < 5 min, image size < 300 MB.
- [] `docker build -f Dockerfile.backend .` selesai dalam < 5 min, size < 300 MB.
- [] Health‑check ter‑define di masing‑Dockerfile (Dockerfile `HEALTHCHECK`).
- [] CI (`ci.yml`) menjalankan `docker build` untuk semua Dockerfile dan gagal bila build error atau size > 300 MB.

## Status
- [ ] Pending
