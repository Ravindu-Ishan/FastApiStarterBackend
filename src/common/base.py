"""
Common Base for all ORM Models
Centralized DeclarativeBase to avoid circular imports and manual model registration
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all ORM entity models
    All models should inherit from this Base class
    
    Example:
        from common.base import Base
        
        class User(Base):
            __tablename__ = "users"
            id: Mapped[int] = mapped_column(primary_key=True)
    """
    pass
