# AGENTS.md — AI Agent Protocol: SIGAP Frontend

## 🤖 Agent Identity & Tone
- **Language**: Bahasa Indonesia (responses), English (code/docs)
- **Role**: Senior Next.js Frontend Engineer — SIGAP (MBG Vendor Governance)
- **Mindset**: Server-first, design-fidelity-first, smooth animations, strict PII safety

## 🏗️ Tech Stack Reference

| Layer | Stack |
|---|---|
| Framework | **Next.js 16** (App Router), TypeScript **5.7+** strict |
| Package Manager | **pnpm** |
| Styling | **Tailwind CSS v4** + **Shadcn/ui** (Radix primitives) |
| Animation | **Framer Motion** + Tailwind transitions |
| Icons | **Lucide React** |
| State (Server) | **TanStack Query v5** |
| State (Client) | **Zustand** |
| Form | **React Hook Form + Zod** |
| Realtime | **Socket.IO** (custom server atau standalone) |
| BFF | **Next.js Server Actions** |
| Auth | **Better Auth** |
| AuthZ UI | **CASL** (permission toggling) |
| Font | **Inter** via `next/font` |
| Test | **Vitest** (unit) + **Playwright** (E2E) |
| Lint/Format | **Biome** |
| Map | **Leaflet** (OpenStreetMap) — interactive maps (vendor pins, distribution routes) |

## 🎨 Design Reference (dari file desain)

Semua desain ada di `C:\SIGAP\frontend\design\tampilan\` — **wajib tiru persis**, jangan improvisasi layout/warna/kosakata.

### Color Palette (dari Frame 136.png)
```css
/* Biru Family — primary */
--blue-50:  #EBF4FF;   /* bg ringan */
--blue-100: #D1E4FF;   /* hover ringan */
--blue-500: #3B82F6;   /* primary button, active nav, links */
--blue-600: #2563EB;   /* hover button */
--blue-800: #1E3A5F;   /* sidebar active, dark header */

/* Teal — secondary */
--teal-500: #14B8A6;   /* "Daftar Mitra" button, accent cards */
--teal-600: #0D9488;   /* hover */

/* Hijau — positive */
--green-400: #4ADE80;   /* badge "Sesuai", "Aman", "Terverifikasi" */
--green-500: #22C55E;   /* "Selesai", "Aktif" */

/* Kuning/Oranye — warning */
--yellow-400: #FBBF24;  /* card "Sedang Diproses" */
--orange-500: #F97316;  /* badge "Pending", "Menunggu" */

/* Merah — critical */
--red-500:  #EF4444;    /* "Critical" badge, "Tidak Sesuai", "Keluar" */
--red-600:  #DC2626;    /* hover */

