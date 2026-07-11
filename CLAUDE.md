# CLAUDE.md - SIGAP Project Guidelines

## 🏗️ Architecture: Modular Monolith
SIGAP is built as a **Modular Monolith** to balance simplicity with strict domain boundaries.
- **Frontend / BFF**: Next.js (App Router, Tailwind, TypeScript). Handles UI and lightweight orchestration.
- **Core Backend**: Python (FastAPI). Handles complex business logic, async workers, and external integrations.
- **Database**: PostgreSQL with **Row Level Security (RLS)** for multi-tenant/scope isolation.
- **AuthZ**: OPA (Open Policy Agent) / CASL for advanced Attribute-Based Access Control (ABAC).

## 💻 Tech Stack Specifics
- **Web**: Next.js 14+ (Server Actions for BFF).
- **API**: FastAPI (Pydantic v2, SQLAlchemy 2.0 / Tortoise ORM).
- **Security**: 
  - PostgreSQL RLS: Every query must run under a session with `app.current_user_id` and `app.current_scope`.
  - PII Masking: NIK/Names must be masked at the application layer before reaching non-admin roles.
- **Async**: Redis + ARQ/Celery for OSS Validation & AI Anomaly Detection.

## 🛠️ Build & Run Commands
### Frontend (Next.js)
- Install: `npm install`
- Dev: `npm run dev`
- Build: `npm run build`
- Lint: `npm run lint`

### Backend (FastAPI)
- Install: `pip install -r requirements.txt` (or `uv sync`)
- Dev: `uvicorn main:app --reload`
- Migrations: `alembic upgrade head`
- Test: `pytest`

## 📏 Coding Standards
### General
- **Indonesian Communication**: AI Assistant responds in Indonesian. Code/Comments in English.
- **Idempotency**: All `POST` state-changing requests MUST support `X-Idempotency-Key`.
- **Audit Trail**: Every mutation MUST be logged to `audit_logs` table (Actor, Entity, Diff).

### Python (FastAPI)
- Follow **Domain-Driven Design (DDD)** folders: `app/modules/[vendor|distribution|complaint]`.
- Use **Dependencies** for Auth and RLS context.
- Probabilistic AI: Anomaly results must return `score: float`, `confidence: float`, and `flag: enum`.

### TypeScript (Next.js)
- Use **Server Actions** for form submissions.
- Strictly type all API responses using shared types or generated OpenAPI clients.

## 🔒 Security & Data Rules
1. **PII Masking Rule**: Only `verifikator_bgn` and `admin` see full NIK. Others see `3175********1234`.
2. **Geospatial**: Distribution reports must have `latitude` and `longitude`. Validated via PostGIS.
3. **ABAC**: Scope is defined by `province` or `kabupaten_kota`. Pengawas only see their scope.
4. **RLS Policy**: No query should be executed without a tenant/user context in the DB session.

## 🧪 Testing Requirements
- Backend: Min. 80% coverage on core modules.
- Integration: Test the async validation flow (Mock OSS API).
- Security: Test RLS bypass attempts and ABAC scope leaks.
