from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.visitor.service import create_visitor, get_visitor, get_visitors, update_visitor

router = APIRouter()


@router.post("/visitors/")
def create_visitor_route(name: str, gender: str, age: int, is_relatives: bool, address_id: int,
                         db: Session = Depends(SessionLocal)):
    return create_visitor(db, name=name, gender=gender, age=age, is_relatives=is_relatives, address_id=address_id)


@router.get("/visitors/{visitor_id}")
def read_visitor(visitor_id: int, db: Session = Depends(SessionLocal)):
    db_visitor = get_visitor(db, visitor_id)
    if db_visitor is None:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return db_visitor


@router.get("/visitors/")
def read_visitors(skip: int = 0, limit: int = 10, db: Session = Depends(SessionLocal)):
    return get_visitors(db, skip=skip, limit=limit)


@router.put("/visitors/{visitor_id}")
def update_visitor_route(visitor_id: int, name: str, gender: str, age: int, is_relatives: bool, address_id: int,
                         db: Session = Depends(SessionLocal)):
    db_visitor = update_visitor(db, visitor_id, name=name, gender=gender, age=age, is_relatives=is_relatives,
                                address_id=address_id)
    if db_visitor is None:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return db_visitor
