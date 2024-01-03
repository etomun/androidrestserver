from pydantic import BaseModel

from src.account.models import Account


class AccountLogin(BaseModel):
    username: str
    password: str


class AccountCreate(AccountLogin):
    phone: str
    name: str


class RefreshToken(BaseModel):
    refresh_token: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class ChangePhone(BaseModel):
    new_phone: str


class ChangeName(BaseModel):
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
    id: str
    username: str
    phone: str
    name: str
    token: TokenData

    @classmethod
    def from_account(cls, account: Account, token: TokenData):
        return cls(id=account.id, username=account.username, phone=account.phone, name=account.name, token=token)
