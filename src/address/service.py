from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.address.models import Address
from src.address.schemas import AddressCreate


async def add(db: Session, data: List[AddressCreate]):
    added_addresses = []

    try:
        for new_address in data:
            existing_address = db.execute(select(Address).filter_by(village=new_address.village)).first()

            if existing_address:
                raise HTTPException(status_code=400,
                                    detail=f"Address with village '{new_address.village}' already exists")

            address_model = Address(**new_address.model_dump())
            db.add(address_model)
            db.commit()
            db.refresh(address_model)
            added_addresses.append(address_model)

    except Exception as e:
        db.rollback()
        raise e
    return added_addresses


async def get_by_id(db: Session, address_id: str):
    address = db.query(Address).filter_by(id=address_id).first()
    if not address:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Data not found")
    return address


async def get_all(db: Session):
    addresses = db.query(Address).all()
    return addresses


async def search(db: Session, keyword: str):
    addresses = db.query(Address).filter(
        (Address.village.ilike(f"%{keyword}%")) |
        (Address.district.ilike(f"%{keyword}%"))
    ).all()
    return addresses


async def update(db: Session, address_id: str, data: AddressCreate):
    address = db.query(Address).filter_by(id=address_id).first()
    if not address:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Data not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(address, field, value)
    db.commit()
    db.refresh(address)
    return address


async def clear(db: Session):
    try:
        db.execute(Address.__table__.delete())
        db.commit()
        return {"message": "Table cleared successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error clearing table: {str(e)}")
