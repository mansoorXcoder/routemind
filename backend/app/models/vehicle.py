import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_number = Column(String(50), unique=True, index=True, nullable=False)
    vehicle_type = Column(String(50), nullable=False)  # Truck, Van, Bike, Three-Wheeler
    capacity = Column(Float, nullable=False)  # capacity in kg
    fuel_type = Column(String(50), nullable=True)  # Diesel, Petrol, CNG, EV
    current_driver = Column(String(100), nullable=True)
    status = Column(String(50), default="offline", index=True)  # online, idle, offline, emergency
    
    current_latitude = Column(Float, nullable=True)
    current_longitude = Column(Float, nullable=True)
    
    hub_id = Column(UUID(as_uuid=True), ForeignKey("hubs.id"), nullable=True)
    hub = relationship("Hub", backref="vehicles")
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<Vehicle {self.vehicle_number} ({self.vehicle_type})>"
