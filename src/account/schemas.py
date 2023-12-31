from pydantic import BaseModel

from src.account.models import Account
from src.schemes import ApiRequest


class CreateAccount(ApiRequest):
    username: str
    password: str
    phone: str
    name: str


class Login(ApiRequest):
    username: str
    password: str


class RefreshToken(ApiRequest):
    refresh_token: str


class ChangePassword(ApiRequest):
    old_password: str
    new_password: str


class ChangePhone(ApiRequest):
    new_phone: str


class ChangeName(ApiRequest):
    new_name: str


class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AccountResponse(BaseModel):
    username: str
    phone: str
    name: str

    @classmethod
    def from_account(cls, account: Account):
        return cls(username=account.username, phone=account.phone, name=account.name)


class LoginResponse(BaseModel):
    username: str
    phone: str
    name: str
    token: TokenData

    @classmethod
    def from_account(cls, account: Account, token: TokenData):
        return cls(username=account.username, phone=account.phone, name=account.name, token=token)
