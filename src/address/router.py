import logging

from fastapi import APIRouter, Depends

from src.account.models import Account
from src.address.schemas import AddressResponse
from src.address.service import *
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


@router.get("", response_model=ApiResponse[List[AddressResponse]])
async def get_all_address(db: Session = Depends(get_db)):
    addresses = await get_all(db)
    if not addresses:
        return ApiResponse(data=[], error_message="Address not found")
    else:
        return ApiResponse(data=[AddressResponse.from_db(address) for address in addresses])


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
    if not address:
        return ApiResponse(data=None, error_message="Address not found")
    else:
        return ApiResponse(data=AddressResponse.from_db(address))


@router.post("/update/{address_id}", response_model=ApiResponse[AddressResponse])
async def update_address(address_id: str, data: AddressCreate, db: Session = Depends(get_db)):
    address = await update(db, address_id, data)
    if not address:
        return ApiResponse(data=None, error_message="Address not found")
    else:
        return ApiResponse(data=AddressResponse.from_db(address))


@router.post('/clear')
async def clear_addresses(db: Session = Depends(get_db), user: Account = Depends(verify_admin)):
    logging.info(user.username)
    result = await clear(db)
    return ApiResponse(data=result)
