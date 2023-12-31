from sqlalchemy.orm import Session

from src.queue.models import VisitorQueue, QueueState


def add_queue(db: Session, event_id: int, visitor_id: int):
    # Avoid double visitors
    existing_visitor = db.query(VisitorQueue).filter(
        VisitorQueue.event_id == event_id,
        VisitorQueue.visitor_id == visitor_id
    ).first()
    if existing_visitor:
        return None  # Double visitor, return None or raise an exception

    db_queue = VisitorQueue(event_id=event_id, visitor_id=visitor_id, state=QueueState.queued)
    db.add(db_queue)
    db.commit()
    db.refresh(db_queue)
    return db_queue


def update_queue(db: Session, event_id: int, visitor_id: int, new_state: str):
    # Avoid double/repeat state
    existing_visitor = db.query(VisitorQueue).filter(
        VisitorQueue.event_id == event_id,
        VisitorQueue.visitor_id == visitor_id
    ).first()
    if existing_visitor and existing_visitor.state == new_state:
        return None  # Double/repeat state, return None or raise an exception

    db_queue = db.query(VisitorQueue).filter(
        VisitorQueue.event_id == event_id,
        VisitorQueue.visitor_id == visitor_id
    ).first()

    if db_queue:
        # If the given state is "Enter Gate," current state must be "Queued"
        if new_state == QueueState.enter_gate and db_queue.state != QueueState.queued:
            return None  # Invalid state transition, return None or raise an exception

        # If the given state is "Exit Gate," current state must be "Enter Gate"
        if new_state == QueueState.exit_gate and db_queue.state != QueueState.enter_gate:
            return None  # Invalid state transition, return None or raise an exception

        # Check if the new state is a valid state
        if new_state in QueueState.__members__:
            db_queue.state = new_state
            db.commit()
            db.refresh(db_queue)

    return db_queue
