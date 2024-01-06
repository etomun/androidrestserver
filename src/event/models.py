import uuid
from enum import Enum as PythonEnum

from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, func, Boolean
from sqlalchemy.orm import relationship

from src.database import Base


class EventState(str, PythonEnum):
    not_started = 'NOT_STARTED'
    started = 'STARTED'
    finished = 'FINISHED'
    cancelled = 'CANCELLED'


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    name = Column(String, index=True, unique=True, nullable=False)
    location = Column(String, nullable=False)
    expected_start_date = Column(DateTime)
    expected_end_date = Column(DateTime)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    organizer = Column(String)
    description = Column(String)
    status = Column(Enum(EventState), default=EventState.not_started)
    has_queue = Column(Boolean)
    creator_id = Column(String, ForeignKey("accounts.id"), index=True, nullable=False)

    # Relationship with VisitorQueue
    queue = relationship("VisitorQueue", back_populates="event")

    # Relationship with Account
    creator = relationship("Account", back_populates="events")

    @property
    def is_event_running(self) -> bool:
        """
        Property to check if the event is currently running.
        Assumes that an event is running if the actual_start_date is set and the actual_end_date is not set.
        """
        return self.start_date is not None and self.end_date is None and self.status == EventState.started


def validate_status(self, status):
    current = self.status if self.status else None
    valid_val = isinstance(status, EventState)
    if current == EventState.not_started:
        valid_transition = status in (EventState.started, EventState.cancelled)
    elif current == EventState.started:
        valid_transition = status is EventState.finished
    else:
        valid_transition = False

    all_valid = valid_val and valid_transition
    if not all_valid:
        raise ValueError(f"Invalid status type. Expected {EventState}, got {type(status)}")
    return all_valid
