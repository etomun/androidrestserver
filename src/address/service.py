from sqlalchemy.orm import Session

from src.address.models import Address


def create_address(db: Session, village: str, district: str, line: str):
    db_address = Address(village=village, district=district, line=line)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def get_address(db: Session, address_id: int):
    return db.query(Address).filter(Address.id == address_id).first()


def search(db: Session, keyword: str):
    return db.query(Address).filter(
        (Address.village.ilike(f"%{keyword}%")) |
        (Address.district.ilike(f"%{keyword}%"))
    ).all()


def get_addresses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Address).offset(skip).limit(limit).all()


def update_address(db: Session, address_id: int, village: str, district: str, line: str):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address:
        db_address.village = village
        db_address.district = district
        db_address.line = line
        db.commit()
        db.refresh(db_address)
    return db_address
