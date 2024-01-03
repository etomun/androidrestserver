from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.account.models import Account
from src.account.schemas import AccountCreate, AccountLogin, ChangePassword, ChangePhone, ChangeName
from src.account.utils import hash_password, verify_password


async def create(db: Session, data: AccountCreate, is_admin: bool = False):
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
    if is_admin:
        new_user.set_as_admin()

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def authenticate(db: Session, data: AccountLogin) -> Account | None:
    user = db.query(Account).filter(Account.username == data.username).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User Not Found")
    if verify_password(data.password, user.hashed_password):
        return user


async def get_by_id(db: Session, uid: str):
    user = db.query(Account).filter(Account.id == uid).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User Not Found")
    return user


async def get_accounts(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Account).offset(skip).limit(limit).all()


async def update_password(db: Session, data: ChangePassword, user: Account):
    user = db.query(Account).filter(Account.id == user.id).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User Not Found")
    if verify_password(data.old_password, user.hashed_password):
        user.hashed_password = hash_password(data.new_password)
        db.commit()
        db.refresh(user)
        return user
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Old password is not valid")


async def update_phone(db: Session, data: ChangePhone, user: Account):
    user = db.query(Account).filter(Account.id == user.id).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User Not Found")
    user.phone = data.new_phone
    db.commit()
    db.refresh(user)
    return user


async def update_name(db: Session, data: ChangeName, user: Account):
    user = db.query(Account).filter(Account.id == user.id).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User Not Found")
    user.name = data.new_name
    db.commit()
    db.refresh(user)
    return user


async def delete(db: Session, uid: str, user: Account) -> bool:
    db_user_account = db.query(Account).filter_by(id=user.id, role=user.role).first()
    db_target_account = db.query(Account).filter(Account.id == uid).first()
    if db_user_account is None or db_target_account is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User Not Found")

    try:
        db.delete(db_user_account)
        db.commit()
        return True
    except:
        return False
