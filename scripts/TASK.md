# TASK.md – Scripts (root)

## Goals
- Central repository for **project‑wide utility scripts** not tied to a specific service.
- Include scripts for **repo initialization**, **code formatting**, **dependency checks**, and **environment validation**.

## Verification Criteria
- [] `scripts/init_repo.sh` creates virtual environment, installs deps (`pip install -r requirements.txt`), and runs `pre‑commit install`.
- [] `scripts/format_code.sh` runs `black .`, `isort .`, `eslint .` and exits with 0 only if no changes were needed.
- [] `scripts/check_env.sh` validates required env vars (`DB_URL`, `OPA_URL`, `JWT_SECRET`) are present; fails with clear message otherwise.
- [] All scripts contain shebang, `set -euo pipefail`, and return non‑zero on error.
- [] CI runs these scripts as part of `pre‑test` stage.

## Status
- [ ] Pending
