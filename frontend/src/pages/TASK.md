# TASK.md – Frontend/pages

## Goals
- Implement semua halaman utama aplikasi vendor‑governance (Dashboard, Vendor List, Vendor Detail, Login, Error pages).
- Gunakan Next.js **file‑system routing** dan **getServerSideProps**/`API` untuk data yang sensitif.
- Pastikan setiap halaman mematuhi **WCAG 2.1 AA** dan responsive design (mobile‑first).

## Verification Criteria
- [] Halaman Dashboard menampilkan tabel vendor dengan pagination, sorting, dan filter.
- [] Halaman Login berfungsi dengan OAuth2/OIDC ke FastAPI Auth; token disimpan di http‑only SameSite cookie.
- [] Error pages (`404`, `500`) memiliki UI yang konsisten dengan brand SIGAP.
- [] Semua halaman melewati **Lighthouse** audit: Performance ≥ 90, Accessibility ≥ 90, Best Practices ≥ 90, SEO ≥ 90.
- [] Unit‑test dengan **Jest + React Testing Library** mencakup minimal 80 % coverage pada folder `pages`.
- [] CI pipeline (`ci.yml`) menjalankan `npm test` dan gagal bila coverage < 80 %.

## Status
- [ ] Pending
