import type { PaginatedResponse } from './api';

export const VENDOR_STATUS = {
  PENDING_VERIFICATION: 'pending_verification',
  VERIFIED: 'verified',
  REJECTED: 'rejected',
  SUSPENDED: 'suspended',
} as const;

export type VendorStatus = (typeof VENDOR_STATUS)[keyof typeof VENDOR_STATUS];

export interface VendorCreate {
  nama_usaha: string;
  nik_penanggung_jawab: string;
  nib: string;
  alamat: string;
  provinsi: string;
  kabupaten_kota: string;
  kontak_telepon?: string;
}

export interface VendorUpdate {
  alamat?: string;
  kontak_telepon?: string;
}

export interface Vendor {
  id: string;
  nama_usaha: string;
  nik_penanggung_jawab_masked: string;
  nib: string;
  alamat: string;
  provinsi: string;
  kabupaten_kota: string;
  status: VendorStatus;
  vendor_score: number;
  created_at: string;
  updated_at: string;
}

export type VendorListResponse = PaginatedResponse<Vendor>;
