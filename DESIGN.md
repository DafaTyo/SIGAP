# DESIGN.md - Technical Design Specification: SIGAP

## 1. Architecture Overview
SIGAP adopts a **Modular Monolith** architecture to ensure high developer velocity while maintaining strict domain boundaries.

### 1.1 Logical Layers
- **Presentation Layer (Next.js)**: Handles UI/UX and client-side logic.
- **BFF Layer (Next.js Server Actions)**: Orchestrates requests to the Core API, handles SSR data fetching, and provides an additional security layer (PII Masking).
- **Service Layer (FastAPI)**: Implements domain-specific business logic.
- **Domain Modules**: `Vendor`, `Distribution`, `Complaint`. Each has its own schemas, models, and services.
- **Infrastructure Layer**: PostgreSQL (Persistence), Redis (Cache/Queue), OPA (AuthZ).

---

## 2. Security Architecture (The Core Pillar)

### 2.1 PostgreSQL Row Level Security (RLS)
To prevent data leakage between regions/provinces, RLS is enforced at the DB level.
- **Implementation**: Every connection from FastAPI sets a local variable: `SET LOCAL app.current_user_id = '<uuid>'; SET LOCAL app.current_scope = '<province_id>';`.
- **Policies**: Queries automatically filter by `scope_id` or `user_id` based on the active session.

### 2.2 AuthZ: OPA & CASL
- **OPA (Open Policy Agent)**: Centralized policy engine for complex ABAC rules (e.g., "Only Pengawas of Province A can verify Vendors in Province A").
- **CASL (BFF Layer)**: Synchronizes permissions to the frontend for UI element toggling (Read/Write/Delete).

### 2.3 PII Masking & Data Privacy
- **Masking Engine**: A utility class in the BFF layer that identifies sensitive fields (NIK, Phone) and applies `####-####-1234` masking based on the user's role.
- **Audit Logging**: A global FastAPI middleware that captures every mutation, storing the delta (diff) in a JSONB column for full accountability.

---

## 3. Data Strategy

### 3.1 Persistence (PostgreSQL + PostGIS)
- **Geospatial**: PostGIS is used for the `Distribution` module to validate if a vendor's reported coordinates fall within a valid school radius.
- **Idempotency Table**: Stores `idempotency_key` and its associated response for 24 hours to prevent duplicate state changes.

### 3.2 Asynchronous Processing (Redis + Workers)
- **Pattern**: Fire-and-Forget with Polling.
- **Use Cases**:
    - **OSS/BPOM Validation**: External API calls are pushed to a Redis queue to avoid blocking the user.
    - **AI Anomaly Detection**: Distribution reports are analyzed by a Python worker using a probabilistic model.

---

## 4. Module Boundaries

### 4.1 Vendor Module
- **Core Entities**: `Vendor`, `LegalDocument`, `SIODigital`.
- **Inbound**: Registrations, Document Uploads.
- **Outbound**: Verified status, QR SIO.

### 4.2 Distribution Module
- **Core Entities**: `DistributionReport`, `AnomalyFlag`, `VendorScore`.
- **Dependencies**: Uses `Vendor` data for validation.
- **AI Integration**: Triggers AI scoring for every new report.

### 4.3 Complaint Module
- **Core Entities**: `Complaint`, `Ticket`, `ResolutionNote`.
- **Public Access**: Ticket-based access for non-authenticated users.

---

## 5. Trade-offs & Decisions (ADR)
- **Decision**: Modular Monolith over Microservices.
  - *Reasoning*: Lower operational overhead for MVP while allowing easy decoupling of the `AI Engine` or `Public Portal` later.
- **Decision**: Next.js Server Actions for BFF.
  - *Reasoning*: Reduces the need for a separate BFF server and provides type safety from UI to API.
- **Decision**: DB-level RLS over Application-level filtering.
  - *Reasoning*: Provides a fail-safe security layer even if application logic has bugs.

---

## 6. Implementation Checklist
- [ ] Setup PostgreSQL with RLS and PostGIS extension.
- [ ] Configure OPA sidecar/service for policy evaluation.
- [ ] Implement `X-Idempotency-Key` middleware.
- [ ] Build the PII Masking utility in the Next.js layer.
- [ ] Setup Redis for background job orchestration.
