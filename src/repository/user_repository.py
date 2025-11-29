"""
User Repository - Data Access Layer using SQLAlchemy ORM
Spring Boot JPA-style repository pattern
"""

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from model.user import User
from schema.user import UserCreate, UserUpdate


class UserRepository:
    """Repository for user data access operations"""
    
    def __init__(self, session: Session):
        """
        Initialize repository with database session
        
        Args:
            session: SQLAlchemy Session instance
        """
        self.session = session
    
    def create(self, user: UserCreate, hashed_password: str) -> User:
        """
        Create a new user
        
        Args:
            user: User creation data
            hashed_password: Hashed password string
            
        Returns:
            Created User entity
        """
        now = datetime.now(timezone.utc)
        user_entity = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False,
            created_at=now,
            updated_at=now
        )
        self.session.add(user_entity)
        self.session.flush()  # Flush to get the ID without committing
        return user_entity
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User entity or None
        """
        return self.session.get(User, user_id)
    
    def get_all(self, skip: int = 0, limit: int = 10) -> List[User]:
        """
        Get all users with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of User entities
        """
        stmt = select(User).offset(skip).limit(limit).order_by(User.id)
        result = self.session.execute(stmt)
        return list(result.scalars().all())
    
    def count(self) -> int:
        """
        Count total number of users
        
        Returns:
            Total user count
        """
        stmt = select(func.count()).select_from(User)
        result = self.session.execute(stmt)
        return result.scalar()
    
    def update(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """
        Update user information
        
        Args:
            user_id: User ID
            user_update: Update data
            
        Returns:
            Updated User entity or None if not found
        """
        user_entity = self.session.get(User, user_id)
        if not user_entity:
            return None
        
        # Update only provided fields
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user_entity, key, value)
        
        user_entity.updated_at = datetime.now(timezone.utc)
        self.session.flush()  # Flush changes
        return user_entity
    
    def delete(self, user_id: int) -> bool:
        """
        Delete user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted, False otherwise
        """
        user_entity = self.session.get(User, user_id)
        if not user_entity:
            return False
        
        self.session.delete(user_entity)
        self.session.flush()
        return True
    
    def exists_by_username(self, username: str) -> bool:
        """
        Check if username exists
        
        Args:
            username: Username
            
        Returns:
            True if exists, False otherwise
        """
        stmt = select(func.count()).select_from(User).where(User.username == username)
        result = self.session.execute(stmt)
        return result.scalar() > 0
    
    def exists_by_email(self, email: str) -> bool:
        """
        Check if email exists
        
        Args:
            email: Email address
            
        Returns:
            True if exists, False otherwise
        """
        stmt = select(func.count()).select_from(User).where(User.email == email)
        result = self.session.execute(stmt)
        return result.scalar() > 0
