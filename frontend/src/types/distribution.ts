import type { PaginatedResponse } from './api';

export interface DistributionCreate {
  vendor_id: string;
  jumlah_porsi: number;
  lokasi_sekolah?: string;
  latitude: number;
  longitude: number;
  metadata?: {
    capture_time: string;
    exif_timestamp?: string;
    device_id?: string;
  };
}

export interface Distribution {
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
    flag: 'none' | 'low_risk' | 'medium_risk' | 'high_risk' | 'critical';
    detected: boolean;
    details: string[];
    appeal_status: 'none' | 'pending_review' | 'in_progress' | 'resolved' | 'rejected';
    is_frozen: boolean;
  } | null;
}

export type DistributionListResponse = PaginatedResponse<Distribution>;
