"""
API module for FastAPI routes.
Contains all API endpoints and routers.
"""

from app.api.routes import main_router, router

__all__ = ["router", "main_router"]
