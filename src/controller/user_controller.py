"""User Controller - REST API Endpoints"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import logging

from config.database_config import get_db_session
from service.user_service import UserService
from schema.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from schema.common import MessageResponse

# Create APIRouter instance
router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
def create_user(
    user: UserCreate,
    session: Session = Depends(get_db_session)
):
    """Create a new user"""
    logger.info(f"Creating user: {user.username}")
    user_service = UserService(session)
    result = user_service.create_user(user)
    logger.info(f"User created with ID: {result.id}")
    return result


@router.get(
    "/",
    response_model=UserListResponse,
    summary="Get all users"
)
def get_users(
    page: int = 1,
    page_size: int = 10,
    session: Session = Depends(get_db_session)
):
    """Get paginated list of users"""
    logger.debug(f"Fetching users: page={page}, page_size={page_size}")
    user_service = UserService(session)
    return user_service.get_users(page=page, page_size=page_size)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID"
)
def get_user(
    user_id: int,
    session: Session = Depends(get_db_session)
):
    """Get user by ID"""
    logger.debug(f"Fetching user: {user_id}")
    user_service = UserService(session)
    return user_service.get_user(user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user"
)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_db_session)
):
    """Update user information"""
    logger.info(f"Updating user: {user_id}")
    user_service = UserService(session)
    result = user_service.update_user(user_id, user_update)
    logger.info(f"User updated: {user_id}")
    return result


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    summary="Delete user"
)
def delete_user(
    user_id: int,
    session: Session = Depends(get_db_session)
):
    """Delete user by ID"""
    logger.info(f"Deleting user: {user_id}")
    user_service = UserService(session)
    user_service.delete_user(user_id)
    logger.info(f"User deleted: {user_id}")
    return MessageResponse(
        message=f"User with ID {user_id} deleted successfully",
        success=True
    )
