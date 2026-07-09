from pydantic import BaseModel, Field

from app.core.security import mask_nik


class VendorOut(BaseModel):
    id: str
    nama_usaha: str
    nik_penanggung_jawab: str
    nib: str
    alamat: str
    provinsi: str
    kabupaten_kota: str
    status: str

    @property
    def nik_penanggung_jawab_masked(self) -> str:
        return mask_nik(self.nik_penanggung_jawab)
