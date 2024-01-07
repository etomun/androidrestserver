import logging
from typing import List

from fastapi import APIRouter, Depends

from src.database import get_db
from src.dependencies import verify_admin
from src.event.schemas import EventResponse
from src.event.service import *
from src.schemes import ApiResponse
from src.utils import str_to_date_time_gmt

router = APIRouter()


@router.get("", response_model=ApiResponse[List[EventResponse]])
async def get_all_events(db: Session = Depends(get_db)):
    events = await get_all(db)
    if not events:
        return ApiResponse(data=[], error_message="No events")
    else:
        return ApiResponse(data=[EventResponse.from_db(event) for event in events])


@router.get("/{event_id}", response_model=ApiResponse[EventResponse])
async def get_event(event_id: str, db: Session = Depends(get_db)):
    event = await get_by_id(db, event_id)
    if not event:
        return ApiResponse(data=None, error_message="Event not found")
    else:
        return ApiResponse(data=EventResponse.from_db(event))


@router.post("/create", response_model=ApiResponse[EventResponse])
async def create_event(data: EventCreate, db: Session = Depends(get_db), admin: Account = Depends(verify_admin)):
    if await get_by_name(db, data.name):
        raise ValueError("Event Name is already registered")
    if str_to_date_time_gmt(data.expected_end_date) <= str_to_date_time_gmt(data.expected_start_date):
        raise ValueError("Expected start date cannot be on or after the end date.")
    event = await create(db, admin, data)
    if not event:
        return ApiResponse(data=None, error_message="Event not found")
    else:
        return ApiResponse(data=EventResponse.from_db(event))


@router.post("/delete/{event_id}", response_model=ApiResponse[bool])
async def delete_event(event_id: str, db: Session = Depends(get_db), admin: Account = Depends(verify_admin)):
    logging.info(admin.id)
    response = await delete_by_id(db, event_id)
    return ApiResponse(data=response)


@router.post("/update/{event_id}", response_model=ApiResponse[EventResponse])
async def update_event(event_id: str, data: EventCreate, db: Session = Depends(get_db),
                       admin: Account = Depends(verify_admin)):
    logging.info(admin.id)
    event = await update(db, event_id, data)
    if not event:
        return ApiResponse(data=None, error_message="Event not found")
    else:
        return ApiResponse(data=EventResponse.from_db(event))


@router.post("/start/{event_id}", response_model=ApiResponse[EventResponse])
async def start_event(event_id: str, db: Session = Depends(get_db), admin: Account = Depends(verify_admin)):
    logging.info(admin.id)
    event = await start(db, event_id)
    if not event:
        return ApiResponse(data=None, error_message="Event not found")
    else:
        return ApiResponse(data=EventResponse.from_db(event))


@router.post("/stop/{event_id}", response_model=ApiResponse[EventResponse])
async def stop_event(event_id: str, db: Session = Depends(get_db), admin: Account = Depends(verify_admin)):
    logging.info(admin.id)
    event = await stop(db, event_id)
    if not event:
        return ApiResponse(data=None, error_message="Event not found")
    else:
        return ApiResponse(data=EventResponse.from_db(event))


@router.post("/cancel/{event_id}", response_model=ApiResponse[EventResponse])
async def cancel_event(event_id: str, db: Session = Depends(get_db), admin: Account = Depends(verify_admin)):
    logging.info(admin.id)
    event = await cancel(db, event_id)
    if not event:
        return ApiResponse(data=None, error_message="Event not found")
    else:
        return ApiResponse(data=EventResponse.from_db(event))


@router.post('/clear')
async def clear_events(db: Session = Depends(get_db), user: Account = Depends(verify_admin)):
    logging.info(user.username)
    result = await clear(db)
    return ApiResponse(data=result)
