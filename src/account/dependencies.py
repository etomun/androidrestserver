from datetime import datetime, timedelta

from jose import jwt

from src.account.config import ATE_MINUTES, RTE_DAYS
from src.account.constants import RTE
from src.account.schemas import TokenData
from src.config import JWT_SECRET_KEY, ALGORITHM
from src.constants import SUBJECT


async def __create_token(data: dict, expires_delta: timedelta):
    exp = datetime.utcnow() + expires_delta
    exp_timestamp = int(exp.timestamp())
    return jwt.encode({RTE: exp_timestamp, **data}, JWT_SECRET_KEY, algorithm=ALGORITHM)


async def create_token(username: str):
    data = {SUBJECT: username}
    access_token = await __create_token(data, timedelta(minutes=ATE_MINUTES))
    refresh_token = await __create_token(data, timedelta(days=RTE_DAYS))
    return TokenData(access_token=access_token, refresh_token=refresh_token)
