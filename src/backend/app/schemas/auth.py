from pydantic import BaseModel, Field


class PermissionScope(BaseModel):
    type: str = Field(..., examples=["provinsi", "kabupaten_kota"])
    value: list[str]
