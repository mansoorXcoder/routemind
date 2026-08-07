import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, Date, Integer
from sqlalchemy.dialects.postgresql import UUID
from backend.app.database.base import Base

class Analytics(Base):
    __tablename__ = "analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, unique=True, nullable=False, index=True)
    
    routes_completed = Column(Integer, default=0)
    packages_delivered = Column(Integer, default=0)
    fuel_used = Column(Float, default=0.0)  # in liters
    fuel_saved = Column(Float, default=0.0)  # in liters
    distance = Column(Float, default=0.0)  # in km
    delay = Column(Float, default=0.0)  # in minutes
    optimization_score = Column(Float, default=100.0)

    def __repr__(self) -> str:
        return f"<Analytics Date:{self.date}>"

class TrafficEvent(Base):
    __tablename__ = "traffic_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    severity = Column(String(50), nullable=False, index=True)  # low, medium, high
    description = Column(String(500), nullable=True)
    
    start_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    end_time = Column(DateTime, nullable=True)
    source = Column(String(100), default="internal")

    def __repr__(self) -> str:
        return f"<TrafficEvent Location:{self.location} Severity:{self.severity}>"

class WeatherEvent(Base):
    __tablename__ = "weather_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city = Column(String(100), nullable=False, index=True)
    temperature = Column(Float, nullable=True)
    condition = Column(String(100), nullable=False)  # Rain, Storm, Clear, Fog, Snow
    risk_level = Column(String(50), default="low")  # low, medium, high
    
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<WeatherEvent City:{self.city} Condition:{self.condition}>"
