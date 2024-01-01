from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.visitor.models import Visitor
from src.visitor.schemas import VisitorCreate, ChangeName, ChangeAddress, SetRelatives


def add(db: Session, data: VisitorCreate):
    if db.query(Visitor).filter(Visitor.unique_code == data.unique_code).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID Card already registered")

    db_visitor = Visitor(name=data.name,
                         gender=data.gender,
                         age=data.age,
                         is_relatives=data.is_relatives,
                         address_id=data.address_id)
    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)
    return db_visitor


def get_by_code(db: Session, unique_code: str):
    return db.query(Visitor).filter(Visitor.unique_code == unique_code).first()


def get_all(db: Session):
    return db.query(Visitor).all()


def update_name(db: Session, data: ChangeName):
    db_visitor = db.query(Visitor).filter(Visitor.unique_code == data.visitor_code).first()
    if db_visitor:
        db_visitor.name = data.name
        db.commit()
        db.refresh(db_visitor)
    else:
        raise HTTPException(status_code=404, detail="Visitor not Found")
    return db_visitor


def update_address(db: Session, data: ChangeAddress):
    db_visitor = db.query(Visitor).filter(Visitor.unique_code == data.visitor_code).first()
    if db_visitor:
        db_visitor.address = data.address
        db.commit()
        db.refresh(db_visitor)
    else:
        raise HTTPException(status_code=404, detail="Visitor not Found")
    return db_visitor


def update_relatives(db: Session, data: SetRelatives) -> Visitor:
    db_visitor = db.query(Visitor).filter(Visitor.unique_code == data.visitor_code).first()
    if db_visitor:
        db_visitor.is_relatives = data.is_relative
        db.commit()
        db.refresh(db_visitor)
    else:
        raise HTTPException(status_code=404, detail="Visitor not Found")
    return db_visitor
