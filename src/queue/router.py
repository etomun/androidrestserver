import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.account.dependencies import verify_token
from src.account.models import Account
from src.database import get_db
from src.queue.models import QueueState
from src.queue.schemas import UpdateQueue, VisitorQueueResponse
from src.queue.service import update_state, add_new, get_by_status
from src.schemes import ApiResponse

router = APIRouter()


@router.post("/add", response_model=ApiResponse[VisitorQueueResponse])
async def add_queue(data: UpdateQueue, db: Session = Depends(get_db), user: Account = Depends(verify_token)):
    logging.info(user.id)
    queue = await add_new(db, data)
    return ApiResponse(data=VisitorQueueResponse.from_db(queue))


@router.post("/enter-gate", response_model=ApiResponse[VisitorQueueResponse])
async def enter_gate(data: UpdateQueue, db: Session = Depends(get_db), user: Account = Depends(verify_token)):
    logging.info(user.id)
    return await update_state(db, data, QueueState.enter_gate)


@router.post("/exit-gate", response_model=ApiResponse[VisitorQueueResponse])
async def exit_gate(data: UpdateQueue, db: Session = Depends(get_db), user: Account = Depends(verify_token)):
    logging.info(user.id)
    return await update_state(db, data, QueueState.exit_gate)


@router.get("/waiting", response_model=ApiResponse[List[VisitorQueueResponse]])
async def get_waiting(event_id: str, limit: int, db: Session = Depends(get_db)):
    queue = await get_by_status(db, event_id, QueueState.register, limit)
    responses = [
        VisitorQueueResponse.from_db(q, v, a)
        for q, v, a in queue
    ]
    return ApiResponse(data=responses)


@router.get("/entered", response_model=ApiResponse[List[VisitorQueueResponse]])
async def get_entered(event_id: str, limit: int, db: Session = Depends(get_db)):
    queue = await get_by_status(db, event_id, QueueState.enter_gate, limit)
    responses = [
        VisitorQueueResponse.from_db(q, v, a)
        for q, v, a in queue
    ]
    return ApiResponse(data=responses)


@router.get("/exited", response_model=ApiResponse[List[VisitorQueueResponse]])
async def get_exited(event_id: str, limit: int, db: Session = Depends(get_db)):
    queue = await get_by_status(db, event_id, QueueState.exit_gate, limit)
    responses = [
        VisitorQueueResponse.from_db(q, v, a)
        for q, v, a in queue
    ]
    return ApiResponse(data=responses)
