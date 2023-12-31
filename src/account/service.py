from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.account.config import CREATE_ADMIN_KEY
from src.account.models import Account
from src.account.schemas import CreateAccount, Login, ChangePassword, ChangePhone, ChangeName
from src.account.utils import hash_password, verify_password


async def create(db: Session, data: CreateAccount, admin_key: str = None, ):
    if admin_key is not None and admin_key != CREATE_ADMIN_KEY:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Admin Key")

    if db.query(Account).filter(Account.username == data.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    if db.query(Account).filter(Account.phone == data.phone).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone already registered")

    hashed_password = hash_password(data.password)
    new_user = Account(
        username=data.username,
        hashed_password=hashed_password,
        phone=data.phone,
        name=data.name
    )
    if admin_key is not None and admin_key == CREATE_ADMIN_KEY:
        new_user.set_as_admin()

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def authenticate(db: Session, data: Login) -> Account | None:
    user = db.query(Account).filter(Account.username == data.username).first()
    if user and verify_password(data.password, user.hashed_password):
        return user
    return None


async def get_account(db: Session, uid: str):
    return db.query(Account).filter(Account.id == uid).first()


async def get_accounts(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Account).offset(skip).limit(limit).all()


async def update_password(db: Session, data: ChangePassword, user: Account):
    db_account = db.query(Account).filter(Account.id == user.id).first()
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if verify_password(data.old_password, db_account.hashed_password):
        db_account.hashed_password = hash_password(data.new_password)
        db.commit()
        db.refresh(db_account)
        return db_account
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is not valid",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def update_phone(db: Session, data: ChangePhone, user: Account):
    db_account = db.query(Account).filter(Account.id == user.id).first()
    db_account.phone = data.new_phone
    db.commit()
    db.refresh(db_account)
    return db_account


async def update_name(db: Session, data: ChangeName, user: Account):
    db_account = db.query(Account).filter(Account.id == user.id).first()
    db_account.name = data.new_name
    db.commit()
    db.refresh(db_account)
    return db_account


async def delete(db: Session, uid: str, user: Account) -> bool:
    db_user_account = db.query(Account).filter_by(id=user.id, role=user.role).first()
    db_target_account = db.query(Account).filter(Account.id == uid).first()

    forbidden = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if db_user_account is None or db_target_account is None:
        raise forbidden

    try:
        db.delete(db_user_account)
        db.commit()
        return True
    except:
        return False
