# SIGAP: Sistem Integrasi Gizi & Akuntabilitas Pangan

[![Status](https://img.shields.io/badge/status-development-yellow.svg)]()
[![Architecture](https://img.shields.io/badge/architecture-Modular_Monolith-blue.svg)]()
[![Security](https://img.shields.io/badge/security-RLS_&_OPA-red.svg)]()

SIGAP is an enterprise-grade vendor governance platform for the **Makan Bergizi Gratis (MBG)** program, designed to ensure end-to-end transparency, data integrity, and strict accountability in food distribution.

## 🏛️ System Architecture
SIGAP leverages a **Modular Monolith** pattern with strict domain boundaries, balancing developer velocity with the robustness of a distributed system.

*   **Frontend (BFF)**: Next.js (App Router, Server Actions, TypeScript).
*   **Core Backend**: FastAPI (Domain-Driven Design, Async Workers).
*   **Data Persistence**: PostgreSQL 15+ (PostGIS for Geospatial, pgcrypto for PII).
*   **Security & Policy**: Row-Level Security (RLS) and Open Policy Agent (OPA) for ABAC.

---

## 📂 Project Structure
```text
comming soon
```

---

## 🔒 Governance & Security
SIGAP is strictly compliant with **Satu Data Indonesia (SDI)**, **UU PDP 27/2022**, and **DAMA-DMBOK** standards.

1.  **Data Isolation**: PostgreSQL **Row-Level Security (RLS)** is enforced at the database level using `current_scope` for regional isolation.
2.  **PII Privacy**: All sensitive data (NIK, Phone, Email) is encrypted with **AES-256 (pgcrypto)** at rest and masked at the BFF layer.
3.  **Accountability**: Every `POST/PATCH/DELETE` operation triggers an automated, immutable audit log.
4.  **Access Control**: ABAC is managed via **Open Policy Agent (OPA)** for complex regional scope validation.
5.  **Data Integrity**: Geospatial validation uses **PostGIS** `ST_DWithin` to ensure report authenticity.

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ & Python 3.11+
- PostgreSQL 15+ (with `pgcrypto`, `uuid-ossp`, `postgis`)
- Redis (for Async Workers)
- OPA Service

### Initial Setup
1. **Initialize Database**:
   ```bash
   psql -U <db_user> -d sigap_db -f C:\SIGAP\migrations\001_init_schema.sql
   ```

2. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

---

## 🤖 Development Protocol
This project utilizes a strict AI-Agent protocol (`AGENTS.md`). All code contributions **must** adhere to:
- **Contract-First**: Update `api-contract.yaml` before implementation.
- **Security-First**: Never bypass RLS or leak PII.
- **Verification**: Every feature must include automated tests and audit logs.

---
*SIGAP Engineering Team © 2026*
