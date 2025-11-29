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
