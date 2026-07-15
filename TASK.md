# 📌 Module Task Tracker: Root (Root TASK.md)

## 🎯 Overall Objective & Guidance
- Menyiapkan **struktur folder** proyek SIGAP secara lengkap dan bersih serta menyediakan *task tracker* yang sangat detail pada tiap level.
- **Tidak ada kode program** (Python, JavaScript, TypeScript, dll.) yang boleh ditulis sebelum **semua checklist** dalam file‑file `TASK.md` ini ditandai selesai (`[x]`).
- Instruksi ini bersifat **final gating** – tim pengembang hanya dapat melanjutkan ke fase implementasi ketika setiap item di‑checklist di atas memiliki tanda selesai.

## 📂 High‑Level Folder Checklist (already completed)
- [x] `backend/` (core, domains, api, middleware, dependencies, exceptions, utils, policies, tests)
- [x] `backend/workers/validate_documents/`
- [x] `frontend/public/`
- [x] `frontend/src/components/`
- [x] `frontend/src/hooks/`
- [x] `frontend/src/actions/`
- [x] `frontend/src/utils/`
- [x] `frontend/src/styles/`
- [x] `frontend/src/tests/`
- [x] `infra/docker/`
- [x] `infra/prometheus/`
- [x] `infra/grafana/`
- [x] `infra/scripts/`
- [x] `data/seeds/`
- [x] `data/migrations/`
- [x] `docs/` (existing, no code files)

## 📋 Final Gate Checklist (must be **checked** before any code can be written)
- [ ] **Backend Core** – `backend/app/core/TASK.md` completed.
- [ ] **Backend Domains** – Vendor, Distribution, Complaint `TASK.md` files completed.
- [ ] **Backend API Router** – `backend/app/api/TASK.md` completed.
- [ ] **Backend Middleware** – `backend/app/middleware/TASK.md` completed.
- [ ] **Backend Dependencies** – `backend/app/dependencies/TASK.md` completed.
- [ ] **Backend Exceptions** – `backend/app/exceptions/TASK.md` completed.
- [ ] **Backend Utils** – `backend/app/utils/TASK.md` completed.
- [ ] **Backend Policies** – `backend/app/policies/TASK.md` completed.
- [ ] **Backend Tests** – `backend/app/tests/TASK.md` completed.
- [ ] **Backend Workers** – `backend/workers/validate_documents/TASK.md` completed.
- [ ] **Frontend Public** – `frontend/public/TASK.md` completed.
- [ ] **Frontend Components** – `frontend/src/components/TASK.md` completed.
- [ ] **Frontend Hooks** – `frontend/src/hooks/TASK.md` completed.
- [ ] **Frontend Actions** – `frontend/src/actions/TASK.md` completed.
- [ ] **Frontend Utils** – `frontend/src/utils/TASK.md` completed.
- [ ] **Frontend Styles** – `frontend/src/styles/TASK.md` completed.
- [ ] **Frontend Tests** – `frontend/src/tests/TASK.md` completed.
- [ ] **Infra Docker** – `infra/docker/TASK.md` completed.
- [ ] **Infra Prometheus** – `infra/prometheus/TASK.md` completed.
- [ ] **Infra Grafana** – `infra/grafana/TASK.md` completed.
- [ ] **Infra Scripts** – `infra/scripts/TASK.md` completed.
- [ ] **Data Seeds** – `data/seeds/TASK.md` completed.
- [ ] **Data Migrations** – `data/migrations/TASK.md` completed.

## ✅ How to Mark Completion
1. Open each `TASK.md` file.
2. Replace every unchecked box `- [ ]` with a checked box `- [x]` **only after** the corresponding work (planning, design, or preparatory step) is truly finished.
3. Commit the changes with a message like `chore: complete task tracker for <module>`.
4. Once **all** items in the *Final Gate Checklist* are `[x]`, the repository is considered **Ready‑for‑Implementation**.

## 📄 References & Guidance
- The **Task‑Driven Development** methodology is described in `docs/TASK.md` (already part of the repo).
- All domain‑specific requirements are captured in `docs/IDEA.md`, `PRD_SIGAP.md`, `DESIGN.md`, and `api-contract.yaml`.
- Follow the *best‑practice* checklist format shown in every `TASK.md` for any future module additions.

---

**⚠️ Critical Warning:** *Do not* create any `.py`, `.js`, `.ts`, `.tsx`, `.java`, `.go`, or other executable source files until **every** checklist item above shows a `[x]`. This gate ensures architectural clarity, avoids premature coding, and guarantees that all stakeholders have agreed on the detailed plan before implementation begins.
