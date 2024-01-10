import asyncio
import logging
from typing import List

from fastapi import APIRouter, Depends
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.database import get_db
from src.dependencies import verify_account, verify_admin, get_websocket_manager
from src.queue.dependencies import verify_queue_event_started
from src.queue.schemas import QueueResponse, SocketMessage
from src.queue.service import *
from src.schemes import ApiResponse
from src.websocket import WSManager

router = APIRouter()


@router.post("/add", response_model=ApiResponse[QueueResponse])
async def add_queue(data: UpdateQueue, db: Session = Depends(get_db), user: Account = Depends(verify_account),
                    ws_mgr: WSManager = Depends(get_websocket_manager)):
    logging.info(user.id)
    event = await verify_queue_event_started(data.event_id, db)
    queue = await add_new(db, user, data)
    payload = SocketMessage(event_id=event.id, message_code=QueueState.register.value,
                            message=f"{queue.member.name} just arrived to {queue.event.name}").dict()
    await ws_mgr.send_message(event.id, payload)
    return ApiResponse(data=QueueResponse.from_db(queue))


@router.post("/enter-gate", response_model=ApiResponse[QueueResponse])
async def enter_gate(data: UpdateQueue, db: Session = Depends(get_db), user: Account = Depends(verify_account),
                     ws_mgr: WSManager = Depends(get_websocket_manager)):
    logging.info(user.id)
    event = await verify_queue_event_started(data.event_id, db)
    queue = await update_state(db, data, QueueState.enter_gate)
    payload = SocketMessage(event_id=event.id, message_code=QueueState.enter_gate.value,
                            message=f"{queue.member.name} just entered the Gate of {queue.event.name}").dict()
    await ws_mgr.send_message(event.id, payload)
    return ApiResponse(data=QueueResponse.from_db(queue))


@router.post("/exit-gate", response_model=ApiResponse[QueueResponse])
async def exit_gate(data: UpdateQueue, db: Session = Depends(get_db), user: Account = Depends(verify_account),
                    ws_mgr: WSManager = Depends(get_websocket_manager)):
    logging.info(user.id)
    event = await verify_queue_event_started(data.event_id, db)
    queue = await update_state(db, data, QueueState.exit_gate)

    payload = SocketMessage(event_id=event.id, message_code=QueueState.exit_gate.value,
                            message=f"{queue.member.name} just exited the Gate of {queue.event.name}").dict()
    await ws_mgr.send_message(event.id, payload)
    return ApiResponse(data=QueueResponse.from_db(queue))


@router.get("/{event_id}", response_model=ApiResponse[List[QueueResponse]])
async def get_all_visitors(event_id: str, db: Session = Depends(get_db)):
    queue = await get_all(db, event_id)
    if not queue:
        return ApiResponse(data=None, error_message="Queue not found")
    else:
        return ApiResponse(data=[QueueResponse.from_db(q) for q in queue])


@router.get("/waiting/{event_id}", response_model=ApiResponse[List[QueueResponse]])
async def get_waiting(event_id: str, limit: int = 50, db: Session = Depends(get_db)):
    queue = await get_by_state(db, event_id, QueueState.register, limit)
    if not queue:
        return ApiResponse(data=None, error_message="Queue not found")
    else:
        return ApiResponse(data=[QueueResponse.from_db(q) for q in queue])


@router.get("/entered/{event_id}", response_model=ApiResponse[List[QueueResponse]])
async def get_entered(event_id: str, limit: int = 50, db: Session = Depends(get_db)):
    queue = await get_by_state(db, event_id, QueueState.enter_gate, limit)
    if not queue:
        return ApiResponse(data=None, error_message="Queue not found")
    else:
        return ApiResponse(data=[QueueResponse.from_db(q) for q in queue])


@router.get("/exited/{event_id}", response_model=ApiResponse[List[QueueResponse]])
async def get_exited(event_id: str, limit: int = 50, db: Session = Depends(get_db)):
    queue = await get_by_state(db, event_id, QueueState.exit_gate, limit)
    if not queue:
        return ApiResponse(data=None, error_message="Queue not found")
    else:
        return ApiResponse(data=[QueueResponse.from_db(q) for q in queue])


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


@router.websocket("/ws/{event_id}")
async def listen_queue(ws: WebSocket, event_id: str, ws_mgr: WSManager = Depends(get_websocket_manager),
                       db: Session = Depends(get_db)):
    try:
        # Verify the event and decide whether to accept or close the connection
        event = await verify_queue_event_started(event_id, db)
        if event is None:
            await ws.close(reason="Event is not started")
            return

        # Accept the WebSocket connection
        await ws.accept()

        # Connect the WebSocket to the manager
        await ws_mgr.connect(event_id, ws)

        # Main loop to handle WebSocket messages
        while True:
            await asyncio.sleep(1)
            await ws.receive_json()

    except WebSocketDisconnect:
        # Handle disconnect
        await ws_mgr.disconnect(event_id, ws)
