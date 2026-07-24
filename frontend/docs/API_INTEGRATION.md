# API_INTEGRATION.md — SIGAP Frontend API Integration Guide

## 1. Base Configuration

### 1.1 Environment Variables
```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/v1
SOCKET_URL=http://localhost:3001
```

### 1.2 API Client Helper
```typescript
// src/lib/api-client.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL!;

interface ApiOptions extends RequestInit {
  idempotent?: boolean;  // otomatis tambah X-Idempotency-Key
}

export async function apiFetch<T>(path: string, options: ApiOptions = {}): Promise<T> {
  const { idempotent, ...fetchOptions } = options;
  const headers = new Headers(fetchOptions.headers);

  // GET requests from server components get cookie auth automatically
  if (idempotent && ["POST", "PATCH", "DELETE"].includes(fetchOptions.method ?? "GET")) {
    headers.set("X-Idempotency-Key", crypto.randomUUID());
  }

  const res = await fetch(`${API_URL}${path}`, {
    ...fetchOptions,
    headers,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new ApiError(res.status, err.code || res.status, err.detail || "Unknown error");
  }

  return res.json();
}
```

---

## 2. Endpoint Reference

### 2.1 Auth
| Endpoint | Method | Auth | Idempotent |
|---|---|---|---|
| `/auth/login` | POST | ❌ | ❌ |
| `/auth/me` | GET | ✅ | ❌ |
| `/auth/me/permissions` | GET | ✅ | ❌ |

#### POST /auth/login
```typescript
// Request
type LoginRequest = { email: string; password: string };
// Response
type LoginResponse = { access_token: string; token_type: "bearer"; expires_in: number };
```

#### GET /auth/me
```typescript
type MeResponse = {
  id: string; role: string;
  scope_type: string; scope_value: string[];
};
```

#### GET /auth/me/permissions
```typescript
type PermissionsResponse = {
  role: string;
  permissions: string[];
  scope: { type: string; value: string[] };
};
```

---

### 2.2 Vendors
| Endpoint | Method | Auth | Idempotent |
|---|---|---|---|
| `/vendors` | POST | ✅ | ✅ |
| `/vendors` | GET | ✅ | ❌ |
| `/vendors/{id}` | GET | ✅ | ❌ |
| `/vendors/{id}` | PATCH | ✅ | ✅ |
| `/vendors/{id}/nik` | GET | ✅ (admin/verifikator only) | ❌ |
| `/vendors/{id}/documents` | POST | ✅ | ✅ |
| `/vendors/{id}/documents/{docId}/status` | GET | ✅ | ❌ |
| `/vendors/{id}/documents/{docId}/status/stream` | GET | ✅ | ❌ |
| `/vendors/{id}/verify` | POST | ✅ (verifikator_bgn) | ✅ |
| `/vendors/{id}/sio` | GET | ✅ | ❌ |
| `/vendors/{id}/score` | GET | ✅ | ❌ |

#### TypeScript Types
```typescript
// ── Request ──
interface VendorCreate {
  nama_usaha: string;
  nik_penanggung_jawab: string;   // 16 digit, dikirim ke Server Action
  nib: string;
  alamat: string;
  provinsi: string;
  kabupaten_kota: string;
  kontak_telepon?: string;
}
interface VendorUpdate {
  alamat?: string;
  kontak_telepon?: string;
}
interface VendorVerify {
  decision: "approve" | "reject";
  notes?: string;
}

// ── Response ──
interface Vendor {
  id: string;
  nama_usaha: string;
  nik_penanggung_jawab_masked: string;  // "3175********1234"
  nib: string;
  alamat: string;
  provinsi: string;
  kabupaten_kota: string;
  status: "pending_verification" | "verified" | "rejected" | "suspended";
  vendor_score: number;
  created_at: string;
  updated_at: string;
}
interface VendorNikReveal {
  vendor_id: string;
  nik_penanggung_jawab: string;  // MENTAH — hanya tampil di modal khusus
  revealed_by: string;
  revealed_at: string;
}
interface VendorDocument {
  id: string;
  vendor_id: string;
  document_type: "nik" | "nib" | "pirt" | "sertifikat_halal" | "sertifikat_hygiene";
  file_url: string;
  validation_status: "pending" | "valid" | "invalid";
  validated_via?: string | null;
}
interface DocumentValidationStatus {
  status: "validating" | "valid" | "invalid";
  validated_via?: string | null;
  validated_at: string;
}
interface SIODigital {
  vendor_id: string;
  sio_code: string;
  qr_code_url: string;
  issued_at: string;
  valid_until: string;
}
interface VendorScore {
  vendor_id: string;
  score: number;
  factors: {
    ketepatan_distribusi: number;
    kelengkapan_pelaporan: number;
    hasil_inspeksi: number;
    pengaduan_valid: number;
  };
  last_updated: string;
}
```

