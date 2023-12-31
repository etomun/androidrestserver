from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    village = Column(String, index=True)
    district = Column(String, index=True)
    line = Column(String, index=True)

    # Relationship with Visitor
    visitors = relationship("Visitor", back_populates="address")
