# TASK.md – Infra/docker-compose.yml

## Goals
- Define Docker‑Compose file that brings up **frontend**, **backend**, **postgres**, **opa**, **prometheus**, **grafana**.
- Use internal network `sigap_net`, persistent volume `pg_data`, and health‑checks for each service.
- Enable **environment variable interpolation** for secrets (DB_PASSWORD, JWT_SECRET) via `.env`.

## Verification Criteria
- [] `docker compose up -d` starts all containers without error.
- [] `docker compose ps` shows health status `healthy` for each service.
- [] Services can communicate using service names (`frontend` → `backend`, `backend` → `postgres`).
- [] CI pipeline runs `docker compose config` (validate) and `docker compose up -d` (smoke test) then shuts down.

## Status
- [ ] Pending
