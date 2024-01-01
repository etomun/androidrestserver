from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.account.dependencies import verify_token
from src.account.models import Account
from src.database import get_db
from src.queue.models import QueueState
from src.queue.schemas import UpdateQueue
from src.queue.service import update_state, add_new, get_by_status

router = APIRouter()


@router.post("/add")
async def add_queue(data: UpdateQueue, db: Session = Depends(get_db), user: Account = Depends(verify_token)):
    return await add_new(db, user, data)


@router.post("/enter-gate")
async def enter_gate(data: UpdateQueue, db: Session = Depends(get_db), user: Account = Depends(verify_token)):
    return await update_state(db, user, data, QueueState.enter_gate)


@router.post("/exit-gate")
async def exit_gate(data: UpdateQueue, db: Session = Depends(get_db), user: Account = Depends(verify_token)):
    return await update_state(db, user, data, QueueState.exit_gate)


@router.get("/waiting")
async def get_waiting(db: Session = Depends(get_db)):
    return await get_by_status(db, QueueState.register)


@router.get("/entered")
async def get_entered(db: Session = Depends(get_db)):
    return await get_by_status(db, QueueState.enter_gate)


@router.get("/exited")
async def get_exited(db: Session = Depends(get_db)):
    return await get_by_status(db, QueueState.exit_gate)
