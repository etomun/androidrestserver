from pydantic import BaseModel


class EventCreate(BaseModel):
    name: str
    location: str
    expected_start_date: str
    expected_end_date: str
    organizer: str
    description: str


class EventResponse(EventCreate):
    id: str
    status: str
