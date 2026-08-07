import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class Route(Base):
    __tablename__ = "routes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    route_code = Column(String(100), unique=True, index=True, nullable=False)
    
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=True)
    driver_id = Column(UUID(as_uuid=True), ForeignKey("drivers.id"), nullable=True)
    hub_id = Column(UUID(as_uuid=True), ForeignKey("hubs.id"), nullable=True)
    
    date = Column(Date, nullable=False, index=True)
    status = Column(String(50), default="planned", index=True)  # planned, active, completed, cancelled, pending_approval
    
    planned_distance = Column(Float, default=0.0)  # in km
    actual_distance = Column(Float, default=0.0)
    planned_duration = Column(Float, default=0.0)  # in minutes
    actual_duration = Column(Float, default=0.0)
    optimization_score = Column(Float, default=100.0)
    
    vehicle = relationship("Vehicle", backref="routes")
    driver = relationship("Driver", backref="routes")
    hub = relationship("Hub", backref="routes")
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<Route {self.route_code} ({self.status})>"
