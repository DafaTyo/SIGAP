# TASK.md – Frontend/tests

## Goals
- Menulis unit & integration test untuk seluruh lapisan frontend (pages, components, hooks).
- Memastikan **coverage** ≥ 80 % secara keseluruhan, dan masing‑muka ≥ 80 % untuk pages + components.

## Verification Criteria
- [] `npm test` menghasilkan laporan coverage di `coverage/`.
- [] Semua snapshot tests lulus pada CI.
- [] Lint (`npm run lint`) bersih (ESLint + Prettier).
- [] CI pipeline (`ci.yml`) otomatis menjalankan `npm test` dan gagal bila coverage < 80 %.

## Status
- [ ] Pending
