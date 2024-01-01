from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette import status

from src.queue.models import VisitorQueue, QueueState
from src.queue.schemas import UpdateQueue


async def add_new(db: Session, data: UpdateQueue):
    current_state = db.query(VisitorQueue).filter(
        VisitorQueue.event_id == data.event_id,
        VisitorQueue.visitor_id == data.visitor_id
    ).first()
    if current_state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Visitor already in queue",
            headers={"WWW-Authenticate": "Bearer"}
        )

    db_queue = VisitorQueue(event_id=data.event_id, visitor_id=data.visitor_id, state=QueueState.register)
    db.add(db_queue)
    db.commit()
    db.refresh(db_queue)
    return db_queue


async def update_state(db: Session, data: UpdateQueue, new_state: QueueState):
    existing_queue = db.query(VisitorQueue).filter(
        VisitorQueue.event_id == data.event_id, VisitorQueue.visitor_id == data.visitor_id).first()
    if existing_queue:
        existing_queue.update_state(new_state.value)
        db.commit()
        db.refresh(existing_queue)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No queue to be updated",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_by_status(db: Session, state: QueueState):
    return db.query(VisitorQueue).filter(VisitorQueue.state == state).order_by(desc(VisitorQueue.timestamp)).all()
