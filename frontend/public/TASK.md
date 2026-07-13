# TASK.md – Frontend/public

## Goals
- Menyimpan aset statis (logo, favicon, gambar ilustrasi) yang akan di‑serve langsung oleh Next.js.
- Optimasi ukuran gambar (WebP, compress) untuk performa LCP < 1 s.

## Verification Criteria
- [] Semua aset dapat di‑akses lewat `/public/<filename>` tanpa 404.
- [] Gambar dikompresi < 200 KB, format WebP bila memungkinkan.
- [] LCP (Largest Contentful Paint) pada halaman Home < 1 s pada jaringan 3G.
- [] CI menjalankan `npm run lint && npm run build` dan gagal bila ada asset yang tidak ter‑optimasi.

## Status
- [ ] Pending
