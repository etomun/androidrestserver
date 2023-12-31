from datetime import datetime

from sqlalchemy.orm import Session

from src.event.models import Event, EventState


def create_event(db: Session, name: str, organizer: str, location: str, start_date: datetime, end_date: datetime, description: str):
    db_event = Event(name=name, organizer=organizer, location=location, start_date=start_date, end_date=end_date,
                     description=description)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_event(db: Session, event_id: int) -> Event:
    return db.query(Event).filter(Event.id == event_id).first()


def get_events(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Event).offset(skip).limit(limit).all()


def update_event(db: Session, event_id: int, name: str, organizer: str, location: str, start_date, end_date,
                 description: str):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        db_event.name = name
        db_event.organizer = organizer
        db_event.location = location
        db_event.actual_start_date = start_date
        db_event.actual_end_date = end_date
        db_event.description = description
        db.commit()
        db.refresh(db_event)
    return db_event


def start_event(db: Session, event_id: int):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        db_event.status = EventState.running
        db.commit()
        db.refresh(db_event)
    return db_event


def stop_event(db: Session, event_id: int):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        db_event.status = EventState.finished
        db_event.actual_end_date = datetime.utcnow()
        db.commit()
        db.refresh(db_event)
    return db_event


def cancel_event(db: Session, event_id: int):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        db_event.status = EventState.cancelled
        db_event.actual_end_date = datetime.utcnow()
        db.commit()
        db.refresh(db_event)
    return db_event
