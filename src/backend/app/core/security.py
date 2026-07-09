def mask_nik(nik: str) -> str:
    """Mask NIK/PII: tampilkan 4 digit awal dan 4 digit akhir, sisanya bintang.

    Jika panjang kurang dari 8, sembunyikan seluruh nilai untuk keamanan.
    """
    if not nik:
        return ""
    if len(nik) <= 8:
        return "*" * len(nik)
    return f"{nik[:4]}{'*' * (len(nik) - 8)}{nik[-4:]}"
