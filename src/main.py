import logging

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from starlette.staticfiles import StaticFiles

from src import account, member, address, event, queue
from src.database import init_db
from src.dependencies import verify_account, get_websocket_manager
from src.exceptions import GeneralException
from src.websocket import WSManager

app = FastAPI(title="Visit Marthapura")

# Initialize the database tables
init_db()


@app.exception_handler(GeneralException)
async def general_exception_handler(request, exc: GeneralException):
    logging.info(request)
    return exc.as_response()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    logging.info(request)
    general_exc = GeneralException(exc.status_code, exc.detail, exc.status_code, exc.detail)
    return general_exc.as_response()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.info(request)
    code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return GeneralException(code, f'{exc.errors()}', code, exc.body).as_response()


@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc: Exception):
    logging.info(request)
    status_500 = status.HTTP_500_INTERNAL_SERVER_ERROR
    message_500 = "Internal Server Error"
    if isinstance(exc, IntegrityError):
        general_exc = GeneralException(status_500, message_500, 12, str(exc))
    else:
        general_exc = GeneralException(status_500, message_500, 11, str(exc))
    return general_exc.as_response()


app.include_router(account.router, prefix="/api/auth", tags=["Account"])
app.include_router(event.router, prefix="/api/event", tags=["Event"])
app.include_router(queue.router, prefix="/api/queue", tags=["Queue of Visitor"])
app.include_router(address.router, prefix="/api/address", tags=["Address"], dependencies=[Depends(verify_account)])
app.include_router(member.router, prefix="/api/member", tags=["Member"], dependencies=[Depends(verify_account)])


@app.post('/ws/broadcast', tags=['Test WebSocket'])
async def ws_test_broadcast(event_id: str, message: str, ws_mgr: WSManager = Depends(get_websocket_manager)):
    await ws_mgr.send_message(event_id, {
        "event_id": event_id,
        "message": f"Test websocket {message} of {event_id}"
    })


# Mount the ReactJS build directory as a static path
app.mount("/", StaticFiles(directory="web/build", html=True), name="static")
