import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.database import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(String, primary_key=True, unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    village = Column(String, index=True, unique=True, nullable=False)
    sub_district = Column(String, index=True, nullable=False)
    district = Column(String, index=True, nullable=False)
    regency = Column(String, nullable=False)
    province = Column(String, nullable=False)

    # Relationship with Member
    members = relationship("Member", back_populates="address")

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in Address.__table__.columns}