---

### 2.3 Distributions
| Endpoint | Method | Auth | Idempotent |
|---|---|---|---|
| `/distributions` | POST | ✅ | ✅ |
| `/distributions` | GET | ✅ | ❌ |
| `/distributions/{id}` | GET | ✅ | ❌ |
| `/distributions/{id}/metadata` | GET | ✅ (verifikator/pengawas/admin) | ❌ |
| `/distributions/{id}/appeal` | POST | ✅ (vendor) | ✅ |

```typescript
interface DistributionCreate {
  vendor_id: string;
  jumlah_porsi: number;
  lokasi_sekolah?: string;
  latitude: number;
  longitude: number;
  metadata?: { capture_time: string; exif_timestamp?: string; device_id?: string };
}
interface Distribution {
  id: string;
  vendor_id: string;
  jumlah_porsi: number;
  lokasi_sekolah?: string;
  latitude: number;
  longitude: number;
  foto_url?: string;
  reported_at: string;
  photo_taken_at?: string | null;
  tampering_suspicion: boolean;
  geo_validation?: {
    distance_from_school_meters: number;
    radius_allowed_meters: number;
    radius_tolerance_meters: number;
    within_tolerance: boolean;
    requires_manual_verification: boolean;
  };
  anomaly?: {
    score: number;
    confidence: number;
    flag: "none" | "low_risk" | "medium_risk" | "high_risk" | "critical";
    detected: boolean;
    details: string[];
    appeal_status: "none" | "pending_review" | "in_progress" | "resolved" | "rejected";
    is_frozen: boolean;
  } | null;
}
interface DistributionMetadata {
  distribution_id: string;
  photo_taken_at?: string;
  exif_timestamp?: string;
  device_id?: string;
  latitude: number;
  longitude: number;
  tampering_suspicion: boolean;
  created_at: string;
}
interface AppealResponse {
  distribution_id: string;
  appeal_status: "pending_review" | "in_progress";
  is_frozen: true;
  submitted_at: string;
}
```

---

### 2.4 Complaints
| Endpoint | Method | Auth | Idempotent |
|---|---|---|---|
| `/complaints` | POST | ❌ (public) | ✅ |
| `/complaints` | GET | ✅ | ❌ |
| `/complaints/{id}` | GET | ❌ (public) | ❌ |
| `/complaints/{id}` | PATCH | ✅ (verifikator) | ✅ |

```typescript
interface ComplaintCreate {
  vendor_id: string;
  kategori: "keracunan" | "keterlambatan" | "kekurangan_porsi" | "kualitas_makanan" | "lainnya";
  deskripsi: string;
  nama_pelapor?: string;
  latitude?: number;
  longitude?: number;
  distribution_id?: string;
  tanggal_kejadian?: string; // date
}
interface Complaint {
  id: string;
  ticket_number: string;
  vendor_id: string;
  kategori: string;
  deskripsi: string;
  severity: "rendah" | "sedang" | "tinggi" | "kritis";
  status: "baru" | "diproses" | "ditindaklanjuti" | "ditutup";
  resolution_notes?: string | null;
  created_at: string;
  sla_deadline: string;
}
```

---

