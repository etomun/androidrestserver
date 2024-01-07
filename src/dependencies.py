from fastapi import HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from src.account.models import Account, Role
from src.config import ADM_TOKEN_NAME, ADM_TOKEN, JWT_SECRET_KEY, ALGORITHM
from src.constants import SUBJECT
from src.database import get_db
from src.websocket import WSManager

# Web Socket

ws_manager = WSManager()


async def get_websocket_manager():
    return ws_manager


# JWT Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def verify_account(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status.HTTP_401_UNAUTHORIZED, "Could not validate credentials")

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get(SUBJECT)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Account).filter_by(username=username).first()
    if user is None:
        raise credentials_exception

    return user


def verify_token_su(request: Request):
    if request.headers.get(ADM_TOKEN_NAME) != ADM_TOKEN:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Could not validate admin credentials")
    return True


def verify_admin(user: Account = Depends(verify_account)):
    if user.role is Role.ADMIN:
        return user
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You have no permissions to perform this action")
