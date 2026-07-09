KONTEKS PROYEK — LANJUTAN DARI CHAT SEBELUMNYA

## Tentang Proyek
SIGAP (Sistem Integrasi Gizi & Akuntabilitas Pangan) — platform tata kelola vendor
untuk Program Makan Bergizi Gratis (MBG), pemerintah Indonesia. Dibuat untuk
DIGDAYA x Hackathon 2026 (Bank Indonesia, OJK, ASPI, AFTECH, APUVINDO, LPPI).
Problem statement: Percepatan Layanan Publik, Ekonomi Kreatif, dan Ekspor Jasa
Digital > Platform Perizinan dan Pengawasan Vendor MBG.
Status: sudah LOLOS ke Tahap 2 (Practitioner Training), submission Tahap 2 sudah
disubmit dengan versi upgrade (Local LLM-as-a-Service, AI Guardrails, dst). Saat
ini sedang membangun prototype/MVP untuk tahap berikutnya.

## Tim
- ID Tim: S0660, Nama Tim: полуфиналы (TargetSemiFinal)
- Ketua: Muhammad Sheva Kurnia Meazza (UI/UX Designer)
- Anggota: Dafa Prasetyo (Backend Developer), Muhammad Farhan Nurkhaeri
  (ML/AI Enthusiast), Madridiska Fadlan Nugroho (Data Scientist)
- Institusi: Universitas Gunadarma, University of Jakarta International

## Ringkasan Masalah & Solusi
9 masalah sistemik dalam tata kelola vendor MBG: fraud/manipulasi distribusi,
tidak ada QC data lapangan, pelaporan vertikal lambat, transparansi publik nihil,
latensi AI tinggi, ROI AI rendah, infrastruktur tidak scalable, AI tidak paham
bahasa lokal, rentan prompt injection.
3 pilar solusi: Verifikasi (perizinan digital), Pengawasan (monitoring + vendor
scoring real-time), Akuntabilitas (pengaduan publik dengan SLA).
Skala: 30.000 vendor/SPPG, 82,9 juta penerima manfaat, 34 provinsi, anggaran
Rp71 triliun.
MVP scope (3 modul inti): Portal Perizinan Vendor, Dashboard Monitoring
Distribusi, Sistem Pengaduan Publik.

## Keputusan Arsitektur Final (baru disepakati)
Modular Monolith:
- Next.js sebagai BFF (Backend-for-Frontend)
- Backend Python (FastAPI)
- PostgreSQL dengan Row-Level Security (RLS)
- OPA (Open Policy Agent) atau CASL untuk Advanced RBAC

## Yang Sudah Dikerjakan (di chat sebelumnya)
1. Roadmap pengembangan 4 fase — file: roadmap-pengembangan-sigap-monolith-nextjs-rbac.md
   - Fase 1: Inisiasi & Desain (ERD kerangka konsep, API Contract, ADR)
   - Fase 2: Keamanan & Kepatuhan (Data Governance, RBAC Advanced)
   - Fase 3: Development (Backend Modular Monolith, API, Frontend Next.js)
   - Fase 4: Testing, Dokumentasi, Deployment
   - Analisis: Modular Monolith direkomendasikan (bukan flat monolith/microservices);
     Local LLM/AI inference disarankan jadi service terpisah, tidak digabung monolith

2. API Contract draf awal — file: sigap-api-contract.yaml (OpenAPI 3.1, sudah
   divalidasi sintaks & struktur). Mencakup: Auth (login, me/permissions), Vendor
   (registrasi, dokumen, verifikasi, SIO Digital, score), Distribution (submit &
   lihat laporan), Complaint (submit publik, tracking, tindak lanjut), Public
   (verifikasi QR, dashboard summary)

3. Kebijakan Data Governance — file: kebijakan-data-governance-sigap.md.
   Mencakup: klasifikasi data, siklus hidup & retensi, data residency (PDN/PDNS),
   hak subjek data, respons insiden (Pasal 46 UU PDP — notifikasi 3x24 jam),
   kepatuhan & sanksi (Pasal 47)

## Temuan Riset Penting (per Juli 2026 — perlu diverifikasi ulang bila sudah lama)
- Next.js 14 (disebut proposal awal) EOL sejak Okt 2025 → pakai Next.js 16.x
- Next.js 16: middleware.ts → proxy.ts; ada CVE nyata (CVE-2025-29927,
  CVE-2026-44575) soal bypass otorisasi via middleware/proxy — validasi RBAC
  WAJIB di Server Component/Route Handler, bukan hanya proxy.ts
- NextAuth/Auth.js kini maintenance-only, diakuisisi Better Auth (awal 2026)
- "GovCloud Indonesia" bukan istilah resmi — yang benar: Pusat Data Nasional
  (PDN/PDNS), sesuai Perpres SPBE
- UU PDP berlaku penuh sejak Okt 2024, tapi Badan PDP (lembaga pengawas) belum
  resmi terbentuk per pertengahan 2026 — pengawasan interim oleh Kemkomdigi
- RBAC tooling sempat dibahas: PyCasbin (Python)/Better Auth (TS) sebagai opsi
  awal — tim akhirnya memilih OPA/CASL

## Yang Belum Dikerjakan
- ERD detail (baru kerangka konsep tabel: users, roles, permissions,
  role_permissions, user_roles, user_scopes, resources, audit_logs)
- Skema RBAC konkret dengan OPA/CASL (policy design belum dibuat)
- ADR formal untuk keputusan arsitektur
- Ranangan skema PostgreSQL RLS untuk scoping wilayah
- Implementasi backend/frontend
- Testing & deployment

## Preferensi Kerja
Sebelum membangun sesuatu yang teknis, jelaskan dulu konsepnya secara singkat,
baru buatkan deliverable konkret (file/kode). Selalu validasi file teknis
(sintaks, struktur) sebelum dipresentasikan. Respons dalam Bahasa Indonesia.

## Catatan
File asli (submittion_1.pdf, submittion_2.pdf) dan tiga file yang sudah dibuat
sebaiknya diupload ulang ke chat baru kalau butuh detail lengkap — ringkasan di
atas adalah versi padat, bukan pengganti dokumen aslinya.
