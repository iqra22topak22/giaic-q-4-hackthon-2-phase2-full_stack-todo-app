from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_exception_handlers(app: FastAPI):
    """
    Add centralized exception handlers to the FastAPI application
    """
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        Handle HTTP exceptions and return consistent error responses
        """
        logger.error(f"HTTP {exc.status_code} error: {exc.detail}")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": "HTTP_ERROR",
                    "message": exc.detail
                }
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """
        Handle general exceptions and return consistent error responses
        """
        logger.error(f"General error: {str(exc)}")
        
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An internal server error occurred"
                }
            }
        )

# Also add a custom exception for validation errors if needed
class ValidationError(Exception):
    def __init__(self, message: str, code: str = "VALIDATION_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

def register_validation_exception_handler(app: FastAPI):
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {
                    "code": exc.code,
                    "message": exc.message
                }
            }
        )