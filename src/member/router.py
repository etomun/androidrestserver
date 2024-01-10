import logging

from fastapi import APIRouter, Depends

from src.database import get_db
from src.dependencies import verify_admin, verify_account
from src.member.schemas import MemberResponse
from src.member.service import *
from src.schemes import ApiResponse

router = APIRouter()


@router.post("/register", response_model=ApiResponse[MemberResponse])
async def register_member(data: MemberCreate, db: Session = Depends(get_db), pic: Account = Depends(verify_account)):
    member = await add(db, data, pic)
    if not member:
        return ApiResponse(data=None, error_message="Failed to create member")
    else:
        return ApiResponse(data=MemberResponse.from_db(member))


@router.post("/batch-register", response_model=ApiResponse[List[MemberResponse]])
async def bulk_reg_male_members(codes: List[str], address_id: str, db: Session = Depends(get_db),
                                pic: Account = Depends(verify_account)):
    datas = [MemberCreate(
        unique_code=code,
        name="",
        gender="male",
        age=0,
        is_relatives=False,
        address_id=address_id
    ) for code in codes]
    members = await bulk_insert(db, datas, pic)
    if not members:
        return ApiResponse(data=None, error_message="Failed to create member")
    else:
        return ApiResponse(data=[MemberResponse.from_db(member) for member in members])


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
        return ApiResponse(data=None, error_message="Member not found")
    else:
        return ApiResponse(data=MemberResponse.from_db(member))


@router.get("/", response_model=ApiResponse[List[MemberResponse]])
async def get_all_members(db: Session = Depends(get_db)):
    members = await get_all(db)
    if not members:
        return ApiResponse(data=[], error_message="No members")
    else:
        return ApiResponse(data=[MemberResponse.from_db(v) for v in members])


@router.get("", response_model=ApiResponse[List[MemberResponse]])
async def get_members_by_category(gender: str = "male", is_relatives: bool = False, db: Session = Depends(get_db)):
    members = await filtered(db, gender, is_relatives)
    if not members:
        return ApiResponse(data=[], error_message="No members")
    else:
        return ApiResponse(data=[MemberResponse.from_db(v) for v in members])


@router.post("/change-name", response_model=ApiResponse[MemberResponse])
async def change_name(data: ChangeName, db: Session = Depends(get_db)):
    member = await update_name(db, data)
    if not member:
        return ApiResponse(data=None, error_message="Member not found")
    else:
        return ApiResponse(data=MemberResponse.from_db(member))


@router.post("/change-address", response_model=ApiResponse[MemberResponse])
async def change_address(data: ChangeAddress, db: Session = Depends(get_db)):
    member = await update_address(db, data)
    if not member:
        return ApiResponse(data=None, error_message="Member not found")
    else:
        return ApiResponse(data=MemberResponse.from_db(member))


@router.post("/change-relatives", response_model=ApiResponse[MemberResponse])
async def change_relatives(data: SetRelatives, db: Session = Depends(get_db)):
    member = await update_relatives(db, data)
    if not member:
        return ApiResponse(data=None, error_message="Member not found")
    else:
        return ApiResponse(data=MemberResponse.from_db(member))


@router.post('/clear')
async def clear_members(db: Session = Depends(get_db), user: Account = Depends(verify_admin)):
    logging.info(user.username)
    result = await clear(db)
    return ApiResponse(data=result)
