"""
User Service - Business Logic Layer
Spring Boot-style service with entity-to-DTO conversion
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import hashlib
import logging

from repository.user_repository import UserRepository
from schema.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from model.user import User


class UserService:
    """Service for user business logic"""
    
    def __init__(self, session: Session):
        """
        Initialize service with database session
        
        Args:
            session: SQLAlchemy Session instance
        """
        self.repository = UserRepository(session)
        self.logger = logging.getLogger(__name__)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password using SHA-256 (for demo purposes)
        In production, use bcrypt or similar
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _entity_to_dto(self, user: User) -> UserResponse:
        """
        Convert User entity to UserResponse DTO
        Spring Boot-style entity-to-DTO conversion
        
        Args:
            user: User entity
            
        Returns:
            UserResponse DTO
        """
        return UserResponse.model_validate(user)
    
    def create_user(self, user: UserCreate) -> UserResponse:
        """
        Create a new user
        
        Args:
            user: User creation data
            
        Returns:
            Created user response
            
        Raises:
            HTTPException: If username or email already exists
        """
        self.logger.info(f"Creating new user: {user.username}")
        
        # Check if username exists
        if self.repository.exists_by_username(user.username):
            self.logger.warning(f"Username already exists: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        # Check if email exists
        if self.repository.exists_by_email(user.email):
            self.logger.warning(f"Email already exists: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        # Hash password
        hashed_password = self.hash_password(user.password)
        
        # Create user entity
        user_entity = self.repository.create(user, hashed_password)
        self.logger.info(f"User created successfully with ID: {user_entity.id}")
        
        # Convert entity to DTO
        return self._entity_to_dto(user_entity)
    
    def get_user(self, user_id: int) -> UserResponse:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User response
            
        Raises:
            HTTPException: If user not found
        """
        self.logger.debug(f"Fetching user with ID: {user_id}")
        user_entity = self.repository.get_by_id(user_id)
        if not user_entity:
            self.logger.warning(f"User not found with ID: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        self.logger.debug(f"User retrieved: {user_entity.username}")
        return self._entity_to_dto(user_entity)
    
    def get_users(self, page: int = 1, page_size: int = 10) -> UserListResponse:
        """
        Get paginated list of users
        
        Args:
            page: Page number (starts from 1)
            page_size: Number of items per page
            
        Returns:
            Paginated user list response
        """
        skip = (page - 1) * page_size
        user_entities = self.repository.get_all(skip=skip, limit=page_size)
        total = self.repository.count()
        
        # Convert entities to DTOs
        user_responses = [self._entity_to_dto(entity) for entity in user_entities]
        
        return UserListResponse(
            users=user_responses,
            total=total,
            page=page,
            page_size=page_size
        )
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        """
        Update user information
        
        Args:
            user_id: User ID
            user_update: Update data
            
        Returns:
            Updated user response
            
        Raises:
            HTTPException: If user not found or email already exists
        """
        self.logger.info(f"Updating user with ID: {user_id}")
        
        # Check if user exists
        existing_user = self.repository.get_by_id(user_id)
        if not existing_user:
            self.logger.warning(f"User not found for update: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        # If email is being updated, check if it already exists
        if user_update.email and user_update.email != existing_user.email:
            if self.repository.exists_by_email(user_update.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
        
        # Update user
        updated_entity = self.repository.update(user_id, user_update)
        if not updated_entity:
            self.logger.error(f"Failed to update user with ID: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user"
            )
        
        self.logger.info(f"User updated successfully: {user_id}")
        return self._entity_to_dto(updated_entity)
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted successfully
            
        Raises:
            HTTPException: If user not found
        """
        self.logger.info(f"Deleting user with ID: {user_id}")
        
        # Check if user exists
        if not self.repository.get_by_id(user_id):
            self.logger.warning(f"User not found for deletion: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        # Delete user
        success = self.repository.delete(user_id)
        if not success:
            self.logger.error(f"Failed to delete user with ID: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete user"
            )
        
        self.logger.info(f"User deleted successfully: {user_id}")
        return True
