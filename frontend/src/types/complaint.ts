import type { PaginatedResponse } from './api';

export interface ComplaintCreate {
  vendor_id: string;
  kategori: 'keracunan' | 'keterlambatan' | 'kekurangan_porsi' | 'kualitas_makanan' | 'lainnya';
  deskripsi: string;
  nama_pelapor?: string;
  latitude?: number;
  longitude?: number;
  distribution_id?: string;
  tanggal_kejadian?: string;
}

export interface Complaint {
  id: string;
  ticket_number: string;
  vendor_id: string;
  kategori: string;
  deskripsi: string;
  severity: 'rendah' | 'sedang' | 'tinggi' | 'kritis';
  status: 'baru' | 'diproses' | 'ditindaklanjuti' | 'ditutup';
  resolution_notes?: string | null;
  created_at: string;
  sla_deadline: string;
}

export type ComplaintListResponse = PaginatedResponse<Complaint>;
