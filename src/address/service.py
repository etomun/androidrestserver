from sqlalchemy.orm import Session

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


async def get_by_id(db: Session, address_id: int):
    return db.query(Address).filter(Address.id == address_id).first()


async def search(db: Session, keyword: str):
    addresses = db.query(Address).filter(
        (Address.village.ilike(f"%{keyword}%")) |
        (Address.district.ilike(f"%{keyword}%"))
    ).all()
    return addresses


async def update(db: Session, address_id: int, data: AddressCreate):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address:
        db_address.village = data.village
        db_address.district = data.district
        db_address.line = data.line
        db.commit()
        db.refresh(db_address)
    return db_address.to_response()
