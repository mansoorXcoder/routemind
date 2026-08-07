import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Boolean, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class Optimization(Base):
    __tablename__ = "optimizations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    route_id = Column(UUID(as_uuid=True), ForeignKey("routes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    optimization_type = Column(String(50), nullable=False)  # routing, dynamic_replan, sequencing
    algorithm = Column(String(50), nullable=False, index=True)  # or-tools, adaptive-ai
    
    old_route = Column(JSON, nullable=True)  # stores old stops sequence
    new_route = Column(JSON, nullable=True)  # stores new stops sequence
    
    distance_saved = Column(Float, default=0.0)  # in km
    time_saved = Column(Float, default=0.0)  # in minutes
    fuel_saved = Column(Float, default=0.0)  # in liters
    carbon_saved = Column(Float, default=0.0)  # in kg CO2
    confidence = Column(Float, default=100.0)
    reason = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    route = relationship("Route", backref="optimizations")

    def __repr__(self) -> str:
        return f"<Optimization Route:{self.route_id} Alg:{self.algorithm}>"

class AIDecision(Base):
    __tablename__ = "ai_decisions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    route_id = Column(UUID(as_uuid=True), ForeignKey("routes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    decision = Column(String(100), nullable=False)  # e.g., re_route, bypass, split_delivery
    confidence = Column(Float, default=100.0)
    reason = Column(String(1000), nullable=True)
    llm_model = Column(String(100), nullable=True)
    execution_time = Column(Float, default=0.0)  # in seconds
    cost = Column(Float, default=0.0)  # estimated api token cost
    approved = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    route = relationship("Route", backref="ai_decisions")

    def __repr__(self) -> str:
        return f"<AIDecision Route:{self.route_id} Approved:{self.approved}>"

class RouteHistory(Base):
    __tablename__ = "route_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    route_id = Column(UUID(as_uuid=True), ForeignKey("routes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    version = Column(Integer, nullable=False, default=1)
    modified_by = Column(String(100), nullable=True)  # user ID or agent name
    change_reason = Column(String(500), nullable=True)
    
    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    route = relationship("Route", backref="history")

    def __repr__(self) -> str:
        return f"<RouteHistory Route:{self.route_id} Ver:{self.version}>"
