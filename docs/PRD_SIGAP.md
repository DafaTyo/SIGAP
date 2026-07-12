# 📄 Product Requirements Document (PRD): SIGAP
**Sistem Integrasi Gizi & Akuntabilitas Pangan**  
*Platform Tata Kelola Vendor Program Makan Bergizi Gratis (MBG)*

| Version | Status | Date | Owner | Note |
| :--- | :--- | :--- | :--- | :--- |
| v1.0 | Draft | 11 July 2026 | Senior Solution Architect | Initial comprehensive draft |

---

## 1. Executive Summary
### 1.1 Visi Produk
Membangun ekosistem tata kelola vendor yang transparan, akuntabel, dan terautomasi untuk memastikan distribusi program Makan Bergizi Gratis berjalan tepat sasaran, higienis, dan bebas dari anomali/fraud.

### 1.2 Masalah yang Diselesaikan
*   **Fragmentasi Data**: Proses perizinan vendor yang manual dan tidak terintegrasi dengan data legal (OSS/BPOM).
*   **Kurangnya Transparansi**: Sulitnya memonitor distribusi secara real-time dan valid (risiko laporan fiktif).
*   **Kelemahan Akuntabilitas**: Tidak adanya jejak audit (*audit trail*) yang kuat pada perubahan data sensitif.
*   **Responsivitas Rendah**: Pengaduan masyarakat seringkali tidak tertangani secara sistematis dan terukur.

### 1.3 Tujuan Utama (Goals)
1.  **Automated Onboarding**: Mempercepat verifikasi vendor melalui integrasi asinkron dengan sistem pemerintah.
2.  **Real-time Distribution Guard**: Mendeteksi anomali distribusi menggunakan AI berbasis probabilitas.
3.  **Public Trust**: Menyediakan kanal pengaduan transparan dengan sistem tracking tiket.
4.  **Enterprise Governance**: Menjamin keamanan data PII dan akuntabilitas penuh melalui audit trail dan ABAC.

---

## 2. User Personas
| Persona | Deskripsi | Kebutuhan Utama |
| :--- | :--- | :--- |
| **Vendor** | Pelaku usaha penyedia makanan | Pendaftaran mudah, upload dokumen, pelaporan distribusi harian, pengajuan banding AI. |
| **Verifikator BGN** | Staf Badan Gizi Nasional | Verifikasi dokumen legal, approval SIO, monitoring skor vendor. |
| **Pengawas Dinas** | Pejabat daerah (Provinsi/Kota) | Monitoring distribusi di wilayah scope-nya (ABAC), tindak lanjut pengaduan lokal. |
| **Admin Sistem** | IT Administrator | Manajemen user, konfigurasi role/permission, monitoring audit logs. |
| **Masyarakat** | Pengguna akhir/orang tua siswa | Melaporkan keluhan, mengecek keabsahan vendor via QR SIO. |

---

## 3. Functional Requirements

### 3.1 Modul 1: Portal Perizinan Vendor (Onboarding)
*   **FR1.1 Registrasi Vendor**: Vendor dapat mendaftar dengan menginput data usaha dan NIK penanggung jawab.
*   **FR1.2 Upload Dokumen Legal**: Sistem harus mendukung upload NIK, NIB, PIRT, Sertifikat Halal, dan Hygiene.
*   **FR1.3 Asynchronous Validation**: Sistem harus melakukan validasi dokumen ke API eksternal (OSS/BPOM/BPJPH) di background.
*   **FR1.4 SIO Digital**: Setelah diverifikasi, sistem menerbitkan SIO (Surat Izin Operasional) Digital dengan QR Code unik.
*   **FR1.5 PII Masking**: NIK penanggung jawab hanya boleh tampil utuh bagi Admin/Verifikator; untuk role lain harus di-mask (4 digit awal & akhir).

### 3.2 Modul 2: Monitoring Distribusi & AI Guard
*   **FR2.1 Pelaporan Harian**: Vendor wajib submit laporan harian yang mencakup: jumlah porsi, foto bukti, dan koordinat GPS.
*   **FR2.2 Geospatial Validation**: Sistem memvalidasi koordinat laporan terhadap radius lokasi sekolah yang ditentukan.
*   **FR2.3 Probabilistic Anomaly Detection**: AI menganalisis setiap laporan dan memberikan:
    *   `Anomaly Score` (0.0 - 1.0)
    *   `Confidence Level`
    *   `Risk Flag` (None, Low, Medium, High, Critical).
*   **FR2.4 Banding AI**: Vendor yang mendapat flag `High/Critical` dapat mengajukan banding dengan melampirkan bukti tambahan.
*   **FR2.5 Dynamic Vendor Scoring**: Perhitungan skor vendor berdasarkan ketepatan distribusi, hasil inspeksi, dan volume pengaduan.

