from src.schemes import ApiRequest


class AddressCreate(ApiRequest):
    village: str
    district: str
    line: str


class AddressResponse(AddressCreate):
    id: str
