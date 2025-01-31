from fastapi import HTTPException, status
from typing import Type, Optional
from pydantic import BaseModel, ValidationError
import logging

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base class for API errors."""
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: Optional[str] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

def handle_validation_error(error: ValidationError) -> HTTPException:
    """Handle Pydantic validation errors."""
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={
            "message": "Validation error",
            "errors": error.errors()
        }
    )

def handle_database_error(error: Exception) -> HTTPException:
    """Handle database-related errors."""
    logger.error(f"Database error: {str(error)}")
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An error occurred while processing your request"
    )

def handle_not_found(
    model_name: str,
    identifier: str | int
) -> HTTPException:
    """Handle not found errors."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{model_name} with id {identifier} not found"
    )

def handle_api_error(error: APIError) -> HTTPException:
    """Handle custom API errors."""
    return HTTPException(
        status_code=error.status_code,
        detail={
            "message": error.message,
            "error_code": error.error_code
        }
    )
