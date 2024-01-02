import uuid
from enum import Enum as PythonEnum

from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship, validates

from src.database import Base
from src.utils import str_to_date_time_gmt


class EventState(str, PythonEnum):
    not_started = 'NOT_STARTED'
    started = 'STARTED'
    finished = 'FINISHED'
    cancelled = 'CANCELLED'


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    location = Column(String, nullable=False)
    expected_start_date = Column(DateTime)
    expected_end_date = Column(DateTime)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    organizer = Column(String)
    description = Column(String)
    status = Column(Enum(EventState), default=EventState.not_started)
    creator_id = Column(String, ForeignKey("accounts.id"), index=True, nullable=False)

    # Relationship with VisitorQueue
    queue = relationship("VisitorQueue", back_populates="event")

    # Relationship with Account
    creator = relationship("Account", back_populates="events")

    @property
    def is_running(self):
        """
        Property to check if the event is currently running.
        Assumes that an event is running if the actual_start_date is set and the actual_end_date is not set.
        """
        return self.actual_start_date is not None and self.actual_end_date is None and self.status == EventState.started

    # Validate that the status is a valid EventState value
    @validates('status')
    def validate_status(self, value):
        current = self.status if self.status else None

        valid_val = isinstance(value, EventState)
        if current == EventState.not_started:
            valid_transition = value in (EventState.started, EventState.cancelled)
        elif current == EventState.started:
            valid_transition = value is EventState.finished
        else:
            valid_transition = False

        all_valid = valid_val and valid_transition
        if not all_valid:
            raise ValueError(f"Invalid status type. Expected {EventState}, got {type(value)}")
        return all_valid

    @validates('expected_start_date')
    def validate_expected_start_date(self, key, value):
        if value >= self.expected_end_date:
            raise ValueError("Date cannot be on or after the end date.")

        if value is None or isinstance(value, DateTime):
            return value

        return str_to_date_time_gmt(value)

    @validates('expected_end_date')
    def validate_expected_end_date(self, key, value):
        if value <= self.expected_start_date:
            raise ValueError("Date cannot be on or before the start date.")

        if value is None or isinstance(value, DateTime):
            return value

        return str_to_date_time_gmt(value)

    @validates('start_date')
    def validate_start_date(self, key, value):
        if value >= self.end_date:
            raise ValueError("Date cannot be on or after the end date.")

        if value is None or isinstance(value, DateTime):
            return value

        return str_to_date_time_gmt(value)

    @validates('end_date')
    def validate_end_date(self, key, value):
        if value <= self.start_date:
            raise ValueError("Date cannot be on or before the start date.")

        if value is None or isinstance(value, DateTime):
            return value

        return str_to_date_time_gmt(value)
