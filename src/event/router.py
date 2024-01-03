import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.account.dependencies import verify_token
from src.account.models import Account
from src.database import get_db
from src.event.schemas import EventCreate, EventResponse
from src.event.service import create, get_by_id, get_all, update, start, stop, cancel, delete_by_id, get_by_name
from src.schemes import ApiResponse
from src.utils import str_to_date_time_gmt

router = APIRouter()


@router.get("/{event_id}", response_model=ApiResponse[EventResponse])
async def get_event(event_id: str, db: Session = Depends(get_db)):
    event = await get_by_id(db, event_id)
    return ApiResponse(data=EventResponse.from_db(event))


@router.get("/", response_model=ApiResponse[List[EventResponse]])
async def get_all_event(db: Session = Depends(get_db)):
    events = await get_all(db)
    responses = [
        EventResponse.from_db(event)
        for event in events
    ]
    return ApiResponse(data=responses)


@router.post("/create", response_model=ApiResponse[EventResponse])
async def create_event(data: EventCreate, db: Session = Depends(get_db), user: Account = Depends(verify_token)):
    if await get_by_name(db, data.name):
        raise ValueError("Event Name is already registered")
    if str_to_date_time_gmt(data.expected_end_date) <= str_to_date_time_gmt(data.expected_start_date):
        raise ValueError("Expected start date cannot be on or after the end date.")
    event = await create(db, user, data)
    return ApiResponse(data=EventResponse.from_db(event))


@router.post("/delete/{event_id}", response_model=ApiResponse[bool])
async def delete_event(event_id: str, db: Session = Depends(get_db), user: Account = Depends(verify_token)):
    logging.info(user.name)
    response = await delete_by_id(db, event_id)
    return ApiResponse(data=response)


@router.post("/update/{event_id}", response_model=ApiResponse[EventResponse])
async def update_event(event_id: str, data: EventCreate, db: Session = Depends(get_db),
                       user: Account = Depends(verify_token)):
    logging.info(user.id)
    event = await update(db, event_id, data)
    return ApiResponse(data=EventResponse.from_db(event))


@router.post("/start/{event_id}", response_model=ApiResponse[EventResponse])
async def start_event(event_id: str, db: Session = Depends(get_db), user: Account = Depends(verify_token)):
    logging.info(user.id)
    return await start(db, event_id)


@router.post("/stop/{event_id}", response_model=ApiResponse[EventResponse])
async def stop_event(event_id: str, db: Session = Depends(get_db), user: Account = Depends(verify_token)):
    logging.info(user.id)
    event = await stop(db, event_id)
    return ApiResponse(data=EventResponse.from_db(event))


@router.post("/cancel/{event_id}", response_model=ApiResponse[EventResponse])
async def cancel_event(event_id: str, db: Session = Depends(get_db), user: Account = Depends(verify_token)):
    logging.info(user.id)
    event = await cancel(db, event_id)
    return ApiResponse(data=EventResponse.from_db(event))
