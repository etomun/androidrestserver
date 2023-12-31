from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.queue.service import update_queue

router = APIRouter()


@router.post("/queue/")
def add_queue(event_id: int, visitor_id: int, state: str, db: Session = Depends(SessionLocal)):
    return add_queue(db, event_id=event_id, visitor_id=visitor_id, state=state)


@router.put("/queue/update_state")
def update_state(event_id: int, visitor_id: int, new_state: str, db: Session = Depends(SessionLocal)):
    db_event_visitor = update_queue(db, event_id=event_id, visitor_id=visitor_id, new_state=new_state)
    if db_event_visitor is None:
        raise HTTPException(status_code=404, detail="Queue not found")
    return db_event_visitor
