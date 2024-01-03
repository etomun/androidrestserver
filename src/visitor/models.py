import uuid

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from src.database import Base


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    unique_code = Column(String, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    gender = Column(String)
    age = Column(Integer)
    is_relatives = Column(Boolean)
    date_registered = Column(DateTime, server_default=func.now())
    address_id = Column(String, ForeignKey("addresses.id"), index=True, nullable=False)

    # Relationship with Address and VisitorQueue
    address = relationship("Address", back_populates="visitors")
    queue = relationship("VisitorQueue", back_populates="visitor")
