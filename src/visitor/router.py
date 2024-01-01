from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.visitor.schemas import VisitorCreate, ChangeName, SetRelatives, ChangeAddress
from src.visitor.service import add, get_by_code, get_all, update_name, update_address, update_relatives

router = APIRouter()


@router.post("/register")
def register_visitor(data: VisitorCreate, db: Session = Depends(get_db)):
    return add(db, data)


@router.get("/{visitor_code}")
def get_visitor(visitor_code: str, db: Session = Depends(get_db)):
    return get_by_code(db, visitor_code)


@router.get("/")
def get_visitors(db: Session = Depends(get_db)):
    return get_all(db)


@router.post("/change-name")
def change_name(data: ChangeName, db: Session = Depends(get_db)):
    return update_name(db, data)


@router.post("/change-address")
def change_address(data: ChangeAddress, db: Session = Depends(get_db)):
    return update_address(db, data)


@router.post("/change-relatives")
def change_relatives(data: SetRelatives, db: Session = Depends(get_db)):
    return update_relatives(db, data)
