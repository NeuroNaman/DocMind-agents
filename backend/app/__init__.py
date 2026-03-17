"""
FastAPI application factory and configuration.
Main entry point for the application.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_config
from app.utils.logger import get_logger

logger = get_logger("app")


# Static files and templates
# Templates are handled by the React frontend in production
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting AutoDocThinker...")
    config = get_config()

    # Ensure upload folder exists
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(config.VECTOR_DB_PATH, exist_ok=True)

    logger.info("AutoDocThinker started successfully!")
    yield
    # Shutdown
    logger.info("Shutting down AutoDocThinker...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    config = get_config()

    app = FastAPI(
        title="AutoDocThinker",
        description="AI-powered document intelligence platform",
        version="2.0.0",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount static files
    # 1. API static files (uploads, etc)
    static_dir = os.path.join(os.getcwd(), "static")
    os.makedirs(static_dir, exist_ok=True)
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    # 2. Frontend static files (built React app)
    frontend_dist = os.path.join(os.getcwd(), "frontend_dist")
    if os.path.exists(frontend_dist):
        app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
    else:
        logger.warning(
            f"Frontend dist directory not found at {frontend_dist}. UI will not be served."
        )

    # Include routers
    from app.api.routes import main_router
    from app.api.routes import router as api_router

    app.include_router(main_router)
    app.include_router(api_router, prefix="/api")

    # Attach config and setup logging
    app.config = config
    from app.utils.logger import setup_logging

    setup_logging(app)

    logger.info(f"Application created in {config.ENV} mode")

    return app


# Create app instance
app = create_app()
