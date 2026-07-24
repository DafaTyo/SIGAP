# DESIGN.md — Frontend Architecture: SIGAP

## 1. Route Structure

### 1.1 Route Map (dari desain)
```
/                                    → Redirect ke dashboard (jika login) / landing page
/auth/login                          → Split-screen login (2-step)
/auth/register                       → (future)

# Publik (PublicLayout — header minimal + footer)
/public/
├── /                                → Landing Page + Chatbot SIGAP Asisten AI
├── /vendors/search                  → Cari Vendor (split: list kiri + map kanan)
├── /complaints                      → Layanan Pengaduan (form + ticket tracking)
├── /vendors/register                → Registrasi Vendor 3-step wizard
│   ├── /step1                       → Identitas Hukum (NIK, NIB, NPWP)
│   ├── /step2                       → Berkas Kelayakan (upload dokumen)
│   ├── /step3                       → Lokasi & Akun (map pin + credentials)
│   └── /success                     → Sukses — pending verification

# Dashboard (DashboardLayout — sidebar + navbar)
/(dashboard)/
├── /                                → Redirect ke role-specific dashboard
│
├── # Role: BGN/Admin
│   ├── /                            → Dashboard BGN (stats + map + logistics panel)
│   ├── /perizinan                   → Verifikasi vendor (table + SLA badges)
│   ├── /pengaduan                   → Pusat Pengaduan (ticket list + detail panel)
│   ├── /pengaduan/{id}              → Detail pengaduan + timeline
│   ├── /laporan-audit              → Laporan Audit (charts + audit trail table)
│   └── /laporan-audit/{logId}       → Detail log entry
│
├── # Role: Vendor
│   ├── /                            → Dashboard Vendor (stats + distribution status)
│   ├── /pelaporan-harian            → Daily reporting (6-step flow)
│   │   ├── /input                   → Input porsi per sekolah
│   │   ├── /bukti                   → Upload foto geotagging
│   │   ├── /kendala                 → Catat kendala lapangan
│   │   ├── /ringkasan              → Review & konfirmasi
│   │   └── /sukses                  → Laporan terkirim (loading animation rocket)
│   ├── /manajemen-aset              → Armada + kapasitas dapur
│   └── /rapor-aduan                → Skor vendor + tren + daftar aduan
│
├── # Role: Verifikator/Pengawas
│   ├── /perizinan                   → Sama dengan BGN view
│   └── /pengaduan                   → Sama dengan BGN view
│
└── # Shared
    ├── /vendors/{id}                → Detail vendor (tab: info, dokumen, SIO, skor)
    └── /distributions/{id}          → Detail distribusi
```

### 1.2 Auth Protection
| Kelompok | Middleware | Guard |
|---|---|---|
| `(public)` | None | Semua orang bisa akses (landing, cari vendor, pengaduan, register) |
| `(auth)` | Guest only | Redirect ke dashboard jika sudah login |
| `(dashboard)` | Authenticated | JWT token wajib, validasi di middleware, redirect ke login jika invalid |
| Role: BGN | RBAC | Hanya admin/verifikator_bgn/pengawas_dinas |
| Role: Vendor | RBAC | Hanya role=vendor |

### 1.3 RLS / ABAC di Frontend
- **Middleware** membaca role + scope dari JWT (via cookie).
- **Redirect** jika user tidak punya akses ke halaman tertentu.
- **CASL** mengatur visibility tombol/action di UI (`can('vendors:verify')` → show/hide tombol Verify).

## 2. Layout Components (dari desain)

### 2.1 Public Layout (Landing Page)
```
┌──────────────────────────────────────────────────────┐
│ Logo SIGAP    Beranda | Cari Vendor | Pengaduan   Masuk │
├──────────────────────────────────────────────────────┤
│                 Hero Section (2-col)                   │
│   Judul + Subtitle        Ilustrasi Isometric          │
│   [Pantau Wilayah] [Daftar Mitra]                     │
├──────────────────────────────────────────────────────┤
│              Tentang Kami — Visi & Misi               │
│   (2-col: teks + diagram lingkaran/icons)              │
├──────────────────────────────────────────────────────┤
│           Bagaimana SIGAP Bekerja (4 cards grid)       │
│   [Vendor Terdaftar] [Monitoring] [Laporan] [Sertif]   │
├──────────────────────────────────────────────────────┤
│              SIGAP Asisten AI (Chatbot)                │
│   — Green accent header, message bubbles, input        │
├──────────────────────────────────────────────────────┤
│   CTA Banner: "Daftar menjadi Mitra SPPG"              │
│   Footer: Logo | Kebijakan Privasi | Syarat | Kontak     │
└──────────────────────────────────────────────────────┘
```

