from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from starlette import status

from src.address.models import Address
from src.queue.models import VisitorQueue, QueueState
from src.queue.schemas import UpdateQueue
from src.visitor.models import Visitor


async def add_new(db: Session, data: UpdateQueue):
    existing_queue = db.query(VisitorQueue).filter(VisitorQueue.event_id == data.event_id,
                                                   VisitorQueue.visitor_id == data.visitor_id).first()
    if existing_queue:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Visitor already in queue")

    queue = VisitorQueue(event_id=data.event_id, visitor_id=data.visitor_id, state=QueueState.register)
    db.add(queue)
    db.commit()
    db.refresh(queue)
    return queue


async def update_state(db: Session, data: UpdateQueue, new_state: QueueState):
    existing_queue = db.query(VisitorQueue).filter(VisitorQueue.event_id == data.event_id,
                                                   VisitorQueue.visitor_id == data.visitor_id).first()
    if not existing_queue:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No queue to be updated")

    existing_queue.update_state(new_state.value)
    db.commit()
    db.refresh(existing_queue)
    return existing_queue


async def get_by_status(db: Session, event_id: str, state: QueueState, limit: int):
    return (
        db.query(VisitorQueue, Visitor, Address)
        .join(Visitor, VisitorQueue.visitor_id == Visitor.id)
        .join(Address, Visitor.address_id == Address.id)
        .options(joinedload(VisitorQueue.visitor).joinedload(Visitor.address))
        .filter(VisitorQueue.state == state)
        .filter(VisitorQueue.event_id == event_id)
        .order_by(VisitorQueue.timestamp)
        .limit(limit)
        .all()
    )
