from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.event import get_by_id, Event


async def verify_queue_event_started(event_id: str, db: Session):
    event: Event = await get_by_id(db, event_id)
    if event is None:
        HTTPException(status.HTTP_404_NOT_FOUND, "Event not found")
    if not event.has_queue:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Event has no queue")
    if not event.is_event_running:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Event is not started yet")
    return event
