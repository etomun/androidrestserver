from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from starlette import status

from src.account.models import Account
from src.event.models import Event, EventState
from src.event.schemas import EventCreate
from src.utils import str_to_date_time_gmt


async def create(db: Session, user: Account, data: EventCreate):
    db_event: Event = Event(name=data.name, organizer=data.organizer, location=data.location,
                            description=data.description, has_queue=data.has_queue, creator_id=user.id)
    db_event.expected_start_date = str_to_date_time_gmt(data.expected_start_date)
    db_event.expected_end_date = str_to_date_time_gmt(data.expected_end_date)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db.query(Event).filter_by(id=db_event.id).options(joinedload(Event.creator)).first()


async def delete_by_id(db: Session, event_id: str) -> bool:
    event = db.query(Event).filter_by(id=event_id).first()
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event data not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        db.delete(event)
        db.commit()
        return True
    except:
        return False


async def get_by_id(db: Session, event_id: str):
    return db.query(Event).filter_by(id=event_id).options(joinedload(Event.creator)).first()


async def get_by_name(db: Session, event_name: str):
    return db.query(Event).filter_by(name=event_name).options(joinedload(Event.creator)).first()


async def get_all(db: Session):
    return db.query(Event).options(
        joinedload(Event.creator)
    ).all()


async def start(db: Session, event_id: str):
    db_event = db.query(Event).filter_by(id=event_id).first()
    if db_event.status is EventState.started:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Event has been started before")
    if db_event.status is EventState.finished:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Event has been finished")
    if db_event.status is EventState.cancelled:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Event has been cancelled")
    if db_event:
        db_event.status = EventState.started
        db_event.start_date = datetime.utcnow()
        db_event.end_date = None
        db.commit()
        db.refresh(db_event)
    return db_event


async def stop(db: Session, event_id: str):
    db_event = db.query(Event).filter_by(id=event_id).first()
    if db_event.status is EventState.not_started:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Event is not started yet")
    if db_event.status is EventState.finished:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Event has been finished before")
    if db_event.status is EventState.cancelled:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Event has been cancelled")
    if db_event:
        db_event.status = EventState.finished
        db_event.end_date = datetime.utcnow()
        db.commit()
        db.refresh(db_event)
    return db_event


async def cancel(db: Session, event_id: str):
    db_event = db.query(Event).filter_by(id=event_id).first()
    if db_event.status is EventState.started:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Event has been started")
    if db_event.status is EventState.finished:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Event has been finished")
    if db_event.status is EventState.cancelled:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Event has been cancelled before")
    if db_event:
        db_event.status = EventState.cancelled
        db_event.start_date = None
        db_event.end_date = None
        db.commit()
        db.refresh(db_event)
    return db_event


async def update(db: Session, event_id: str, data: EventCreate):
    try:
        db_event = db.query(Event).filter_by(id=event_id).first()
        if db_event:
            for attr, value in data.model_dump().items():
                if value is not None:
                    if attr in ['expected_start_date', 'expected_end_date']:
                        value = str_to_date_time_gmt(value)
                    setattr(db_event, attr, value)
            db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Error updating event in the database: {e}")
    return db_event


async def clear(db: Session):
    try:
        db.execute(Event.__table__.delete())
        db.commit()
        return {"message": "Table cleared successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error clearing table: {str(e)}")
