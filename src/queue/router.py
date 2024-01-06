import logging
from typing import List

from fastapi import APIRouter, Depends
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.account.models import Account
from src.database import get_db
from src.dependencies import verify_account, verify_admin, get_websocket_manager
from src.queue.dependencies import verify_queue_event_started
from src.queue.schemas import QueueResponse
from src.queue.service import *
from src.schemes import ApiResponse
from src.websocket import WSManager

router = APIRouter()


@router.post("/add", response_model=ApiResponse[QueueResponse])
async def add_queue(data: UpdateQueue, db: Session = Depends(get_db), user: Account = Depends(verify_account),
                    ws_mgr: WSManager = Depends(get_websocket_manager)):
    logging.info(user.id)
    event = await verify_queue_event_started(data.event_id, db)
    queue = await add_new(db, data)
    # Notify connected WebSocket clients about the update
    await ws_mgr.broadcast(f"Queue updated for event_id: {event.name}")
    return ApiResponse(data=QueueResponse.from_db(queue))


@router.post("/enter-gate", response_model=ApiResponse[QueueResponse])
async def enter_gate(data: UpdateQueue, db: Session = Depends(get_db), user: Account = Depends(verify_account),
                     ws_mgr: WSManager = Depends(get_websocket_manager)):
    logging.info(user.id)
    event = await verify_queue_event_started(data.event_id, db)
    queue = await update_state(db, data, QueueState.enter_gate)

    # Notify connected WebSocket clients about the update
    await ws_mgr.broadcast(f"Queue updated for event_id: {event.name}")
    return ApiResponse(data=QueueResponse.from_db(queue))


@router.post("/exit-gate", response_model=ApiResponse[QueueResponse])
async def exit_gate(data: UpdateQueue, db: Session = Depends(get_db), user: Account = Depends(verify_account),
                    ws_mgr: WSManager = Depends(get_websocket_manager)):
    logging.info(user.id)
    event = await verify_queue_event_started(data.event_id, db)
    queue = await update_state(db, data, QueueState.exit_gate)

    # Notify connected WebSocket clients about the update
    await ws_mgr.broadcast(f"Queue updated for event_id: {event.name}")
    return ApiResponse(data=QueueResponse.from_db(queue))


@router.get("/waiting/{event_id}", response_model=ApiResponse[List[QueueResponse]])
async def get_waiting(event_id: str, limit: int, db: Session = Depends(get_db)):
    queue = await get_by_state(db, event_id, QueueState.register, limit)
    responses = [QueueResponse.from_db(q) for q in queue]
    return ApiResponse(data=responses)


@router.websocket("/ws/waiting/{event_id}")
async def get_waiting(ws: WebSocket, event_id: str, ws_mgr: WSManager = Depends(get_websocket_manager)):
    await ws_mgr.connect(ws)
    try:
        await ws_mgr.broadcast(f"Halo")
        while True:
            # Keep WebSocket connection alive
            message = await ws.receive_text()
            print(message)
    except WebSocketDisconnect:
        pass
    finally:
        ws_mgr.disconnect(ws)


@router.get("/entered/{event_id}", response_model=ApiResponse[List[QueueResponse]])
async def get_entered(event_id: str, limit: int, db: Session = Depends(get_db)):
    queue = await get_by_state(db, event_id, QueueState.enter_gate, limit)
    responses = [QueueResponse.from_db(q) for q in queue]
    return ApiResponse(data=responses)


@router.get("/exited/{event_id}", response_model=ApiResponse[List[QueueResponse]])
async def get_exited(event_id: str, limit: int, db: Session = Depends(get_db)):
    queue = await get_by_state(db, event_id, QueueState.exit_gate, limit)
    responses = [QueueResponse.from_db(q) for q in queue]
    return ApiResponse(data=responses)


@router.post("/delete/{queue_id}", response_model=ApiResponse[bool])
async def delete_queue(queue_id: str, db: Session = Depends(get_db), admin: Account = Depends(verify_admin)):
    logging.info(admin.id)
    success = await delete(db, queue_id)
    return ApiResponse(data=success)


@router.post('/clear')
async def clear_queue(db: Session = Depends(get_db), user: Account = Depends(verify_admin)):
    logging.info(user.username)
    result = await clear(db)
    return ApiResponse(data=result)
