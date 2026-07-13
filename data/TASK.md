# TASK.md – Data

## Goals
- Store **seed data** (JSON/CSV) for development and automated tests.
- Ensure data follows **DAMA‑DMBOK** quality dimensions (accuracy, completeness, consistency).
- Provide **data‑lineage** documentation that shows source → transformation → destination.

## Verification Criteria
- [] `data/seed/vendors.json` & `contracts.json` berisi minimal 10 contoh records dengan field lengkap.
- [] Script `scripts/init_db.sh` dapat import seed data ke PostgreSQL (via `psql -c "COPY ... FROM STDIN CSV"`).
- [] Data validator (`python -m jsonschema`) runs in CI and passes.
- [] Dokumentasi lineage (`docs/DATA_LINEAGE.md`) menjelaskan proses ETL.
- [] CI men‑run data validation dan gagal bila schema tidak cocok.

## Status
- [ ] Pending
