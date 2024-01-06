import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.account.models import Account
from src.address.schemas import AddressCreate, AddressResponse
from src.address.service import add, search, get_by_id, update, clear
from src.database import get_db
from src.dependencies import verify_admin
from src.schemes import ApiResponse

router = APIRouter()


@router.post("/add-bulk", response_model=ApiResponse[List[AddressResponse]])
async def add_address_bulk(data: List[AddressCreate], db: Session = Depends(get_db)):
    inserted = await add(db, data)
    response = [AddressResponse.from_db(address) for address in inserted]
    return ApiResponse(data=response)


@router.post("/add", response_model=ApiResponse[List[AddressResponse]])
async def add_address(data: AddressCreate, db: Session = Depends(get_db)):
    inserted = await add(db, [data])
    response = [AddressResponse.from_db(address) for address in inserted]
    return ApiResponse(data=response)


@router.get("/search", response_model=ApiResponse[List[AddressResponse]])
async def search_address(keyword: str, db: Session = Depends(get_db)):
    addresses = await search(db, keyword=keyword)
    if not addresses:
        return ApiResponse(data=[], error_message="Address not found")
    else:
        return ApiResponse(data=[AddressResponse.from_db(address) for address in addresses])


@router.get("/{address_id}", response_model=ApiResponse[AddressResponse])
async def get_address(address_id: str, db: Session = Depends(get_db)):
    address = await get_by_id(db, address_id)
    return ApiResponse(data=AddressResponse.from_db(address))


@router.post("/update/{address_id}", response_model=ApiResponse[AddressResponse])
async def update_address(address_id: str, data: AddressCreate, db: Session = Depends(get_db)):
    address = await update(db, address_id, data)
    return ApiResponse(data=AddressResponse.from_db(address))


@router.post('/clear')
async def clear_addresses(db: Session = Depends(get_db), user: Account = Depends(verify_admin)):
    logging.info(user.username)
    result = await clear(db)
    return ApiResponse(data=result)
