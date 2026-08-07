import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    
    title = Column(String(100), nullable=False)
    message = Column(String(500), nullable=False)
    type = Column(String(50), default="system", index=True)  # traffic, weather, pickup, failure, maintenance, ai, system
    priority = Column(String(50), default="medium")  # low, medium, high, critical
    is_read = Column(Boolean, default=False, index=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship("User", backref="notifications")

    def __repr__(self) -> str:
        return f"<Notification Title:{self.title} Type:{self.type} Read:{self.is_read}>"
