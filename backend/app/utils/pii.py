"""PII utilities: mask, encrypt, decrypt NIK.
Uses PostgreSQL pgcrypto in production, Fernet (symmetric) for SQLite/test.
"""

from __future__ import annotations

from enum import Enum

from app.core.config import settings


class DataClass(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


def mask_nik(nik: str) -> str:
    """Menerapkan pola masking pada NIK: 4 digit awal + 8 bintang + 4 digit akhir.

    Contoh: '3175********1234' (NIK Indonesia 16 digit)
    """
    if len(nik) < 8:
        half = len(nik) // 2
        return nik[:half] + "*" * half + nik[half * 2 :]
    return nik[:4] + "*" * 8 + nik[-4:]


async def encrypt_nik(plain_nik: str, db_session=None) -> bytes:
    """Enkripsi NIK — PostgreSQL pgcrypto (production) or Fernet (SQLite/test)."""
    if settings.ENV == "test" or "sqlite" in settings.DATABASE_URL:
        from cryptography.fernet import Fernet
        return Fernet(settings.NIK_ENCRYPTION_KEY.encode()).encrypt(plain_nik.encode())
    from sqlalchemy import text
    sql = "SELECT pgp_sym_encrypt(:plain_nik, :key) as encrypted;"
    result = await db_session.execute(text(sql), {"plain_nik": plain_nik, "key": settings.NIK_ENCRYPTION_KEY})
    encrypted = result.scalar()
    if encrypted is None:
        raise ValueError("pgp_sym_encrypt returned NULL")
    return bytes(encrypted)


async def decrypt_nik(cipher_bytes: bytes, db_session=None) -> str:
    """Dekripsi NIK."""
    if settings.ENV == "test" or "sqlite" in settings.DATABASE_URL:
        from cryptography.fernet import Fernet
        return Fernet(settings.NIK_ENCRYPTION_KEY.encode()).decrypt(cipher_bytes).decode()
    from sqlalchemy import text
    sql = "SELECT pgp_sym_decrypt(:encrypted, :key) as decrypted;"
    result = await db_session.execute(text(sql), {"encrypted": cipher_bytes, "key": settings.NIK_ENCRYPTION_KEY})
    decrypted = result.scalar()
    return str(decrypted) if decrypted else ""
