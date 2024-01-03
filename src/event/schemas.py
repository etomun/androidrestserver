from pydantic import BaseModel
from pydantic.v1 import root_validator

from src.event.models import Event
from src.utils import str_to_date_time_gmt


class EventCreate(BaseModel):
    name: str
    location: str
    expected_start_date: str
    expected_end_date: str
    organizer: str
    description: str

    # NOT CALLED https://github.com/pydantic/pydantic/issues/3821, call manually in router
    @root_validator
    def validate_date_range(cls, values):
        start_date = values.get("expected_start_date")
        end_date = values.get("expected_end_date")

        if start_date and end_date:
            start_date_obj = str_to_date_time_gmt(start_date)
            end_date_obj = str_to_date_time_gmt(end_date)

            if start_date_obj >= end_date_obj:
                raise ValueError("Expected start date cannot be on or after the end date.")

        return values


class EventCreator(BaseModel):
    id: str
    username: str
    phone: str
    name: str


class EventResponse(EventCreate):
    id: str
    status: str
    last_updated: str
    creator: EventCreator

    @classmethod
    def from_db(cls, event: Event):
        return cls(id=event.id,
                   status=event.status.value,
                   last_updated=event.last_updated,
                   name=event.name,
                   location=event.location,
                   expected_start_date=str(event.expected_start_date),
                   expected_end_date=str(event.expected_end_date),
                   organizer=event.organizer,
                   description=event.description,
                   creator=EventCreator(
                       id=event.creator.id,
                       username=event.creator.username,
                       phone=event.creator.phone,
                       name=event.creator.name,
                   ))
