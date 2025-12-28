"""SQLAlchemy database models."""

from sqlalchemy import Column, String, Boolean, DateTime, Integer, JSON
from sqlalchemy.sql import func
from api.database import Base


class TaskDB(Base):
    """Task database model."""

    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(2000), default="")
    completed = Column(Boolean, default=False)
    priority = Column(String(10), nullable=True)  # HIGH, MEDIUM, LOW, or None
    tags = Column(JSON, default=list)  # Stored as JSON array
    due_date = Column(String(10), nullable=True)  # YYYY-MM-DD format
    recurring = Column(String(10), nullable=True)  # daily, weekly, monthly
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority,
            "tags": self.tags or [],
            "due_date": self.due_date,
            "recurring": self.recurring,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
