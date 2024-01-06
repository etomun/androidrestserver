from pydantic import BaseModel
from pydantic.v1 import validator

from src.account.schemas import AccountResponse
from src.address.schemas import AddressResponse
from src.member.models import Member, Gender


class MemberCreate(BaseModel):
    unique_code: str
    name: str
    gender: str
    age: int
    is_relatives: bool
    address_id: str

    @validator('gender')
    def validate_gender(cls, value):
        try:
            return Gender(value.upper()).value
        except ValueError:
            return Gender.OTHER.value


class MemberResponse(MemberCreate):
    id: str
    pic_id: str
    address: AddressResponse
    pic: AccountResponse

    @classmethod
    def from_db(cls, member: Member):
        address = AddressResponse.from_db(member.address)
        pic = AccountResponse.from_db(member.pic)
        return cls(id=member.id,
                   address_id=member.address_id,
                   pic_id=member.pic_id,
                   unique_code=member.unique_code,
                   name=member.name,
                   gender=member.gender,
                   age=member.age,
                   is_relatives=member.is_relatives,
                   address=address,
                   pic=pic)


class ChangeName(BaseModel):
    member_code: str
    name: str


class ChangeAddress(BaseModel):
    member_code: str
    address_id: str


class SetRelatives(BaseModel):
    member_code: str
    is_relative: bool
