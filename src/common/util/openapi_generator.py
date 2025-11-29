"""
OpenAPI Schema Generator Utility
"""

import json
from pathlib import Path
from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)


def generate_openapi_file(app: FastAPI, output_path: str = "openapi.json") -> None:
    """
    Generate OpenAPI schema file from FastAPI application
    
    Args:
        app: FastAPI application instance
        output_path: Path where the OpenAPI JSON file will be saved
    """
    try:
        # Get OpenAPI schema
        openapi_schema = app.openapi()
        
        # Resolve output path
        output_file = Path(output_path)
        
        # Write to file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
        
        logger.info(f"OpenAPI schema generated successfully: {output_file.absolute()}")
    except Exception as e:
        logger.error(f"Failed to generate OpenAPI schema: {str(e)}")
