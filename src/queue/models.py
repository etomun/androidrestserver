import uuid
from enum import Enum as PythonEnum

from sqlalchemy import Column, String, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship, validates

from src.database import Base


class QueueState(str, PythonEnum):
    register = "Queued"
    enter_gate = "Enter"
    exit_gate = "Exit"


class VisitorQueue(Base):
    __tablename__ = "queue"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    visitor_id = Column(String, ForeignKey("visitors.id"), nullable=False)
    state = Column(Enum(QueueState), default=QueueState.register)
    timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship with Event and Visitor
    event = relationship("Event", back_populates="queue")
    visitor = relationship("Visitor", back_populates="queue")

    # Validate that the state is a valid QueueState value
    @validates('state')
    def validate_state(self, value):
        current = self.state if self.state else None
        valid_val = isinstance(value, QueueState)
        if current == QueueState.register:
            valid_transition = value is QueueState.enter_gate
        elif current == QueueState.enter_gate:
            valid_transition = value is QueueState.exit_gate
        else:
            valid_transition = value is QueueState.register

        all_valid = valid_val and valid_transition
        if not all_valid:
            raise ValueError(f"Invalid status type. Expected {QueueState}, got {type(value)}")
        return all_valid

    def update_state(self, value):
        self.state = value
        self.timestamp = func.now()
