from src.schemes import ApiRequest


class VisitorCreate(ApiRequest):
    unique_code: str
    name: str
    gender: str
    age: int
    is_relatives: bool
    address_id: int


class VisitorResponse(VisitorCreate):
    id: str


class ChangeName(ApiRequest):
    visitor_code: str
    name: str


class ChangeAddress(ApiRequest):
    visitor_code: str
    address: str


class SetRelatives(ApiRequest):
    visitor_code: str
    is_relative: bool
