import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class Package(Base):
    __tablename__ = "packages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tracking_number = Column(String(50), unique=True, index=True, nullable=False)
    
    route_id = Column(UUID(as_uuid=True), ForeignKey("routes.id", ondelete="SET NULL"), nullable=True, index=True)
    stop_id = Column(UUID(as_uuid=True), ForeignKey("stops.id", ondelete="SET NULL"), nullable=True, index=True)
    
    weight = Column(Float, default=0.0)  # in kg
    volume = Column(Float, default=0.0)  # in cubic meters
    cod_amount = Column(Float, default=0.0)  # Cash on Delivery amount in local currency (INR)
    status = Column(String(50), default="pending", index=True)  # pending, loaded, delivered, failed
    delivery_type = Column(String(50), default="standard")  # standard, express, high_priority
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    route = relationship("Route", backref="packages")
    stop = relationship("Stop", backref="packages")

    def __repr__(self) -> str:
        return f"<Package {self.tracking_number} (Status: {self.status})>"
