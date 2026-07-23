from pydantic import BaseModel

class APIError(BaseModel):
    code: int
    detail: str
