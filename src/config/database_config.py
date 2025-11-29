"""
Database Configuration and Connection Management
Supports MySQL and Oracle databases with SQLAlchemy ORM
"""

from sqlalchemy import create_engine, MetaData, pool
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from typing import Optional
import logging

from config.app_config import config
from common.base import Base  # Import centralized Base

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Database connection manager - Singleton pattern"""
    
    _instance: Optional['DatabaseConnection'] = None
    _engine: Optional[Engine] = None
    metadata: MetaData = MetaData()
    
    def __new__(cls):
        """Singleton pattern to ensure single database connection"""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def _build_connection_url(self) -> str:
        """
        Build database connection URL based on db_type
        
        Returns:
            SQLAlchemy connection URL string
        
        Note:
            This method is also used by Alembic for migrations.
            It reads from deployment.toml configuration.
        """
        db_type = config.db_type.lower()
        
        if db_type == "sqlite":
            # SQLite connection URL
            # Format: sqlite:///path/to/database.db
            sqlite_file = config.get("database", "sqlite_file", "fastapi_db.sqlite")
            url = f"sqlite:///{sqlite_file}"
            logger.info(f"Building SQLite connection URL for file: {sqlite_file}")
            
        elif db_type == "mysql":
            # MySQL connection URL
            # Format: mysql+pymysql://user:password@host:port/database
            username = config.db_username
            password = config.db_password
            host = config.db_host
            port = config.db_port
            database = config.db_database
            url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
            logger.info(f"Building MySQL connection URL for database: {database}")
            
        elif db_type == "oracle":
            # Oracle connection URL with service name
            # Format: oracle+cx_oracle://user:password@host:port/?service_name=service
            username = config.db_username
            password = config.db_password
            host = config.db_host
            port = config.db_port
            service_name = config.db_service_name
            url = f"oracle+cx_oracle://{username}:{password}@{host}:{port}/?service_name={service_name}"
            logger.info(f"Building Oracle connection URL for service: {service_name}")
            
        else:
            raise ValueError(f"Unsupported database type: {db_type}. Supported types: sqlite, mysql, oracle")
        
        return url
    
    def get_engine(self) -> Engine:
        """
        Get or create database engine
        
        Returns:
            SQLAlchemy Engine instance
        """
        if self._engine is None:
            self._engine = self._create_engine()
        return self._engine
    
    def _create_engine(self) -> Engine:
        """
        Create SQLAlchemy engine with appropriate configuration
        
        Returns:
            Configured SQLAlchemy Engine
        """
        connection_url = self._build_connection_url()
        
        # Engine configuration
        engine_config = {
            "echo": False,  # Never use echo - we handle SQL logging through Python logging
        }
        
        # Database-specific configurations
        db_type = config.db_type.lower()
        
        if db_type == "sqlite":
            # SQLite specific configuration
            engine_config["connect_args"] = {
                "check_same_thread": False,  # Allow multi-threaded access
            }
        elif db_type == "mysql":
            # MySQL specific configuration
            engine_config["poolclass"] = pool.QueuePool
            engine_config["pool_size"] = 10
            engine_config["max_overflow"] = 20
            engine_config["pool_pre_ping"] = True
            engine_config["pool_recycle"] = 3600
            engine_config["connect_args"] = {
                "charset": "utf8mb4",
            }
        elif db_type == "oracle":
            # Oracle specific configuration
            engine_config["poolclass"] = pool.QueuePool
            engine_config["pool_size"] = 10
            engine_config["max_overflow"] = 20
            engine_config["pool_pre_ping"] = True
            engine_config["pool_recycle"] = 3600
            engine_config["connect_args"] = {
                "encoding": "UTF-8",
                "nencoding": "UTF-8",
            }
        
        logger.info(f"Creating database engine for {config.db_type}")
        engine = create_engine(connection_url, **engine_config)
        
        # Test connection
        try:
            with engine.connect():
                logger.info("Database connection successful")
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            raise
        
        return engine
    
    def get_connection(self):
        """
        Get a database connection from the pool
        
        Returns:
            SQLAlchemy Connection object
        """
        return self.get_engine().connect()
    
    def close(self):
        """Close database engine and cleanup connections"""
        if self._engine:
            self._engine.dispose()
            logger.info("Database engine disposed")
            self._engine = None


# Create singleton instance
db = DatabaseConnection()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db.get_engine())


def get_db_session():
    """
    Dependency function for FastAPI to get database session
    Use this in route dependencies
    
    Yields:
        Database session with automatic commit/rollback
    """
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    else:
        session.commit()
    finally:
        session.close()


def get_db_connection():
    """
    Legacy dependency function for database connection (deprecated)
    Use get_db_session() instead
    
    Yields:
        Database connection
    """
    connection = db.get_connection()
    try:
        yield connection
    finally:
        connection.close()


def init_db():
    """
    Initialize database - create all tables defined in ORM models
    Auto-discovers all models by importing the model package
    No need to manually register each model!
    
    WARNING: This only creates NEW tables. For schema changes, use Alembic migrations:
        alembic revision --autogenerate -m "description"
        alembic upgrade head
    """
    try:
        # Import model package to trigger model registration
        # This will automatically register all models that inherit from Base
        import model  # noqa: F401
        
        engine = db.get_engine()
        # Create tables from ORM Base.metadata (auto-discovered models)
        Base.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise


def get_database_url() -> str:
    """
    Get database connection URL for external tools (e.g., Alembic)
    
    Returns:
        SQLAlchemy connection URL string
    """
    return db._build_connection_url()
