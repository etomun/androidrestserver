from datetime import datetime, timedelta

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.account.config import ATE_MINUTES, SECRET_KEY, ALGORITHM, RTE_DAYS
from src.account.constants import RTE, SUBJECT
from src.account.models import Account
from src.account.schemas import TokenData
from src.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def __create_token(data: dict, expires_delta: timedelta):
    exp = datetime.utcnow() + expires_delta
    exp_timestamp = int(exp.timestamp())
    return jwt.encode({RTE: exp_timestamp, **data}, SECRET_KEY, algorithm=ALGORITHM)


async def create_token(username: str):
    data = {SUBJECT: username}
    access_token = await __create_token(data, timedelta(minutes=ATE_MINUTES))
    refresh_token = await __create_token(data, timedelta(days=RTE_DAYS))
    return TokenData(access_token=access_token, refresh_token=refresh_token)


async def verify_token(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get(SUBJECT)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Account).filter(Account.username == username).first()
    if user is None:
        raise credentials_exception

    return user
