"""PII utilities: mask, encrypt, decrypt NIK."""

from __future__ import annotations
from enum import Enum

class DataClass(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

def mask_nik(nik: str) -> str:
    if len(nik) < 8:
        half = len(nik) // 2
        return nik[:half] + "*" * half + nik[half*2:]
    return nik[:4] + "*" * 8 + nik[-4:]

def encrypt_nik(plain_nik: str) -> bytes:
    raise NotImplementedError("Requires active DB session")

def decrypt_nik(cipher_bytes: bytes) -> str:
    raise NotImplementedError("Requires active DB session")
