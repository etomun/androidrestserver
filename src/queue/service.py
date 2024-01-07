from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload
from starlette import status

from src.account import Account
from src.member.models import Member
from src.queue.models import VisitorQueue, QueueState
from src.queue.schemas import UpdateQueue


async def add_new(db: Session, pic: Account, data: UpdateQueue):
    queue = db.query(VisitorQueue).filter_by(event_id=data.event_id, member_code=data.member_code).first()
    if queue:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Visitor already in queue")
    queue = VisitorQueue(event_id=data.event_id, member_code=data.member_code, queue_pic_id=pic.id,
                         state=QueueState.register)
    db.add(queue)
    db.commit()
    db.refresh(queue)
    return queue


async def delete(db: Session, queue_id: str) -> bool:
    queue = db.query(VisitorQueue).filter_by(id=queue_id).first()
    if queue is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Visitor Not Found")
    if queue.state != QueueState.register:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Visitor has entered")

    try:
        db.delete(queue)
        db.commit()
        return True
    except:
        return False


async def update_state(db: Session, data: UpdateQueue, new_state: QueueState):
    existing_queue = db.query(VisitorQueue).filter_by(event_id=data.event_id, member_code=data.member_code).first()
    if not existing_queue:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Visitor Not Found")

    if existing_queue.state == new_state:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Visitor already in {new_state.value}")
    existing_queue.update_state(new_state)
    db.commit()
    db.refresh(existing_queue)
    return existing_queue


async def get_by_state(db: Session, event_id: str, state: QueueState, limit: int):
    return (
        db.query(VisitorQueue)
        .filter_by(state=state, event_id=event_id)
        .options(joinedload(VisitorQueue.member).joinedload(Member.address))
        .join(Member, VisitorQueue.member)
        .order_by(desc(Member.is_relatives))  # Relatives first
        .order_by(Member.gender)  # Females before Males
        .order_by(VisitorQueue.last_update)  # First in First out
        .limit(limit)
        .all()
    )


async def clear(db: Session):
    try:
        db.execute(VisitorQueue.__table__.delete())
        db.commit()
        return {"message": "Table cleared successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error clearing table: {str(e)}")
