# SIGAP - Sistem Integrasi Gizi & Akuntabilitas Pangan

Proyek ini menggunakan arsitektur **Modular Monolith** dengan tech stack:
- **Frontend / BFF (Backend-for-Frontend)**: Next.js 16.x (App Router, Server Components)
- **Backend API**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL dengan PostGIS (Geo-spatial) & Row-Level Security (RLS)
- **Otorisasi / RBAC**: OPA (Open Policy Agent) / Rego
- **AI / LLM Layer**: Local LLM Service (GGUF/GPTQ), dipisah sebagai microservice internal
- **Infrastruktur**: Docker, Kubernetes, Redis, MinIO

## Struktur Folder

```text
SIGAP/
├── docs/                      # Dokumentasi proyek (ADR, ERD, API Contract, dsb)
│   ├── adr/                   # Architecture Decision Records
│   └── api/                   # API contracts (termasuk api-contract.yaml)
├── policies/                  # File kebijakan OPA (Rego) untuk RBAC/ABAC
├── scripts/                   # Skrip utilitas (database migration, seeding, deployment)
├── src/                       # Source Code Utama
│   ├── backend/               # Backend API Server (FastAPI)
│   │   ├── app/
│   │   │   ├── api/           # Router & Endpoints (v1)
│   │   │   │   └── v1/        # Routing per modul (auth, vendor, distribution, dll)
│   │   │   ├── core/          # Konfigurasi, Security, Exceptions, Dependencies
│   │   │   ├── db/            # Database engine, session, migrations (Alembic)
│   │   │   ├── models/        # SQLAlchemy ORM Models
│   │   │   ├── schemas/       # Pydantic Models (Validasi I/O)
│   │   │   └── services/      # Business Logic (CRUD, panggil external API)
│   │   ├── tests/             # Pytest Backend
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── frontend/              # Web Client & BFF (Next.js 16)
│   │   ├── app/               # App Router (Pages, Layouts, Server Actions)
│   │   ├── components/        # UI Components (React)
│   │   ├── lib/               # Utility functions, API clients, Session management
│   │   ├── public/            # Static assets (images, icons)
│   │   ├── styles/            # Tailwind CSS / Global styles
│   │   ├── Dockerfile
│   │   └── package.json
│   │
│   └── llm_service/           # (Opsional) Service terpisah untuk Local LLM Inference
│       ├── app/               # Logic untuk inferensi, Guardrails, & RAG
│       ├── models/            # Folder menyimpan bobot LLM (.gguf)
│       └── Dockerfile
├── docker-compose.yml         # Orkestrasi lokal (DB, Redis, OPA, Backend, Frontend)
├── .env.example               # Contoh environment variables
└── README.md
```
