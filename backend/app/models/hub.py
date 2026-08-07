import uuid
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from backend.app.database.base import Base

class Hub(Base):
    __tablename__ = "hubs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String(255), nullable=True)
    capacity = Column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<Hub {self.name} ({self.city})>"
