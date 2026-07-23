# 📌 Module Task Tracker: Exceptions Package (backend/app/exceptions)

## 🎯 Core Objective & Responsibility
- Menentukan hierarki exception backend agar response error konsisten dan mapping ke HTTP status code terpusat.

## 📋 Development Checklist
- [x] **Core exceptions** – `Unauthorized`, `PermissionDenied`, `NotFoundError` didefinisikan di `app.core.exceptions`.
- [x] **Domain re-export** – package ini mengekspor exception umum untuk dipakai domain.
- [ ] **Exception handler** – tambahkan global handler FastAPI agar semua exception ter-mapping ke schema `Error` di api-contract.
- [ ] **Structured detail** – pastikan `detail` selalu array of object untuk konsumsi frontend.

## 🔒 Constraints & Best Practices
- Jangan ever expose stack trace ke client di production.
- Pesan error harus berbahasa Indonesia dan actionable.
- Jangan gunakan `HTTPException` langsung di domain; pakai exception kustom.

## 📄 References
- `api-contract.yaml` – schema `Error` (line ~974).
- `docs/DESIGN.md` – security architecture.
- `docs/DATA_GOVERNANCE.md` – incident response.
