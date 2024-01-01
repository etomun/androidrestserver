from pydantic import BaseModel


class UpdateQueue(BaseModel):
    event_id: str
    visitor_id: str
