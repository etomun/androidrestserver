from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.visitor.service import create, get_by_id, update

router = APIRouter()


@router.post("/create")
def create_visitor(name: str, gender: str, age: int, is_relatives: bool, address_id: int,
                   db: Session = Depends(SessionLocal)):
    return create(db, name=name, gender=gender, age=age, is_relatives=is_relatives, address_id=address_id)


@router.get("/{visitor_id}")
def get_visitor(visitor_id: int, db: Session = Depends(SessionLocal)):
    db_visitor = get_by_id(db, visitor_id)
    if db_visitor is None:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return db_visitor


@router.put("/visitors/{visitor_id}")
def update_visitor(visitor_id: int, name: str, gender: str, age: int, is_relatives: bool, address_id: int,
                   db: Session = Depends(SessionLocal)):
    db_visitor = update(db, visitor_id, name=name, gender=gender, age=age, is_relatives=is_relatives,
                        address_id=address_id)
    if db_visitor is None:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return db_visitor
