from pydantic import BaseModel

from src.address.models import Address
from src.queue.models import VisitorQueue
from src.visitor.models import Visitor


class UpdateQueue(BaseModel):
    event_id: str
    visitor_id: str


class QueueVisitorAddress(BaseModel):
    village: str
    district: str
    line: str


class QueueVisitor(BaseModel):
    id: str
    unique_code: str
    name: str
    gender: str
    age: int
    is_relatives: bool
    address: QueueVisitorAddress


class VisitorQueueResponse(BaseModel):
    id: str
    last_status: str
    last_updated: str
    visitor: QueueVisitor

    @classmethod
    def from_db(cls, visitor_queue: VisitorQueue, visitor: Visitor, address: Address):
        return cls(
            id=str(visitor_queue.id),
            event_id=str(visitor_queue.event_id),
            visitor_id=str(visitor_queue.visitor_id),
            status=str(visitor_queue.state.value),
            visitor=QueueVisitor(
                unique_code=visitor.unique_code,
                name=visitor.name,
                gender=visitor.gender,
                age=visitor.age,
                is_relatives=visitor.is_relatives,
                id=visitor.id,
                address=QueueVisitorAddress(
                    village=address.village,
                    district=address.district,
                    line=address.line,
                ),
            ),
        )
