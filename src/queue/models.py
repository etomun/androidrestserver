from enum import Enum as PythonEnum

from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship, validates

from src.database import Base


class QueueState(str, PythonEnum):
    queued = "Queued"
    enter_gate = "Enter"
    exit_gate = "Exit"


class VisitorQueue(Base):
    __tablename__ = "queue"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    visitor_id = Column(Integer, ForeignKey("visitors.id"))
    state = Column(Enum(QueueState), default=QueueState.queued.value)
    timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship with Event and Visitor
    event = relationship("Event", back_populates="queue")
    visitor = relationship("Visitor", back_populates="queue")

    # Validate that the state is a valid QueueState value
    @validates('state')
    def validate_state(self, value):
        if value not in QueueState.__members__.values():
            raise ValueError(f"Invalid state: {value}. Allowed values: {', '.join(QueueState.__members__.values())}")
        return value