### 3.3 Modul 3: Sistem Pengaduan Publik (Public Feedback)
*   **FR3.1 Public Complaint**: Masyarakat dapat mengirim pengaduan (anonim atau teridentifikasi) disertai foto dan lokasi.
*   **FR3.2 Ticket Tracking**: Setiap laporan mendapatkan nomor tiket unik untuk pelacakan status.
*   **FR3.3 Severity Scoring**: Sistem mengkategorikan pengaduan berdasarkan tingkat urgensi (Rendah → Kritis).
*   **FR3.4 Resolution Workflow**: Verifikator/Pengawas dapat memperbarui status pengaduan dan memberikan catatan penyelesaian.

---

## 4. Technical Infrastructure & Tech Stack (Research-Backed)
*   **Geospatial**: Menggunakan **PostGIS** dengan tipe data `GEOGRAPHY(Point, 4326)`. Validasi radius dilakukan via fungsi `ST_DWithin(report_loc, school_loc, radius_in_meters)`.
*   **Database Security**: Menggunakan **PostgreSQL RLS** dengan `SET LOCAL app.current_scope` untuk menjamin isolasi wilayah tingkat database.
*   **Asynchronous AI**: Menggunakan **Redis + ARQ/Celery** (Python) untuk antrean pemrosesan model anomali, mencegah *blocking* pada *main thread* API.
*   **PII Security**: Data NIK di-encrypt di database menggunakan **pgcrypto** dan di-masking secara dinamis di level **Next.js BFF** sebelum response dikirim ke klien.
*   **Policy Engine**: **Open Policy Agent (OPA)** untuk evaluasi ABAC (Attribute-Based Access Control) yang terpusat.

---

## 4. Non-Functional Requirements (The Architect's Standard)

### 4.1 Keamanan & Privasi (Security)
*   **Data Privacy**: Implementasi standar PII Masking pada seluruh layer API.
*   **Auditability**: Setiap aksi `WRITE` (POST, PATCH, DELETE) wajib mencatat: `Timestamp`, `ActorID`, `EntityID`, `OldValue`, dan `NewValue`.
*   **Access Control**: Menggunakan **ABAC (Attribute-Based Access Control)** untuk memastikan Pengawas Dinas hanya bisa mengakses data sesuai atribut wilayahnya (Provinsi/Kota).

### 4.2 Reliabilitas & Performa (Reliability)
*   **Idempotency**: Semua endpoint submit (Vendor & Distribusi) wajib mendukung `X-Idempotency-Key` untuk mencegah data ganda akibat *network lag*.
*   **Traffic Control**: Implementasi **Rate Limiting** per-user/per-IP untuk mencegah DDoS dan abuse API.
*   **Availability**: Sistem harus dirancang untuk *high availability* menggunakan *asynchronous worker* untuk proses berat (AI & Validasi OSS).

### 4.3 Integritas Data
*   **Geospatial Accuracy**: Koordinat GPS harus divalidasi terhadap *timestamp* untuk mencegah manipulasi lokasi (*GPS spoofing*).
*   **Probabilistic Output**: AI tidak boleh memberikan jawaban Boolean (True/False) secara mentah, melainkan skor probabilitas untuk mengurangi *false positive*.

---

## 5. User Flow (High Level)
1.  **Vendor Flow**: `Daftar` $\rightarrow$ `Upload Dokumen` $\rightarrow$ `Wait (Async Validation)` $\rightarrow$ `Verified` $\rightarrow$ `Terbit SIO` $\rightarrow$ `Lapor Distribusi Harian`.
2.  **Governance Flow**: `Laporan Masuk` $\rightarrow$ `AI Scan` $\rightarrow$ `Anomaly Detected` $\rightarrow$ `Notifikasi Pengawas` $\rightarrow$ `Inspeksi Lapangan/Banding Vendor` $\rightarrow$ `Update Skor Vendor`.
3.  **Public Flow**: `Scan QR SIO` $\rightarrow$ `Cek Keabsahan` $\rightarrow$ `Kirim Pengaduan` $\rightarrow$ `Track Tiket`.

---

## 6. Roadmap & Phases
*   **Phase 1 (MVP)**: Portal Perizinan (Basic), Pelaporan Distribusi (Basic), Pengaduan Publik (Basic), dan Auth RBAC.
*   **Phase 2 (Hardening)**: Integrasi API OSS/BPOM, Implementasi ABAC wilayah, Masking PII, dan Audit Trail.
*   **Phase 3 (Intelligence)**: AI Anomaly Detection (Probabilistik), Dynamic Scoring, dan Geospatial Radius Validation.
*   **Phase 4 (Optimization)**: Dashboard Analytics tingkat nasional, optimasi performa, dan integrasi notifikasi (WhatsApp/Email).

---

## 7. Success Metrics (KPIs)
*   **Onboarding Speed**: Penurunan waktu verifikasi vendor dari X hari menjadi Y jam (lewat automasi OSS).
*   **Fraud Reduction**: Persentase penurunan laporan distribusi fiktif yang berhasil dideteksi AI.
*   **Public Resolution Rate**: Persentase pengaduan masyarakat yang terselesaikan dalam SLA $\le$ 3 hari kerja.
*   **Data Integrity**: Nol insiden kebocoran PII (NIK) pada layer public API.
[H[2J[3J