### 2.2 Auth Layout (Login — Split Screen 50/50)
```
┌──────────────────┬───────────────────────────────────┐
│   Left Panel     │       Right Panel                  │
│   (branding)     │       (form)                       │
│                   │                                   │
│   Foto anak      │   "Masuk ke Akun Anda"             │
│   dengan tray    │   "Silahkan masukan kredensial..." │
│   makanan        │                                   │
│                   │   ○ Email atau NIK [input]        │
│   "Selamat       │   ○ Password [input]              │
│   Datang di      │   □ Ingat Saya  Lupa kata sandi? │
│   SIGAP"         │                                   │
│                   │   [█████ Masuk █████████]         │
│   Overlay biru   │   ─────────────────────            │
│   + logo         │   Belum memiliki Akun?             │
│                   │   [Hubungi admin SIGAP >]         │
└──────────────────┴───────────────────────────────────┘
```

### 2.3 Dashboard Layout
```
┌──────┬──────────────────────────────────────────────┐
│      │  Page Title           [Filter Wilayah]  Profil▾│
│      ├──────────────────────────────────────────────┤
│ Logo │  ┌──────┐ ┌──────┐ ┌──────┐                   │
│ SIGAP │  │Card 1│ │Card 2│ │Card 3│                   │
│      │  └──────┘ └──────┘ └──────┘                   │
│──nav─│                                               │
│ ██Dashboard██ │  [Search...]    [Filter] [↻] [Export] │
│  Pengaduan   │  ┌──────────────────────────────────┐  │
│  Perizinan   │  │ Data Table / Content Grid         │  │
│  Laporan     │  │   ...rows with badges, actions    │  │
│      │       │  │                                    │  │
│      │       │  └──────────────────────────────────┘  │
│      │       │  « 1 2 3 ... 10 »  Tampilkan 5         │
│      │       │                                         │
│  [Keluar]   │  Last updated: 09.11.36 (auto 60s)     │
└──────┴──────────────────────────────────────────────┘
```

### 2.4 Public Vendor Search (Split: List + Map)
```
┌──────────────────┬───────────────────────────────────┐
│   Vendor List    │       Interactive Map              │
│                   │                                   │
│   ┌────────────┐ │    ┌──────────────────────────┐   │
│   │ Thumb      │ │    │                          │   │
│   │ SPPG XYZ   │ │    │   Jakarta area map       │   │
│   │ Koja       │ │    │   with blue pins         │   │
│   │ ✅Verified │ │    │   + popup on hover        │   │
│   │ ⭐Rating   │ │    │                          │   │
│   │ 1500/hari  │ │    │                          │   │
│   │ [Lihat >]  │ │    └──────────────────────────┘   │
│   └────────────┘ │                                   │
│   [Tampilkan     │                                   │
│    Lebih Banyak] │                                   │
└──────────────────┴───────────────────────────────────┘
```

## 3. Data Flow

### 3.1 Request Flow
```
Client Component
    │
    ├─ Server Action ──→ Auth + Masking ──→ FastAPI /v1/...
    │   (actions/*.ts)      (BFF layer)        (backend)
    │
    ├─ TanStack Query ──→ Direct API call ──→ FastAPI
    │   (hooks/*.ts)        (GET only)
    │
    └─ Socket.IO ───────→ Redis Pub/Sub ←─── FastAPI Worker
        (hooks/useSocket)
```

### 3.2 Auth Flow
```
Login Form (split-screen)
  → Server Action: login(email, password)
  → Fastapi POST /auth/login → return JWT
  → Server Action: set cookie (httpOnly)
  → Redirect ke dashboard sesuai role

Setiap request:
  → Next.js Middleware: baca cookie → valid JWT → inject header
  → Server Action: forward Authorization header ke backend
```

## 4. Animation Strategy

### 4.1 Page Transitions
```tsx
"use client";
import { motion, AnimatePresence } from "motion";

export default function AnimatedLayout({ children }: { children: React.ReactNode }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -8 }}
        transition={{ duration: 0.2, ease: "easeOut" }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

### 4.2 List Stagger
```tsx
<motion.ul variants={{ visible: { transition: { staggerChildren: 0.05 } } }}>
  {items.map(item => (
    <motion.li
      layout
      key={item.id}
      variants={{ hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0 } }}
    >
      {item.name}
    </motion.li>
  ))}
