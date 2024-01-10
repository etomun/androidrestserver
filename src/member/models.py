import uuid
from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from src.database import Base


class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'


class Member(Base):
    __tablename__ = "members"

    id = Column(String, primary_key=True, unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    unique_code = Column(String, index=True, unique=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    gender = Column(String, nullable=False)
    address_id = Column(String, ForeignKey("addresses.id"), index=True, nullable=False)
    pic_id = Column(String, ForeignKey("accounts.id"), index=True, nullable=False)
    date_registered = Column(DateTime, server_default=func.now())
    age = Column(Integer)
    is_relatives = Column(Boolean)

    # Relationship with Address, Account(pic) and VisitorQueue
    address = relationship("Address", back_populates="members")
    pic = relationship("Account", back_populates="registered_members")
    queue = relationship("VisitorQueue", back_populates="member")
