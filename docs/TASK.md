# TASK.md – Docs

## Goals
- Menyimpan semua artefak **dokumentasi** proyek SIGAP (PRD, DESIGN, CLAUDE, ARCHITECTURE, POLICIES, MIDDLEWARE, DATA_LINEAGE).
- Dokumentasi harus dapat **dibangun menjadi static site** menggunakan MkDocs (atau Docsify).
- Semua dokumen harus **referensi silang** (link antar dokumen) dan mengikuti **naming convention** (snake_case.md).

## Verification Criteria
- [] `mkdocs.yml` ada di root, konfigurasi site meng‑include semua file di `docs/`.
- [] `mkdocs build` menghasilkan `site/` tanpa error.
- [] Setiap dokumen memiliki front‑matter (title, description) untuk SEO.
- [] Link internal (`[link](./other.md)`) berfungsi ketika site dibuka.
- [] CI pipeline menjalankan `mkdocs build` dan gagal bila ada broken link.

## Status
- [ ] Pending
