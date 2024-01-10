from pydantic import BaseModel

from src.account import AccountResponse
from src.address.schemas import AddressResponse
from src.member.schemas import MemberResponse
from src.queue.models import VisitorQueue
from src.utils import date_time_to_str_gmt


class UpdateQueue(BaseModel):
    event_id: str
    member_code: str


class QueueResponse(BaseModel):
    id: str
    event_id: str
    queue_pic_id: str
    last_status: str
    date_queued: str
    date_entered: str
    date_exited: str
    last_update: str
    member: MemberResponse

    @classmethod
    def from_db(cls, queue: VisitorQueue):
        member = queue.member
        address = AddressResponse.from_db(member.address)
        pic = AccountResponse.from_db(member.pic)
        return cls(
            id=queue.id,
            event_id=queue.event_id,
            queue_pic_id=queue.queue_pic_id,
            last_status=queue.state.value,
            date_queued=date_time_to_str_gmt(queue.date_queued),
            date_entered=date_time_to_str_gmt(queue.date_entered),
            date_exited=date_time_to_str_gmt(queue.date_exited),
            last_update=date_time_to_str_gmt(queue.last_update),
            member=MemberResponse(
                id=member.id,
                address_id=member.address_id,
                pic_id=member.pic_id,
                unique_code=member.unique_code,
                name=member.name,
                gender=member.gender,
                age=member.age,
                is_relatives=member.is_relatives,
                address=address,
                pic=pic,
            ),
        )


class SocketMessage(BaseModel):
    event_id: str
    message_code: str
    message: str