### 2.5 Public
| Endpoint | Method | Auth | Idempotent |
|---|---|---|---|
| `/public/vendors/verify` | GET | ❌ | ❌ |
| `/public/dashboard/summary` | GET | ❌ | ❌ |

```typescript
interface PublicVendorProfile {
  nama_usaha: string;
  kabupaten_kota: string;
  provinsi: string;
  status: string;
  sio_code?: string;
  valid_until?: string;
}
interface PublicDashboardSummary {
  total_vendor_aktif: number;
  total_vendor_termonitor_persen: number;
  total_pengaduan_bulan_ini: number;
  pengaduan_tertindaklanjuti_persen: number;
}
```

---

### 2.6 Admin
| Endpoint | Method | Auth | Idempotent |
|---|---|---|---|
| `/admin/users` | POST | ✅ (admin) | ✅ |
| `/admin/users` | GET | ✅ (admin) | ❌ |

```typescript
interface AdminUserCreate {
  email: string;
  name: string;
  role: "vendor" | "verifikator_bgn" | "pengawas_dinas" | "admin";
  scope_value?: string[];
}
interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  scope_value?: string[];
  is_active: boolean;
  created_at: string;
}
```

---

### 2.7 Audit Logs
| Endpoint | Method | Auth | Idempotent |
|---|---|---|---|
| `/audit-logs` | GET | ✅ (admin/verifikator) | ❌ |

```typescript
interface AuditLog {
  id: string;
  entity_type: string;
  entity_id: string;
  action: "CREATE" | "UPDATE" | "DELETE" | "PII_REVEAL";
  actor_id: string;
  old_values: Record<string, unknown>;
  new_values: Record<string, unknown>;
  timestamp: string;
  ip_address: string;
}
```

---

## 3. Common Types

```typescript
interface Pagination {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}
interface PaginatedResponse<T> {
  data: T[];
  pagination: Pagination;
}
interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>[];
}
```

## 4. Error Codes

| HTTP | error_code | Arti |
|---|---|---|
| 400 | VALIDATION_ERROR | Payload tidak valid |
| 401 | UNAUTHORIZED | Token tidak ada/kadaluarsa |
| 403 | FORBIDDEN | Role/scope tidak punya izin |
| 404 | NOT_FOUND | Resource tidak ditemukan |
| 409 | IDEMPOTENCY_CONFLICT | Idempotency key clash |
| 422 | VALIDATION_FAILED | Validasi field gagal |
| 429 | RATE_LIMIT_EXCEEDED | Too many requests |

## 5. Query Parameters (GET List Endpoints)

### Vendors
```
?status=pending_verification|verified|rejected|suspended
&province=DKI+Jakarta
&page=1
&page_size=20
```

### Distributions
```
?vendor_id={uuid}
&date_from=2026-01-01
&date_to=2026-12-31
&has_anomaly=true|false
&page=1
&page_size=20
```

### Complaints
```
?status=baru|diproses|ditindaklanjuti|ditutup
&severity=rendah|sedang|tinggi|kritis
&page=1
&page_size=20
```

### Audit Logs
```
?entity_type=vendor|distribution|complaint|user
&action=CREATE|UPDATE|DELETE|PII_REVEAL
```

## 6. SSE / Realtime

### Document Validation via SSE
```typescript
// GET /vendors/{vendorId}/documents/{documentId}/status/stream
const source = new EventSource(`/v1/vendors/${vendorId}/documents/${docId}/status/stream`);
source.onmessage = (e) => {
  const data = JSON.parse(e.data);  // { status, validated_via, validated_at }
  // Update UI
};
```

### Socket.IO Channels (setelah implementasi)
```typescript
// docs:status:{uploadId}
socket.on("validation_update", (data) => {
  // { status, validated_via, validated_at }
});

// anomaly:{reportId}
socket.on("anomaly_result", (data) => {
  // { score, confidence, flag, details }
});

// complaint:{ticketId}
socket.on("status_change", (data) => {
  // { status, resolution_notes, updated_at }
});
```
