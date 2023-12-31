from enum import Enum as PythonEnum

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, validates

from src.database import Base


class EventState(str, PythonEnum):
    not_started = 'NOT_STARTED'
    running = 'RUNNING'
    finished = 'FINISHED'
    cancelled = 'CANCELLED'
    unknown = 'UNKNOWN'


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    organizer = Column(String)
    location = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    actual_start_date = Column(DateTime)
    actual_end_date = Column(DateTime)
    description = Column(String)
    status = Column(String, default=EventState.not_started)

    # Relationship with VisitorQueue
    queue = relationship("VisitorQueue", back_populates="event")

    @property
    def is_running(self):
        """
        Property to check if the event is currently running.
        Assumes that an event is running if the start date is set and the end date is not set.
        """
        return self.actual_start_date is not None and self.actual_end_date is None and self.status is EventState.running

    # Validate that the status is a valid EventState value
    @validates('status')
    def validate_status(self, value):
        if value not in EventState.__members__.values():
            raise ValueError(f"Invalid status: {value}. Allowed values: {', '.join(EventState.__members__.values())}")
        return value
