from src.schemes import ApiRequest


class UpdateQueue(ApiRequest):
    event_id: str
    visitor_id: str