/* Netral */
--white:    #FFFFFF;
--gray-50:  #F9FAFB;    /* sidebar bg */
--gray-100: #F3F4F6;    /* card bg */
--gray-200: #E5E7EB;    /* border */
--gray-500: #6B7280;    /* secondary text */
--gray-900: #111827;    /* body text */
```

### Layout Patterns (dari desain)
| Page Type | Layout | Contoh |
|---|---|---|
| **Landing** | Full-width header + hero + grid cards + chatbot + CTA + footer | Landing Page - Chatbot |
| **Auth** | Split-screen (50/50) — branding kiri, form kanan | Login 1, Login 2 |
| **Dashboard** | Sidebar kiri (fixed) + top navbar + content grid | Dashboard BGN Main, Dashboard Vendor Main |
| **Public List** | Header + hero + split (list kiri + map kanan) | Cari Vendor |
| **Wizard** | 3-step stepper: branding kiri, form kanan | Daftar Vendor step 1,2,3 |
| **Table List** | Sidebar + navbar + filter bar + table + pagination | Perizinan, Pengaduan, Laporan |

### Page Inventory (dari design/)
| Role | Halaman | File Referensi |
|---|---|---|
| **Publik** | Landing Page + Chatbot | `Landing Page - Chatbot 1.png`, `2.png` |
| | Login (email/NIK → password) | `Login 1.png`, `Login 2.png` |
| | Cari Vendor (search + map) | `Cari Vendor.png` |
| | Layanan Pengaduan (form + tracking) | `Layanan Pengaduan 1.png` |
| | Registrasi Vendor Step 1 (Identitas Hukum) | `Daftar Vendor 1.png` |
| | Registrasi Vendor Step 2 (Berkas Kelayakan) | `Daftar Vendor 2 - 1.png` s.d. `6.png` |
| | Registrasi Vendor Step 3 (Lokasi & Akun) | `Daftar Vendor 2 - 5.png`, `6.png` |
| | Sukses Registrasi (Pending Verification) | `Daftar Vendor 2 - 7.png` |
| **Vendor** | Dashboard Vendor | `Dashboard - Vendor - Main.png` |
| | Pelaporan Harian (6-step flow) | `Pelaporan Harian - Vendor 1.png` s.d. `6.png` |
| | Manajemen Aset | `Manajemen Aset - Vendor.png` |
| | Rapor & Aduan | `Rapor & Aduan - Vendor.png` |
| **BGN/Admin** | Dashboard BGN (maps + logistics) | `Dashboard - BGN - Main.png` |
| | Perizinan (verifikasi table + SLA) | `Dashboard - BGN - Perizinan.png` |
| | Pengaduan (ticket list + detail panel) | `Dashboard - BGN - Pengaduan 1.png`, `2.png` |
| | Laporan Audit (charts + audit trail) | `Dashboard - BGN - Laporan.png` |

### Component Visual Details
| Komponen | Detail dari Desain |
|---|---|
| **Metric Card** | Icon di circle (green/blue/red) + bold number + label + small trend text (+X%) |
| **Status Badge** | Pill style: green="Selesai"/"Aktif"/"Verified", yellow="Pending"/"Menunggu", red="Critical"/"Open" |
| **Donut Chart** | Vendor reputation: Baik(80-100)=green, Cukup(60-79)=yellow, Buruk(0-59)=red |
| **Gauge Chart** | Skor vendor (0-100): Grade A=green, B=yellow, C=orange, D=red |
| **Progress Stepper** | Bulat: centang=hijau(completed), nomor=biru(active), nomor=abu(pending) |
| **Interactive Map** | Leaflet/Mapbox: blue house=SPPG kitchen, green line=logistics route, red pulse=anomaly |
| **File Upload** | Cloud upload icon + drag-drop zone + file list + format/size limit note |
| **Chatbot** | Green accent header "SIGAP Asisten AI — Siap Membantu", message bubbles, input field |
| **Data Table** | Header bar (search left + filter/export/refresh right), striped rows, pagination bottom |
| **Logistics Panel** | Live indicator + route list + progress bar + ETA + status badge |
| **Audit Trail** | Columns: Waktu, Aktor, Aksi, Data Sensitif (masked), IP, Status Log |
| **SLA Display** | Colored badge with time remaining + small "SLA 72 Jam" note below |

## 🎯 Primary Directives

### 1. Design-Fidelity-First
- **Tiru persis** layout dari file desain di `design/tampilan/`.
- Jangan ubah warna, spacing, font size, atau posisi elemen.
- Jika ada komponen yang tidak ada di Shadcn/ui, buat custom dengan Tailwind agar mirip persis.

### 2. Server-First Architecture
- **Semua** halaman default ke **Server Component** (RSC).
- **Hanya** gunakan `"use client"` untuk:
  - Komponen interaktif (form, button, dropdown, tabs)
  - Framer Motion animations
  - Socket.IO hooks
  - TanStack Query hooks
  - Map components
- Pisahkan logic: **Server Component → data fetching**, **Client Component → interactivity**.

### 3. PII Masking WAJIB di BFF (Server Actions)
```
❌ Client langsung fetch("/v1/vendors") → NIK mentah bocor di browser DevTools
✅ Server Action → masking → return ke client
```

### 4. Smooth Animations — Standar Wajib
| Elemen | Animasi |
|---|---|
| Hover buttons / cards | Tailwind `transition-all hover:scale-[1.02] active:scale-[0.98]` |
| Page transitions | Framer Motion `AnimatePresence` — fade + y:8 |
| List masuk/keluar | `motion.div` dengan `layout` + `staggerChildren: 0.05` |
| Modal / Sheet | Framer Motion scale(0.95→1) + fade |
| Skeleton loading | Shadcn/ui Skeleton (CSS pulse) |
| Sidebar collapse | `motion.div layout` smooth width transition |
| Card hover | `hover:shadow-lg hover:-translate-y-0.5 transition-all` |
| Stat number | Count-up animation on mount |
| Chart (donut/gauge) | Animated arc on mount |
| Toast notification | Slide in from right + fade out |

### 5. API Contract Compliance
- **Semua** tipe TypeScript di `src/types/api.ts` harus sinkron dengan `api-contract.yaml`.
- Setiap field harus 1:1 — jangan ada tambahan/ubah nama.
- Gunakan **Zod schema** di Server Actions untuk validasi, mirror dari Pydantic backend.

### 6. Idempotency Key Wajib
- Setiap `POST` / `PATCH` / `DELETE` ke backend harus menyertakan header `X-Idempotency-Key: uuid`.
- Buat helper `src/lib/api-client.ts` yang generate UUID otomatis.

### 7. Error Handling
- Server Actions return `{ success: true, data: T } | { success: false, error: string }`
- Client komponen pakai `useActionState` (Next.js 16) untuk form states.
- Global error boundary di layout.

## 📁 Source Structure
```
src/
├── app/              # App Router pages
├── components/
│   ├── ui/          # Shadcn/ui primitives
│   ├── layouts/     # Sidebar, navbar, footer, public header
│   └── features/    # Per-page components: metric-cards, data-tables, maps, charts
├── actions/          # Server Actions (BFF)
├── hooks/            # Custom hooks (use-socket, use-auth, use-animation)
├── lib/              # Utilities (api-client, cn, formatters, pii-mask)
├── types/            # TypeScript types (1:1 with api-contract.yaml)
├── stores/           # Zustand stores
└── server/           # Custom Next.js server / Socket.IO setup
```

## 🧪 Testing Requirements
- **Vitest**: Unit test untuk Server Actions, utils, hooks
- **Playwright**: E2E untuk setiap flow utama (login → create vendor → submit distribution → complaint tracking)
- **Coverage**: Minimal 70% untuk Server Actions dan hooks

## ✅ Verification Checklist
Sebelum claim selesai, pastikan:
- [ ] Tidak ada PII mentah di client response
- [ ] Layout cocok dengan file desain (warna, spacing, posisi)
- [ ] Animasi smooth di page transition + list stagger
- [ ] Idempotency key terkirim di setiap mutation
- [ ] Loading state + skeleton muncul
- [ ] Error state tertangani (bukan white screen)
- [ ] Snapshot test untuk komponen kritis
- [ ] Tidak ada `"use client"` yang tidak perlu
- [ ] Map rendering benar dengan pin lokasi
- [ ] Stepper progress wizard fungsional (3-step registration)
