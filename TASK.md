# TASK.md – Master To‑Do List (Project SIGAP)

## Project Overview
- **Nama**: SIGAP (Sistem Informasi Governance Vendor – MBG Program)
- **Arsitektur**: Modular‑Monolith – Frontend (Next.js BFF) + Backend (FastAPI) + PostgreSQL RLS + OPA/CASL (ABAC)
- **Standar**: DAMA‑DMBOK, Satu Data Indonesia, keamanan OWASP, CI/CD lint‑test‑build, audit‑logging, observability (Prometheus/Grafana).

## Goal Categories (ID Prefix)
- Frontend: `TASK‑FE‑###`
- Backend: `TASK‑BE‑###`
- DevOps / Infra: `TASK‑DO‑###`
- Quality Assurance: `TASK‑QA‑###`
- Data / Database: `TASK‑DB‑###`

## Master Checklist
| ID | Ringkasan | Goals | Verification Criteria | Status |
|----|-----------|-------|-----------------------|--------|
| **TASK‑FE‑001** | **Setup Frontend project** | • Initialise Next.js monorepo, TypeScript, ESLint, Prettier, Tailwind | • `[ ]` `npm ci` berhasil, lint‑free, build sukses (`next build`). | `[ ]` |
| **TASK‑BE‑001** | **Setup Backend skeleton** | • Initialise FastAPI app, pyproject, alembic, OPA integration | • `[ ]` `uvicorn` start, migration success, lint‑free (`flake8`). | `[ ]` |
| **TASK‑DO‑001** | **Provision Infra (Docker‑Compose)** | • Define services, health‑checks, persistent volumes | • `[ ]` `docker compose up -d` runs without error, all health‑checks pass. | `[ ]` |
| **TASK‑QA‑001** | **Testing & Coverage** | • Unit, integration, e2e, coverage ≥ 80 % (FE) / 90 % (BE) | • `[ ]` CI fails when coverage below threshold. | `[ ]` |
| **TASK‑DB‑001** | **Database schema & RLS** | • Design tables, apply Row‑Level Security, audit trail | • `[ ]` Alembic migrations apply, RLS policies enforce per‑tenant. | `[ ]` |

*Setiap sub‑folder memiliki `TASK.md` spesifik yang mendetailkan poin‑poin di atas.*

---

### Cara Menggunakan
1. Buka `TASK.md` di folder yang bersangkutan.
2. Centang checklist (`[x]`) hanya setelah **Verification Criteria** seluruhnya terpenuhi.
3. CI/CD akan otomatis memeriksa coverage & lint sebelum mengizinkan merge.

---

*File ini berada di `C:\SIGAP\TASK.md`.*