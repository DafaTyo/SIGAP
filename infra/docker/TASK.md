# 📌 Module Task Tracker: Infra Docker (infra/docker)

## 🎯 Core Objective & Responsibility
- Menyediakan **Dockerfile** dan **docker‑compose.yml** untuk membangun dan menjalankan seluruh stack SIGAP (backend, frontend, Postgres, Redis, OPA, Prometheus, Grafana).
- Menjamin semua layanan dapat berkomunikasi via jaringan Docker internal.

## 📋 Development Checklist
- [ ] **Package init** – `README.md` dengan langkah build/run.
- [ ] **Dockerfile for Backend** – `backend.Dockerfile`
  - Base image: `python:3.11-slim`
  - Install dependencies (`pip install -r requirements.txt`).
  - Copy `backend/` code, set `WORKDIR /app`.
  - Expose port `8000`.
- [ ] **Dockerfile for Frontend** – `frontend.Dockerfile`
  - Base image: `node:20-alpine`
  - Install deps, build (`npm run build`).
  - Use `nginx` stage to serve static files.
- [ ] **docker-compose.yml** (root of `infra/docker`)
  - Services: `backend`, `frontend`, `postgres`, `redis`, `opa`, `prometheus`, `grafana`.
  - Define env vars (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `DATABASE_URL`, `REDIS_URL`, `OPA_URL`).
  - Networks: `sigap_net`.
  - Volumes: `pg_data`, `redis_data`.
- [ ] **Healthcheck scripts** – `healthcheck.sh` untuk backend (curl /health) dan DB (pg_isready).
- [ ] **Write Infra Docker README** – langkah build images, `docker compose up -d`, akses UI (`localhost:3000`), API (`localhost:8000`).

## 🔒 Constraints & Best Practices
- **Multi‑stage builds** untuk frontend to keep image size < 150 MB.
- **Least privilege:** run containers as non‑root user (`USER node` for frontend, `USER app` for backend).
- **Secret handling:** tidak hard‑code credentials; gunakan `.env` file (excluded from git).
- **Logging:** send logs to stdout/stderr, let Docker capture.

## 📄 References
- `docs/DESIGN.md` – diagram deployment.
- `api-contract.yaml` – port dan base path (`/v1`).

---

**Instruksi Eksplisit:** Tidak ada Dockerfile atau compose file yang boleh ditulis sampai semua poin checklist di atas ditandai selesai.
