import logging

from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from starlette import status

from src.config import ADM_TOKEN_NAME, JWT_SECRET_KEY, ALGORITHM, ADM_TOKEN_SUB, ADM_TOKEN


def verify_admin(request: Request):
    if request.headers.get(ADM_TOKEN_NAME) != ADM_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate admin credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


async def verify_admin_token(token: str = Depends(lambda x: x.headers.get(ADM_TOKEN_NAME))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate admin credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    logging.error(f"admin token {token}")
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        adm_key: str = payload.get(ADM_TOKEN_SUB)
        logging.error(f"admin payload {payload}")
        if adm_key is None or adm_key != ADM_TOKEN:
            logging.error("admin Satu")
            raise credentials_exception
    except JWTError:
        logging.error("admin Dua")
        raise credentials_exception

    return True
