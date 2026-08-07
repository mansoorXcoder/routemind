import uuid
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class Stop(Base):
    __tablename__ = "stops"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    route_id = Column(UUID(as_uuid=True), ForeignKey("routes.id", ondelete="CASCADE"), nullable=False, index=True)
    sequence = Column(Integer, nullable=False, index=True)
    
    customer_name = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    stop_type = Column(String(50), default="delivery")  # pickup, delivery, hub
    
    delivery_window_start = Column(DateTime, nullable=True)
    delivery_window_end = Column(DateTime, nullable=True)
    
    status = Column(String(50), default="pending")  # pending, arrived, completed, failed, skipped
    arrival_time = Column(DateTime, nullable=True)
    departure_time = Column(DateTime, nullable=True)
    
    route = relationship("Route", backref="stops")

    def __repr__(self) -> str:
        return f"<Stop Route:{self.route_id} Seq:{self.sequence} ({self.status})>"
