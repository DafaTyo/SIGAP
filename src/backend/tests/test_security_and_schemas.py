from app.core.security import mask_nik
from app.schemas.vendor import VendorOut
from app.schemas.auth import PermissionScope


def test_mask_nik_shows_first_and_last_four_digits_only():
    assert mask_nik("3175123412345678") == "3175********5678"


def test_mask_nik_handles_short_values_safely():
    assert mask_nik("12345678") == "********"


def test_vendor_out_exposes_masked_nik():
    vendor = VendorOut(
        id="vendor-1",
        nama_usaha="SPPG Contoh",
        nik_penanggung_jawab="3175123412345678",
        nib="1234567890123",
        alamat="Jl. Contoh",
        provinsi="DKI Jakarta",
        kabupaten_kota="Jakarta Pusat",
        status="verified",
    )

    assert vendor.nik_penanggung_jawab_masked == "3175********5678"


def test_permission_scope_supports_multi_scope_values():
    scope = PermissionScope(type="provinsi", value=["DKI Jakarta", "Jawa Barat"])
    assert scope.value == ["DKI Jakarta", "Jawa Barat"]
