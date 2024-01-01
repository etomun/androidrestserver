from pydantic import BaseModel


class AddressCreate(BaseModel):
    village: str
    district: str
    line: str


class AddressResponse(AddressCreate):
    id: str
