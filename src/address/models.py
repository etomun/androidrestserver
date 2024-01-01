import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.database import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    village = Column(String, index=True, nullable=False)
    district = Column(String, index=True, nullable=False)
    line = Column(String, index=True)

    # Relationship with Visitor
    visitors = relationship("Visitor", back_populates="address")
