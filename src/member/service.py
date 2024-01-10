from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from starlette import status

from src.account.models import Account
from src.member.models import Member
from src.member.schemas import MemberCreate, ChangeName, ChangeAddress, SetRelatives


async def add(db: Session, data: MemberCreate, pic: Account):
    if db.query(Member).filter_by(unique_code=data.unique_code).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Code already registered")

    db_member = Member(unique_code=data.unique_code,
                       name=data.name,
                       gender=data.gender,
                       age=data.age,
                       is_relatives=data.is_relatives,
                       address_id=data.address_id,
                       pic_id=pic.id)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


async def bulk_insert(db: Session, datas: List[MemberCreate], pic: Account):
    members = [Member(unique_code=data.unique_code,
                      name=data.name,
                      gender=data.gender,
                      age=data.age,
                      is_relatives=data.is_relatives,
                      address_id=data.address_id,
                      pic_id=pic.id) for data in datas]
    db.add_all(members)
    db.commit()
    return members


async def delete(db: Session, unique_code: str) -> bool:
    member = db.query(Member).filter_by(unique_code=unique_code).first()
    if member is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Member Not Found")
    try:
        db.delete(member)
        db.commit()
        return True
    except:
        return False


async def check_existed(db: Session, member_code: str) -> bool:
    member = db.query(Member).filter_by(unique_code=member_code).first()
    return member is not None


async def get_by_code(db: Session, unique_code: str):
    return (db.query(Member)
            .filter_by(unique_code=unique_code)
            .options(joinedload(Member.address), joinedload(Member.pic))
            .first())


async def filtered(db: Session, gender: str, is_relatives: bool = False):
    return (db.query(Member)
            .filter_by(gender=gender, is_relatives=is_relatives)
            .options(joinedload(Member.address), joinedload(Member.pic))
            .all())


async def get_all(db: Session):
    return (db.query(Member)
            .options(joinedload(Member.address), joinedload(Member.pic))
            .all())


async def update_name(db: Session, data: ChangeName):
    db_member = db.query(Member).filter_by(unique_code=data.member_code).first()
    if db_member:
        db_member.name = data.name
        db.commit()
        db.refresh(db_member)
    else:
        raise HTTPException(status_code=404, detail="Member not Found")
    return db_member


async def update_address(db: Session, data: ChangeAddress):
    db_member = db.query(Member).filter_by(unique_code=data.member_code).first()
    if db_member:
        db_member.address_id = data.address_id
        db.commit()
        db.refresh(db_member)
    else:
        raise HTTPException(status_code=404, detail="Member not Found")
    return db_member


async def update_relatives(db: Session, data: SetRelatives):
    db_member = db.query(Member).filter_by(unique_code=data.member_code).first()
    if db_member:
        db_member.is_relatives = data.is_relative
        db.commit()
        db.refresh(db_member)
    else:
        raise HTTPException(status_code=404, detail="Member not Found")
    return db_member


async def clear(db: Session):
    try:
        db.execute(Member.__table__.delete())
        db.commit()
        return {"message": "Table cleared successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error clearing table: {str(e)}")
