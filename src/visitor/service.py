from sqlalchemy.orm import Session

from src.visitor.models import Visitor


def create_visitor(db: Session, unique_code: str, name: str, gender: str, age: int, is_relatives: bool,
                   address_id: int):
    # Avoid double visitor
    existing_visitor = db.query(Visitor).filter(Visitor.unique_code == unique_code).first()
    if existing_visitor:
        return None

    db_visitor = Visitor(name=name, gender=gender, age=age, is_relatives=is_relatives, address_id=address_id)
    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)
    return db_visitor


def get_visitor(db: Session, unique_code: int):
    return db.query(Visitor).filter(Visitor.id == unique_code).first()


def get_visitors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Visitor).offset(skip).limit(limit).all()


def update_visitor(db: Session, visitor_id: int, unique_code: str, name: str, gender: str, age: int, is_relatives: bool,
                   address_id: int):
    db_visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if db_visitor:
        db_visitor.unique_code = unique_code
        db_visitor.name = name
        db_visitor.gender = gender
        db_visitor.age = age
        db_visitor.is_relatives = is_relatives
        db_visitor.address_id = address_id
        db.commit()
        db.refresh(db_visitor)
    return db_visitor
