from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)
    unique_code = Column(String, index=True)
    name = Column(String, index=True)
    gender = Column(String)
    age = Column(Integer)
    is_relatives = Column(Boolean)
    address_id = Column(Integer, ForeignKey("addresses.id"), index=True)

    # Relationship with Address and VisitorQueue
    address = relationship("Address", back_populates="visitors")
    queue = relationship("VisitorQueue", back_populates="visitor")
