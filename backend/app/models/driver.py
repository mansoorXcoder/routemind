import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class Driver(Base):
    __tablename__ = "drivers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=False)
    license_number = Column(String(100), nullable=True)
    experience = Column(Integer, nullable=True)  # experience in years
    rating = Column(Float, default=5.0)
    current_vehicle = Column(String(100), nullable=True)
    status = Column(String(50), default="offline", index=True)  # online, idle, offline, emergency
    
    hub_id = Column(UUID(as_uuid=True), ForeignKey("hubs.id"), nullable=True)
    hub = relationship("Hub", backref="drivers")
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<Driver {self.name} (ID: {self.employee_id})>"
