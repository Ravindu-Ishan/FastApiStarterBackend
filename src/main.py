"""
FastAPI Starter Template - Main Entry Point
"""
#test change
import logging
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config.app_config import config
from config.database_config import init_db, db
from config.log_config import setup_logging, setup_audit_logger
from controller import user_router
from common.util import generate_openapi_file, print_banner

# Configure logging using centralized log configuration
setup_logging(
    log_level=config.log_level,
    detailed=config.detailed_logs,
    log_to_file=config.log_to_file,
    log_dir=config.log_dir,
    rotation_type=config.rotation_type,
    max_bytes=config.max_bytes,
    backup_count=config.backup_count,
    rotation_when=config.rotation_when,
    rotation_interval=config.rotation_interval,
    rotation_backup_count=config.rotation_backup_count,
)

# Setup separate audit logger
audit_logger = setup_audit_logger(
    log_dir=config.log_dir,
    rotation_type=config.rotation_type,
    max_bytes=config.max_bytes,
    backup_count=config.backup_count,
    rotation_when=config.rotation_when,
    rotation_interval=config.rotation_interval,
    rotation_backup_count=config.rotation_backup_count,
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup - Show banner
    print_banner()
    logger.info("Starting FastAPI application...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    
    # Generate OpenAPI schema file
    generate_openapi_file(app, output_path="openapi.json")
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastAPI application...")
    db.close()
    logger.info("Database connections closed")
    
    # Clean up banner marker file on shutdown
    import os
    if os.path.exists('.banner_session'):
        os.remove('.banner_session')


# Create FastAPI application
app = FastAPI(
    title=config.app_name,
    description="FastAPI Starter Template with SQLAlchemy Core, MySQL/Oracle support, and clean architecture",
    version="1.0.0",
    debug=config.debug,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=config.get("cors", "allow_credentials", True),
    allow_methods=config.get("cors", "allow_methods", ["*"]),
    allow_headers=config.get("cors", "allow_headers", ["*"]),
)


# Add request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID to each request for tracing"""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses to audit log"""
    start_time = time.time()
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    # Log incoming request
    audit_logger.info(
        f"REQUEST | {request_id} | {request.method} {request.url.path} | Client: {request.client.host}"
    )
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    audit_logger.info(
        f"RESPONSE | {request_id} | {request.method} {request.url.path} | "
        f"Status: {response.status_code} | Time: {process_time:.3f}s"
    )
    
    return response


# Register routers
app.include_router(user_router, prefix=config.api_prefix)


@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {
        "message": f"Welcome to {config.app_name}",
        "version": "1.0.0",
        "database": config.db_type,
        "docs": "/docs",
        "api_prefix": config.api_prefix
    }


if __name__ == "__main__":
    import uvicorn
    import sys
    
    logger.info(f"Starting {config.app_name} on {config.server_host}:{config.server_port}")
    
    # Add parent directory to path so src module can be imported
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # For direct python execution, use module path
    uvicorn.run(
        "src.main:app",
        host=config.server_host,
        port=config.server_port,
        reload=config.server_reload,
        reload_excludes=[
            "**/logs/**",
            "**/*.log",
            "**/openapi.json",
            "**/*.db",
            "**/*.sqlite",
            "**/*.sqlite-journal",
            "**/__pycache__/**",
        ],
        log_config=None,  # Disable uvicorn's log config, use our format
        log_level="warning"  # Only show warnings from uvicorn itself
    )
