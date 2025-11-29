"""
User Repository - Data Access Layer using SQLAlchemy Core
"""

from sqlalchemy import select, insert, update, delete, func
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from model.user import users
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
    
    def create(self, user: UserCreate, hashed_password: str) -> int:
        """
        Create a new user
        
        Args:
            user: User creation data
            hashed_password: Hashed password string
            
        Returns:
            Created user ID
        """
        stmt = insert(users).values(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        result = self.session.execute(stmt)
        return result.inserted_primary_key[0]
    
    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User data dictionary or None
        """
        stmt = select(users).where(users.c.id == user_id)
        result = self.session.execute(stmt)
        row = result.fetchone()
        return dict(row._mapping) if row else None
    
    def get_all(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get all users with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of user data dictionaries
        """
        stmt = select(users).offset(skip).limit(limit).order_by(users.c.id)
        result = self.session.execute(stmt)
        return [dict(row._mapping) for row in result.fetchall()]
    
    def count(self) -> int:
        """
        Count total number of users
        
        Returns:
            Total user count
        """
        stmt = select(func.count()).select_from(users)
        result = self.session.execute(stmt)
        return result.scalar()
    
    def update(self, user_id: int, user_update: UserUpdate) -> bool:
        """
        Update user information
        
        Args:
            user_id: User ID
            user_update: Update data
            
        Returns:
            True if updated, False otherwise
        """
        # Build update dictionary with only provided fields
        update_data = user_update.model_dump(exclude_unset=True)
        
        if not update_data:
            return False
        
        update_data["updated_at"] = datetime.utcnow()
        
        stmt = update(users).where(users.c.id == user_id).values(**update_data)
        result = self.session.execute(stmt)
        return result.rowcount > 0
    
    def delete(self, user_id: int) -> bool:
        """
        Delete user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted, False otherwise
        """
        stmt = delete(users).where(users.c.id == user_id)
        result = self.session.execute(stmt)
        return result.rowcount > 0
    
    def exists_by_username(self, username: str) -> bool:
        """
        Check if username exists
        
        Args:
            username: Username
            
        Returns:
            True if exists, False otherwise
        """
        stmt = select(func.count()).select_from(users).where(users.c.username == username)
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
        stmt = select(func.count()).select_from(users).where(users.c.email == email)
        result = self.session.execute(stmt)
        return result.scalar() > 0
