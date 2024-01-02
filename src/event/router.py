import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.account.dependencies import verify_token
from src.account.models import Account
from src.database import get_db
from src.event.schemas import EventCreate
from src.event.service import create, get_by_id, get_all, update, start, stop, cancel

router = APIRouter()


@router.get("/{event_id}")
async def get_event(event_id: str, db: Session = Depends(get_db)):
    db_event = await get_by_id(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.get("/")
async def get_all_event(db: Session = Depends(get_db)):
    return await get_all(db)


@router.post("/create")
async def create_event(data: EventCreate, db: Session = Depends(get_db), user: Account = Depends(verify_token)):
    return await create(db, user, data)


@router.post("/update/{event_id}")
async def update_event(event_id: str, data: EventCreate, db: Session = Depends(get_db),
                       user: Account = Depends(verify_token)):
    logging.info(user.id)
    return await update(db, event_id, data)


@router.post("/start/{event_id}")
async def start_event(event_id: str, db: Session = Depends(get_db), user: Account = Depends(verify_token)):
    logging.info(user.id)
    return await start(db, event_id)


@router.post("/stop/{event_id}")
async def stop_event(event_id: str, db: Session = Depends(get_db), user: Account = Depends(verify_token)):
    logging.info(user.id)
    return await stop(db, event_id)


@router.post("/cancel/{event_id}")
async def cancel_event(event_id: str, db: Session = Depends(get_db), user: Account = Depends(verify_token)):
    logging.info(user.id)
    return await cancel(db, event_id)
