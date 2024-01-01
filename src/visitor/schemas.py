from pydantic import BaseModel


class VisitorCreate(BaseModel):
    unique_code: str
    name: str
    gender: str
    age: int
    is_relatives: bool
    address_id: str


class VisitorResponse(VisitorCreate):
    id: str


class ChangeName(BaseModel):
    visitor_code: str
    name: str


class ChangeAddress(BaseModel):
    visitor_code: str
    address: str


class SetRelatives(BaseModel):
    visitor_code: str
    is_relative: bool
