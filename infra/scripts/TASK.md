# TASK.md – Infra/scripts

## Goals
- Provide utility scripts for **deployment**, **backup**, **restore**, **health‑check**, and **environment bootstrap**.
- Scripts must be **POSIX‑compatible** (bash) and work on Windows Git‑Bash as well as Linux CI runners.

## Verification Criteria
- [] `scripts/deploy.sh` builds Docker images, tags with `git rev-parse --short HEAD`, and pushes to registry (Docker Hub / GHCR).
- [] `scripts/backup.sh` runs `pg_dump` and stores dump in `backups/` with timestamped filename.
- [] `scripts/restore.sh` can restore a dump into a fresh PostgreSQL container.
- [] `scripts/healthcheck.sh` curls `/health` endpoint of each service and exits 0 only if all are healthy.
- [] CI runs `bash scripts/healthcheck.sh` after `docker compose up` to ensure all services start correctly.
- [] All scripts have shebang (`#!/usr/bin/env bash`) and exit with non‑zero code on failure.

## Status
- [ ] Pending
