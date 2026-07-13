# TASK.md – Infra/.github/workflows

## Goals
- Buat GitHub Actions workflow untuk lint, test, dan build Docker images.
- Pastikan pipeline memicu pada push ke `main` dan pull‑request.

## Verification Criteria
- [] Workflow `lint.yml` menjalankan ESLint & flake8 tanpa error.
- [] Workflow `ci.yml` menjalankan semua unit test (`npm test`, `pytest`).
- [] Docker images dibangun dan di‑push ke registry (opsional).
- [] Badge status tampil di README.

## Status
- [] Pending