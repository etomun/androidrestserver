from pydantic import BaseModel, root_validator

from src.event.models import Event
from src.utils import str_to_date_time_gmt, date_time_to_str_gmt


class EventCreate(BaseModel):
    name: str
    location: str
    expected_start_date: str
    expected_end_date: str
    organizer: str
    description: str
    has_queue: bool

    # NOT CALLED https://github.com/pydantic/pydantic/issues/3821, call manually in router
    @root_validator(pre=False, skip_on_failure=True)
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
    start_date: str
    end_date: str
    creator: EventCreator

    @classmethod
    def from_db(cls, event: Event):
        return cls(id=event.id,
                   status=event.status.value,
                   last_updated=date_time_to_str_gmt(event.last_updated),
                   start_date=date_time_to_str_gmt(event.start_date),
                   end_date=date_time_to_str_gmt(event.end_date),
                   name=event.name,
                   location=event.location,
                   expected_start_date=date_time_to_str_gmt(event.expected_start_date),
                   expected_end_date=date_time_to_str_gmt(event.expected_end_date),
                   organizer=event.organizer,
                   description=event.description,
                   has_queue=event.has_queue,
                   creator=EventCreator(
                       id=event.creator.id,
                       username=event.creator.username,
                       phone=event.creator.phone,
                       name=event.creator.name,
                   ))
