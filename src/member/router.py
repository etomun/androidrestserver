import logging
from typing import List

from fastapi import APIRouter, Depends

from src.database import get_db
from src.dependencies import verify_admin, verify_account
from src.schemes import ApiResponse
from src.member.schemas import MemberResponse
from src.member.service import *

router = APIRouter()


@router.post("/register", response_model=ApiResponse[MemberResponse])
async def register_member(data: MemberCreate, db: Session = Depends(get_db), pic: Account = Depends(verify_account)):
    member = await add(db, data, pic)
    if not member:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to add Member")
    return ApiResponse(data=MemberResponse.from_db(member))


@router.post("/delete/{unique_code}", response_model=ApiResponse[bool])
async def delete_member(unique_code: str, db: Session = Depends(get_db), admin: Account = Depends(verify_admin)):
    logging.info(admin.id)
    success = await delete(db, unique_code)
    return ApiResponse(data=success)


@router.get("/check/{member_code}", response_model=ApiResponse[bool])
async def check_member_existed(member_code: str, db: Session = Depends(get_db)):
    is_existed = await check_existed(db, member_code)
    return ApiResponse(data=is_existed)


@router.get("/{member_code}", response_model=ApiResponse[MemberResponse])
async def get_member(member_code: str, db: Session = Depends(get_db)):
    member = await get_by_code(db, member_code)
    if not member:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Member Not found")
    return ApiResponse(data=MemberResponse.from_db(member))


@router.get("/", response_model=ApiResponse[List[MemberResponse]])
async def get_all_members(db: Session = Depends(get_db)):
    members = await get_all(db)
    if not members:
        return ApiResponse(data=[])
    return ApiResponse(data=[MemberResponse.from_db(v) for v in members])


@router.get("", response_model=ApiResponse[List[MemberResponse]])
async def get_members_by_category(gender: str = "male", is_relatives: bool = False, db: Session = Depends(get_db)):
    members = await filtered(db, gender, is_relatives)
    if not members:
        return ApiResponse(data=[])
    return ApiResponse(data=[MemberResponse.from_db(v) for v in members])


@router.post("/change-name", response_model=ApiResponse[MemberResponse])
async def change_name(data: ChangeName, db: Session = Depends(get_db)):
    member = await update_name(db, data)
    if not member:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Member Not found")
    return ApiResponse(data=MemberResponse.from_db(member))


@router.post("/change-address", response_model=ApiResponse[MemberResponse])
async def change_address(data: ChangeAddress, db: Session = Depends(get_db)):
    member = await update_address(db, data)
    if not member:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Member Not found")
    return ApiResponse(data=MemberResponse.from_db(member))


@router.post("/change-relatives", response_model=ApiResponse[MemberResponse])
async def change_relatives(data: SetRelatives, db: Session = Depends(get_db)):
    member = await update_relatives(db, data)
    if not member:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Member Not found")
    return ApiResponse(data=MemberResponse.from_db(member))


@router.post('/clear')
async def clear_members(db: Session = Depends(get_db), user: Account = Depends(verify_admin)):
    logging.info(user.username)
    result = await clear(db)
    return ApiResponse(data=result)
