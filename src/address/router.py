from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.address.schemas import AddressCreate, AddressResponse
from src.address.service import add, search, get_by_id, update
from src.database import get_db
from src.schemes import ApiResponse

router = APIRouter()


@router.post("/add-bulk", response_model=ApiResponse[bool])
async def add_address_bulk(data: list[AddressCreate], db: Session = Depends(get_db)):
    success = await add(db, data)
    return ApiResponse(data=success)


@router.post("/add", response_model=ApiResponse[AddressResponse])
async def add_address(data: AddressCreate, db: Session = Depends(get_db)):
    success = await add(db, [data])
    return ApiResponse(data=success)


@router.get("/search", response_model=ApiResponse[List[AddressResponse]])
async def search_address(keyword: str = Query(..., min_length=3), db: Session = Depends(get_db)):
    addresses = await search(db, keyword=keyword)
    return ApiResponse(data=addresses)


@router.get("/{address_id}", response_model=ApiResponse[AddressResponse])
async def get_address(address_id: str, db: Session = Depends(get_db)):
    address = get_by_id(db, address_id)
    return ApiResponse(data=address)


@router.post("/update/{address_id}", response_model=ApiResponse[AddressResponse])
async def update_address(address_id: str, data: AddressCreate, db: Session = Depends(get_db)):
    address = update(db, address_id, data)
    return ApiResponse(data=address)
