from pydantic import BaseModel

from src.address.models import Address


class AddressCreate(BaseModel):
    village: str
    sub_district: str
    district: str
    regency: str
    province: str


class AddressResponse(AddressCreate):
    id: str

    @classmethod
    def from_db(cls, address: Address):
        return cls(id=address.id, village=address.village, sub_district=address.sub_district, district=address.district,
                   regency=address.regency, province=address.province)
