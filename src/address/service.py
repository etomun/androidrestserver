from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.address.models import Address
from src.address.schemas import AddressCreate


async def add(db: Session, data: list[AddressCreate]):
    try:
        address_dict = [user.model_dump() for user in data]
        db.bulk_save_objects(address_dict)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return True


async def get_by_id(db: Session, address_id: str):
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Data not found")


async def search(db: Session, keyword: str):
    addresses = db.query(Address).filter(
        (Address.village.ilike(f"%{keyword}%")) |
        (Address.district.ilike(f"%{keyword}%"))
    ).all()
    return addresses


async def update(db: Session, address_id: str, data: AddressCreate):
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Data not found")
    if address:
        address.village = data.village
        address.district = data.district
        address.line = data.line
        db.commit()
        db.refresh(address)
    return address
