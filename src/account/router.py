from fastapi import APIRouter, Depends

from src.account.dependencies import create_token, verify_token
from src.account.schemas import *
from src.account.service import *
from src.database import get_db
from src.dependencies import verify_admin
from src.schemes import ApiResponse

router = APIRouter()


@router.post("/create-admin", response_model=ApiResponse[AccountResponse])
async def create_account(data: CreateAccount, db: Session = Depends(get_db), allowed=Depends(verify_admin)):
    if allowed:
        user = await create(db, data)
        return ApiResponse(data=AccountResponse.from_account(account=user))


@router.post("/create", response_model=ApiResponse[AccountResponse])
async def create_account(data: CreateAccount, db: Session = Depends(get_db)):
    user = await create(db, data)
    return ApiResponse(data=AccountResponse.from_account(account=user))


@router.post("/login", response_model=ApiResponse[LoginResponse])
async def login(data: Login, db: Session = Depends(get_db)):
    user = await authenticate(db, data)
    token = await create_token(user.username)
    return ApiResponse(data=LoginResponse.from_account(account=user, token=token))


@router.post("/token", response_model=ApiResponse[LoginResponse])
async def refresh_token(data: RefreshToken, db: Session = Depends(get_db)):
    user = await verify_token(db, data.refresh_token)
    new_tokens = await create_token(user.username)
    account_response = LoginResponse(username=user.username, phone=user.phone, name=user.name, token=new_tokens)
    return ApiResponse(data=account_response)


@router.post("/change-password", response_model=ApiResponse[AccountResponse])
async def change_password(data: ChangePassword, user: Account = Depends(verify_token), db: Session = Depends(get_db)):
    updated_user = await update_password(db, data, user)
    account_response = AccountResponse(username=updated_user.username, phone=updated_user.phone, name=updated_user.name)
    return ApiResponse(data=account_response)


@router.post("/change-phone", response_model=ApiResponse[AccountResponse])
async def change_phone(data: ChangePhone, user: Account = Depends(verify_token), db: Session = Depends(get_db)):
    updated_user = await update_phone(db, data, user)
    account_response = AccountResponse(username=updated_user.username, phone=updated_user.phone, name=updated_user.name)
    return ApiResponse(data=account_response)


@router.post("/change-name", response_model=ApiResponse[AccountResponse])
async def change_name(data: ChangeName, user: Account = Depends(verify_token), db: Session = Depends(get_db)):
    updated_user = await update_name(db, data, user)
    account_response = AccountResponse(username=updated_user.username, phone=updated_user.phone, name=updated_user.name)
    return ApiResponse(data=account_response)


@router.post("/delete/{uid}", response_model=ApiResponse[bool])
async def delete_account(uid: str, user: Account = Depends(verify_token), db: Session = Depends(get_db)):
    succeed = await delete(db, uid, user)
    return ApiResponse(data={succeed: succeed})
