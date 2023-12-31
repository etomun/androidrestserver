from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.address.service import create_address, search, get_address, get_addresses, update_address
from src.database import SessionLocal

router = APIRouter()


@router.post("/add")
def create_address_route(village: str, district: str, line: str, db: Session = Depends(SessionLocal)):
    return create_address(db, village=village, district=district, line=line)


@router.get("/")
def search_address(keyword: str = Query(..., min_length=3), db: Session = Depends(SessionLocal)):
    addresses = search(db, keyword=keyword)
    if not addresses:
        raise HTTPException(status_code=404, detail=f"No addresses found for keyword: {keyword}")
    return addresses


@router.get("/{address_id}")
def read_address(address_id: int, db: Session = Depends(SessionLocal)):
    db_address = get_address(db, address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@router.get("/")
def read_addresses(skip: int = 0, limit: int = 10, db: Session = Depends(SessionLocal)):
    return get_addresses(db, skip=skip, limit=limit)


@router.put("/{address_id}")
def update_address_route(address_id: int, village: str, district: str, line: str, db: Session = Depends(SessionLocal)):
    db_address = update_address(db, address_id, village=village, district=district, line=line)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address
