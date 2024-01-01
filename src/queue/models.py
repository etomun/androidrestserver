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
    state = Column(Enum(QueueState), default=QueueState.register.value)
    timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship with Event and Visitor
    event = relationship("Event", back_populates="queue")
    visitor = relationship("Visitor", back_populates="queue")

    # Validate that the state is a valid QueueState value
    @validates('state')
    def validate_state(self, value):
        current = self.state.value if self.state else None
        valid_val = value in QueueState.__members__.values()
        if current == QueueState.register.value:
            valid_transition = value == QueueState.enter_gate.value
        elif current == QueueState.enter_gate.value:
            valid_transition = value == QueueState.exit_gate.value
        else:
            valid_transition = value == QueueState.register.value

        return valid_val and valid_transition

    def update_state(self, value):
        self.state = value
        self.timestamp = func.now()
