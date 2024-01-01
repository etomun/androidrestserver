from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.address.schemas import AddressCreate
from src.address.service import add, search, get_by_id, update
from src.database import SessionLocal

router = APIRouter()


@router.post("/add-bulk")
async def add_address_bulk(data: list[AddressCreate], db: Session = Depends(SessionLocal)):
    return await add(db, data)


@router.post("/add")
async def add_address(data: AddressCreate, db: Session = Depends(SessionLocal)):
    return await add(db, [data])


@router.get("/search")
async def search_address(keyword: str = Query(..., min_length=3), db: Session = Depends(SessionLocal)):
    addresses = await search(db, keyword=keyword)
    if not addresses:
        raise HTTPException(status_code=404, detail=f"No addresses found for keyword: {keyword}")
    return addresses


@router.get("/{address_id}")
async def get_address(address_id: int, db: Session = Depends(SessionLocal)):
    db_address = get_by_id(db, address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@router.put("/{address_id}")
async def update_address(address_id: int, data: AddressCreate, db: Session = Depends(SessionLocal)):
    db_address = update(db, address_id, data)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address
