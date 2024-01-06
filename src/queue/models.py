import uuid
from enum import Enum as PythonEnum

from sqlalchemy import Column, String, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship, validates

from src.database import Base


class QueueState(str, PythonEnum):
    register = "Queued"
    enter_gate = "Entered"
    exit_gate = "Exited"


class VisitorQueue(Base):
    __tablename__ = "queue"

    id = Column(String, primary_key=True, unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    member_code = Column(String, ForeignKey("members.unique_code"), nullable=False)
    state = Column(Enum(QueueState), default=QueueState.register)
    date_queued = Column(DateTime, server_default=func.now())
    date_entered = Column(DateTime)
    date_exited = Column(DateTime)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship with Event and Member
    event = relationship("Event", back_populates="queue")
    member = relationship("Member", back_populates="queue")

    # Validate that the state is a valid QueueState value
    @validates('state')
    def validate_state(self, key, value):
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
        return value

    def update_state(self, value: QueueState):
        stamp = func.now()
        self.state = value
        self.last_update = stamp
        if value is QueueState.exit_gate:
            self.date_exited = stamp
        if value is QueueState.enter_gate:
            self.date_entered = stamp
        if value is QueueState.register:
            self.date_queued = stamp
