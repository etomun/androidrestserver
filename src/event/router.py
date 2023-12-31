from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.event.service import create_event, get_event, get_events, update_event, start_event, stop_event

router = APIRouter()


@router.post("/create")
async def create_event_route(name: str, organizer: str, location: str, start_date: datetime, end_date: datetime,
                             description: str,
                             db: Session = Depends(SessionLocal)):
    return create_event(db, name=name, organizer=organizer, location=location, start_date=start_date, end_date=end_date,
                        description=description)


@router.get("/{event_id}")
async def read_event(event_id: int, db: Session = Depends(SessionLocal)):
    db_event = get_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.get("/")
async def get_all_events(skip: int = 0, limit: int = 10, db: Session = Depends(SessionLocal)):
    return get_events(db, skip=skip, limit=limit)


@router.put("/{event_id}")
async def update_event_route(event_id: int, name: str, organizer: str, location: str, start_date, end_date,
                             description: str,
                             db: Session = Depends(SessionLocal)):
    db_event = update_event(db, event_id, name=name, organizer=organizer, location=location, start_date=start_date,
                            end_date=end_date, description=description)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.put("/start/{event_id}")
async def start_event_route(event_id: int, db: Session = Depends(SessionLocal)):
    db_event = start_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.put("/stop/{event_id}")
async def stop_event_route(event_id: int, db: Session = Depends(SessionLocal)):
    db_event = stop_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.put("/status/{event_id}", response_model=dict)
async def get_event_status(event_id: int, db: Session = Depends(SessionLocal)):
    db_event = get_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"status": db_event.status}
