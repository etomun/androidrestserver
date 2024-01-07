import logging
from typing import List

from fastapi import APIRouter, Depends

from src.account.dependencies import create_token
from src.account.schemas import *
from src.account.service import *
from src.database import get_db
from src.dependencies import verify_token_su, verify_account, verify_admin
from src.schemes import ApiResponse

router = APIRouter()


@router.post("/create-admin", response_model=ApiResponse[AccountResponse])
async def create_admin_su(data: AccountCreate, db: Session = Depends(get_db), admin_only=Depends(verify_token_su)):
    if admin_only:
        user = await create(db, data, True)
        return ApiResponse(data=AccountResponse.from_db(account=user))
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not Allowed")


@router.post("/create", response_model=ApiResponse[AccountResponse])
async def create_account(data: AccountCreate, db: Session = Depends(get_db), admin: Account = Depends(verify_admin)):
    user = await create(db, data, False, pic_id=admin.id)
    return ApiResponse(data=AccountResponse.from_db(account=user))


@router.get("/fetch-accounts", response_model=ApiResponse[List[AccountResponse]])
async def get_all_account(db: Session = Depends(get_db), admin: Account = Depends(verify_admin)):
    logging.info(admin.username)
    users = await get_accounts(db)
    if not users:
        return ApiResponse(data=[], error_message="Users not found")
    else:
        return ApiResponse(data=[AccountResponse.from_db(account=usr) for usr in users])


@router.post("/login", response_model=ApiResponse[LoginResponse])
async def login(data: AccountLogin, db: Session = Depends(get_db)):
    user = await authenticate(db, data)
    if not user:
        return ApiResponse(data=None, error_message="User not found")
    else:
        token = await create_token(user.username)
        return ApiResponse(data=LoginResponse.from_account(account=user, token=token))


@router.post("/token", response_model=ApiResponse[LoginResponse])
async def refresh_token(data: RefreshToken, db: Session = Depends(get_db)):
    user = await verify_account(db, data.refresh_token)
    if not user:
        return ApiResponse(data=None, error_message="User not found")
    else:
        new_tokens = await create_token(user.username)
        return ApiResponse(data=LoginResponse.from_account(account=user, token=new_tokens))


@router.post("/change-password", response_model=ApiResponse[AccountResponse])
async def change_password(data: ChangePassword, user: Account = Depends(verify_account), db: Session = Depends(get_db)):
    updated_user = await update_password(db, data, user)
    if not updated_user:
        return ApiResponse(data=None, error_message="User not found")
    else:
        return ApiResponse(data=AccountResponse.from_db(updated_user))


@router.post("/change-phone", response_model=ApiResponse[AccountResponse])
async def change_phone(data: ChangePhone, user: Account = Depends(verify_account), db: Session = Depends(get_db)):
    updated_user = await update_phone(db, data, user)
    if not updated_user:
        return ApiResponse(data=None, error_message="User not found")
    else:
        return ApiResponse(data=AccountResponse.from_db(updated_user))


@router.post("/change-name", response_model=ApiResponse[AccountResponse])
async def change_name(data: ChangeName, user: Account = Depends(verify_account), db: Session = Depends(get_db)):
    updated_user = await update_name(db, data, user)
    if not updated_user:
        return ApiResponse(data=None, error_message="User not found")
    else:
        return ApiResponse(data=AccountResponse.from_db(updated_user))


@router.post("/delete/{uid}", response_model=ApiResponse[bool])
async def delete_account(uid: str, user: Account = Depends(verify_account), db: Session = Depends(get_db)):
    succeed = await delete(db, uid, user)
    return ApiResponse(data={succeed: succeed})


@router.post('/clear')
async def clear_accounts(db: Session = Depends(get_db), user: Account = Depends(verify_admin)):
    logging.info(user.username)
    result = await clear(db)
    return ApiResponse(data=result)
