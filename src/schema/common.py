"""
Common Schemas - Shared DTOs
"""

from pydantic import BaseModel, Field
from typing import Any, Optional


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str = Field(..., description="Response message")
    success: bool = Field(default=True, description="Operation success status")
    data: Optional[Any] = Field(None, description="Optional additional data")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Operation completed successfully",
                "success": True,
                "data": None
            }
        }
    }


class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints"""
    page: int = Field(default=1, ge=1, description="Page number (starts from 1)")
    page_size: int = Field(default=10, ge=1, le=100, description="Items per page (max 100)")
    
    @property
    def offset(self) -> int:
        """Calculate offset for database query"""
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """Get limit for database query"""
        return self.page_size
