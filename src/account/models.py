import uuid
from enum import Enum

from sqlalchemy import Column, String, Enum as SQLEnum
from sqlalchemy.orm import relationship

from src.database import Base


class Role(Enum):
    USER = 'user'
    ADMIN = 'admin'


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True)
    hashed_password = Column(String)
    role = Column(SQLEnum(Role), default=Role.USER, nullable=False)

    events = relationship("Event", back_populates="creator")

    def set_as_admin(self):
        self.role = Role.ADMIN