</motion.ul>
```

### 4.3 Micro-interactions
| Komponen | Animasi | Teknik |
|---|---|---|
| Button | `transition-all hover:scale-[1.02] active:scale-[0.98]` | Tailwind |
| Card | `hover:shadow-lg hover:-translate-y-0.5 transition-all` | Tailwind |
| Modal | scale(0.95→1) + opacity(0→1) | Framer Motion |
| Skeleton | Shimmer pulse | Tailwind `animate-pulse` |
| Toast | Slide in from right + fade out | Framer Motion |
| Sidebar | Smooth width collapse/expand | `motion.div layout` |
| Metric number | Count-up on viewport enter | Framer Motion `useAnimate` |
| Donut/gauge chart | Animated arc on mount | Framer Motion or SVG transition |
| Success checkmark | Scaling + rotating check | Framer Motion |
| Loading animation | Rocket flying up (di "mengirim data") | Framer Motion + Lottie |

### 4.4 Rocket Loading Screen (dari desain)
Desain menampilkan ilustrasi roket biru + awan + teks "Tunggu, Roket sedang mengantar data Anda" — implementasi:
- Framer Motion loop animation: rocket bounce + cloud float
- Auto-redirect ke halaman sukses setelah 3-5 detik

## 5. Realtime — Socket.IO Integration

### 5.1 Architecture
```
FastAPI Worker → Redis Pub/Sub → Socket.IO Server → Browser Client
```

### 5.2 Channel Mapping
| Channel | Event | Payload |
|---|---|---|
| `docs:status:{uploadId}` | `validation_update` | `{status, validated_via, validated_at}` |
| `anomaly:{reportId}` | `anomaly_result` | `{score, confidence, flag, details}` |
| `complaint:{ticketId}` | `status_change` | `{status, resolution_notes, updated_at}` |

### 5.3 Implementation
- Socket.IO client hook (`useSocket`) connect di layout level.
- Zustand store untuk realtime events.
- TanStack Query `invalidateQueries` saat event realtime diterima.
- "Live" indicator di logistics panel (pulse animation).

## 6. State Management

### 6.1 Server State (TanStack Query)
- `useQuery` untuk GET endpoints dengan caching + staleTime.
- `useMutation` untuk POST/PATCH, auto-invalidate query terkait.
- Query keys: `["vendors", filters]`, `["distributions", id]`, dll.

### 6.2 Client State (Zustand)
- `useAuthStore` → user, token, role
- `useUIStore` → sidebar collapsed, theme, active filters
- `useSocketStore` → connection status, pending events

## 7. Security di Frontend

| Risiko | Mitigasi |
|---|---|
| PII bocor di client | Server Actions masking + CASL hide/show |
| XSS | React + Next.js escape otomatis, jangan `dangerouslySetInnerHTML` |
| CSRF | SameSite cookie + Next.js Server Actions built-in CSRF |
| Token leakage | httpOnly cookie, tidak di localStorage |
| Unauthorized page access | Middleware check JWT + role setiap request |
| Abuse API key | API key di server/actions, tidak di client bundle |
| Foto geotagging | Validasi EXIF GPS di Server Action sebelum kirim ke backend |

## 8. Key Pages — Visual Specification

### 8.1 Landing Page
- **Hero**: Left text (judul "Pantau Makanan Sehat di Wilayah Kamu" + CTA buttons), right isometric illustration
- **Tentang Kami**: Visi (mata diagram) + Misi (target diagram) — 2 sections dengan icon circles
- **Bagaimana SIGAP Bekerja**: 4 cards grid (Vendor Terdaftar, Monitoring, Laporan, Sertifikasi Digital)
- **Chatbot**: SIGAP Asisten AI — green accent, floating di kanan bawah atau full section
- **CTA Banner**: Dark blue bg, white text "Mau menjadi bagian dari Perubahan?"
- **Footer**: Light blue bg, logo + 3 links + copyright

### 8.2 Dashboard BGN
- **3 Metric Cards**: Total Porsi (green icon), Vendor Aktif (blue icon), Indikator Keterlambatan (red icon)
- **Interactive Map**: Jakarta area, blue house pins (SPPG), green lines (logistics routes), red pulse (anomaly)
- **Logistics Panel (kanan)**: "Logistik Real-Time" header with "Langsung" live indicator, active shipments list with progress bars + ETA
- **Footer**: Last updated time + auto-refresh note

### 8.3 Pelaporan Harian Vendor (6-step)
1. Input porsi per sekolah — table dengan target vs delivered, status badge (Sesuai/Tidak Sesuai)
2. Upload foto geotagging
3. Catat kendala lapangan
4. Ringkasan & konfirmasi akhir
5. Loading animation (roket)
6. Sukses: "Laporan Harian Berhasil Dikirim" + auto-redirect 5s

### 8.4 Registrasi Vendor (3-step wizard)
- **Step 1**: NIK (masked display), NIB, NPWP — dengan catatan UU PDP
- **Step 2**: Upload 5 dokumen (KTP, NPWP, Akta, NIB, SK Kemenkumham) — format PDF max 10MB
- **Step 3**: Map pin lokasi + kapasitas maksimum + username + email + password + checkbox S&K
- **Success**: Timeline 3-stage (Pendaftaran✅ Verifikasi⏳ Aktivasi🔒) + WhatsApp help button

## 9. Build & Run

```bash
# Install
pnpm install

# Dev
pnpm dev                        # Next.js :3000
pnpm dev:socket                  # Socket.IO :3001

# Build
pnpm build

# Test
pnpm test                       # Vitest
pnpm test:e2e                   # Playwright

# Lint
pnpm biome check src/
```
