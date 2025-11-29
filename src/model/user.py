"""
User Model - SQLAlchemy ORM Entity Definition
"""

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from typing import Optional
from common.base import Base


def utc_now() -> datetime:
    """Return current UTC time with timezone info"""
    return datetime.now(timezone.utc)


class User(Base):
    """User entity - Spring Boot style ORM model"""
    __tablename__ = 'users'
    
    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # User credentials
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # User profile
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # User status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=utc_now, 
        onupdate=utc_now, 
        nullable=False
    )
    
    def __repr__(self) -> str:
        """String representation of User entity"""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
