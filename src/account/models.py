import uuid
from enum import Enum

from sqlalchemy import Column, String, Enum as SQLEnum, DateTime, func
from sqlalchemy.orm import relationship

from src.database import Base


class Role(Enum):
    USER = 'user'
    ADMIN = 'admin'


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True, unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    username = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(Role), default=Role.USER, nullable=False)
    pic_id = Column(String, nullable=True)
    created_date = Column(DateTime, server_default=func.now())

    # Relationship with Event(as Creator) and Member(as PIC)
    events = relationship("Event", back_populates="creator")
    registered_members = relationship("Member", back_populates="pic")

    def set_as_admin(self):
        self.role = Role.ADMIN
