// 1:1 dengan api-contract.yaml v0.2.0
// — semua tipe request/response

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
}

export interface MeResponse {
  id: string;
  role: string;
  scope_type: string;
  scope_value: string[];
}

export interface PermissionsResponse {
  role: string;
  permissions: string[];
  scope: { type: string; value: string[] };
}

export interface Pagination {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: Pagination;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>[];
}
