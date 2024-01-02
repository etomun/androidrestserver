from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.account.models import Account, Role
from src.event.models import Event, EventState
from src.event.schemas import EventCreate


async def create(db: Session, user: Account, data: EventCreate):
    if user.role is not Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create Event",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_event: Event = Event(name=data.name, organizer=data.organizer, location=data.location,
                            description=data.description)
    db_event.expected_start_date = data.expected_start_date
    db_event.expected_end_date = data.expected_end_date
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


async def get_by_id(db: Session, event_id: str) -> Event:
    return db.query(Event).filter(Event.id == event_id).first()


async def get_all(db: Session):
    return db.query(Event).all()


async def start(db: Session, event_id: str):
    db_event: Event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        db_event.status = EventState.started
        db_event.start_date = datetime.utcnow()
        db_event.end_date = None
        db.commit()
        db.refresh(db_event)
    return db_event


async def stop(db: Session, event_id: str):
    db_event: Event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        db_event.status = EventState.finished
        db_event.end_date = datetime.utcnow()
        db.commit()
        db.refresh(db_event)
    return db_event


async def cancel(db: Session, event_id: str):
    db_event: Event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        db_event.status = EventState.cancelled
        db_event.start_date = None
        db_event.end_date = None
        db.commit()
        db.refresh(db_event)
    return db_event


async def update(db: Session, event_id: str, data: EventCreate):
    db_event: Event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        for attr, value in data.model_dump().items():
            if value is not None:
                setattr(db_event, attr, value)
    return db_event
