"""
Logging Configuration Module
Centralized logging setup for the application
"""

import logging
import sys
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime


class SizeAndTimeRotatingFileHandler(TimedRotatingFileHandler):
    """
    Custom handler that rotates logs based on both time AND size.
    Extends TimedRotatingFileHandler to add size-based rotation.
    """
    
    def __init__(self, filename, when='midnight', interval=1, backupCount=0,
                 encoding=None, delay=False, utc=False, atTime=None,
                 maxBytes=0):
        """
        Initialize with both time-based and size-based rotation parameters.
        
        Args:
            maxBytes: Maximum file size in bytes before rotation
            All other args: Same as TimedRotatingFileHandler
        """
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime)
        self.maxBytes = maxBytes
    
    def shouldRollover(self, record):
        """
        Determine if rollover should occur.
        Returns True if either time-based OR size-based condition is met.
        """
        # Check time-based rollover first
        if super().shouldRollover(record):
            return True
        
        # Check size-based rollover
        if self.maxBytes > 0:
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)  # Go to end of file
            if self.stream.tell() + len(msg.encode('utf-8')) >= self.maxBytes:
                return True
        
        return False


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for terminal output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m',       # Reset
        'BOLD': '\033[1m',        # Bold
        'DIM': '\033[2m',         # Dim
    }
    
    def format(self, record):
        # Color the level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        # Format the message
        result = super().format(record)
        
        # Reset levelname to avoid affecting file logs
        record.levelname = levelname
        
        return result


class LogConfig:
    """Logging configuration handler"""
    
    # Log levels
    LOG_LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    
    # Default log format - Industry standard
    DEFAULT_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    DETAILED_FORMAT = "%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s"
    
    def __init__(
        self,
        log_level: str = "INFO",
        log_format: str = None,
        log_to_file: bool = True,
        log_dir: str = "logs",
        log_file: str = "app.log",
        rotation_type: str = "size",
        max_bytes: int = 10485760,  # 10MB
        backup_count: int = 5,
        rotation_when: str = "midnight",
        rotation_interval: int = 1,
        rotation_backup_count: int = 30,
        enable_console: bool = True,
    ):
        """
        Initialize logging configuration
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_format: Custom log format string
            log_to_file: Whether to log to file
            log_dir: Directory for log files
            log_file: Log file name
            rotation_type: "size" for size-based or "time" for time-based rotation
            max_bytes: Maximum size of log file before rotation (bytes) - for size-based
            backup_count: Number of backup files to keep - for size-based
            rotation_when: When to rotate - "S", "M", "H", "D", "midnight", "W0"-"W6" - for time-based
            rotation_interval: Rotation interval - for time-based
            rotation_backup_count: Number of backup files to keep - for time-based
            enable_console: Whether to log to console
        """
        self.log_level = self.LOG_LEVELS.get(log_level.upper(), logging.INFO)
        self.log_format = log_format or self.DEFAULT_FORMAT
        self.log_to_file = log_to_file
        self.log_dir = Path(log_dir)
        self.log_file = log_file
        self.rotation_type = rotation_type.lower()
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.rotation_when = rotation_when
        self.rotation_interval = rotation_interval
        self.rotation_backup_count = rotation_backup_count
        self.enable_console = enable_console
        
        # Create log directory if it doesn't exist
        if self.log_to_file:
            self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def setup(self):
        """Setup logging configuration"""
        # Get root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)
        
        # Remove existing handlers to avoid duplicates
        root_logger.handlers.clear()
        
        # Create colored formatter for console
        colored_formatter = ColoredFormatter(
            self.log_format,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Create plain formatter for file
        plain_formatter = logging.Formatter(
            self.log_format,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler with colors
        if self.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.log_level)
            console_handler.setFormatter(colored_formatter)
            root_logger.addHandler(console_handler)
        
        # File handler without colors
        if self.log_to_file:
            log_file_path = self.log_dir / self.log_file
            
            if self.rotation_type == "both":
                # Rotate by both time AND size
                file_handler = SizeAndTimeRotatingFileHandler(
                    log_file_path,
                    when=self.rotation_when,
                    interval=self.rotation_interval,
                    backupCount=self.rotation_backup_count,
                    maxBytes=self.max_bytes,
                    encoding='utf-8'
                )
            elif self.rotation_type == "time":
                # Time-based rotation only (daily, weekly, etc.)
                file_handler = TimedRotatingFileHandler(
                    log_file_path,
                    when=self.rotation_when,
                    interval=self.rotation_interval,
                    backupCount=self.rotation_backup_count,
                    encoding='utf-8'
                )
            else:
                # Size-based rotation only (default)
                file_handler = RotatingFileHandler(
                    log_file_path,
                    maxBytes=self.max_bytes,
                    backupCount=self.backup_count,
                    encoding='utf-8'
                )
            
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(plain_formatter)
            root_logger.addHandler(file_handler)
            
            # Add separate debug log file if log level is DEBUG
            if self.log_level == logging.DEBUG:
                debug_log_path = self.log_dir / "debug.log"
                
                if self.rotation_type == "both":
                    debug_handler = SizeAndTimeRotatingFileHandler(
                        debug_log_path,
                        when=self.rotation_when,
                        interval=self.rotation_interval,
                        backupCount=self.rotation_backup_count,
                        maxBytes=self.max_bytes,
                        encoding='utf-8'
                    )
                elif self.rotation_type == "time":
                    debug_handler = TimedRotatingFileHandler(
                        debug_log_path,
                        when=self.rotation_when,
                        interval=self.rotation_interval,
                        backupCount=self.rotation_backup_count,
                        encoding='utf-8'
                    )
                else:
                    debug_handler = RotatingFileHandler(
                        debug_log_path,
                        maxBytes=self.max_bytes,
                        backupCount=self.backup_count,
                        encoding='utf-8'
                    )
                
                # Only log DEBUG level messages to debug.log
                debug_handler.setLevel(logging.DEBUG)
                debug_handler.addFilter(lambda record: record.levelno == logging.DEBUG)
                debug_handler.setFormatter(plain_formatter)
                root_logger.addHandler(debug_handler)
        
        # Configure third-party loggers to use our format
        # Set appropriate log levels for noisy loggers
        # SQLAlchemy will show SQL queries when log_level is DEBUG
        sqlalchemy_level = logging.DEBUG if self.log_level == logging.DEBUG else logging.WARNING
        
        third_party_configs = {
            'sqlalchemy.engine': sqlalchemy_level,  # Shows SQL queries in DEBUG mode
            'sqlalchemy.pool': logging.WARNING,
            'sqlalchemy.dialects': logging.WARNING,
            'sqlalchemy.orm': logging.WARNING,
            'watchfiles': logging.WARNING,
            'asyncio': logging.WARNING,
            'uvicorn': logging.INFO,
            'uvicorn.error': logging.INFO,
            'uvicorn.access': logging.WARNING,
        }
        
        for logger_name, level in third_party_configs.items():
            third_party_logger = logging.getLogger(logger_name)
            third_party_logger.setLevel(level)
            # CRITICAL: Remove their handlers completely to prevent duplicate logs
            third_party_logger.handlers.clear()
            # Prevent them from creating new handlers
            third_party_logger.propagate = True
        
        # Special handling for SQLAlchemy to disable its internal logging config
        logging.getLogger('sqlalchemy').handlers.clear()
        logging.getLogger('sqlalchemy').propagate = True
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a logger instance
        
        Args:
            name: Logger name (typically __name__)
            
        Returns:
            Logger instance
        """
        return logging.getLogger(name)


def setup_logging(
    log_level: str = "INFO",
    detailed: bool = False,
    log_to_file: bool = True,
    log_dir: str = "logs",
    rotation_type: str = "size",
    max_bytes: int = 10485760,
    backup_count: int = 5,
    rotation_when: str = "midnight",
    rotation_interval: int = 1,
    rotation_backup_count: int = 30,
) -> None:
    """
    Quick setup function for logging
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        detailed: Use detailed log format with file and line number
        log_to_file: Whether to log to file
        log_dir: Directory for log files
        rotation_type: "size" for size-based or "time" for time-based rotation
        max_bytes: Maximum log file size before rotation (for size-based)
        backup_count: Number of backup files to keep (for size-based)
        rotation_when: When to rotate - "midnight", "D", "H", etc. (for time-based)
        rotation_interval: Rotation interval (for time-based)
        rotation_backup_count: Number of backup files to keep (for time-based)
    """
    log_format = LogConfig.DETAILED_FORMAT if detailed else LogConfig.DEFAULT_FORMAT
    
    log_config = LogConfig(
        log_level=log_level,
        log_format=log_format,
        log_to_file=log_to_file,
        log_dir=log_dir,
        rotation_type=rotation_type,
        max_bytes=max_bytes,
        backup_count=backup_count,
        rotation_when=rotation_when,
        rotation_interval=rotation_interval,
        rotation_backup_count=rotation_backup_count,
    )
    log_config.setup()


def setup_audit_logger(
    log_dir: str = "logs",
    rotation_type: str = "size",
    max_bytes: int = 10485760,
    backup_count: int = 5,
    rotation_when: str = "midnight",
    rotation_interval: int = 1,
    rotation_backup_count: int = 30,
) -> logging.Logger:
    """
    Setup a separate audit logger for request/response logging
    
    Args:
        log_dir: Directory for log files
        rotation_type: "size", "time", or "both" for rotation strategy
        max_bytes: Maximum log file size before rotation (for size-based)
        backup_count: Number of backup files to keep (for size-based)
        rotation_when: When to rotate - "midnight", "D", "H", etc. (for time-based)
        rotation_interval: Rotation interval (for time-based)
        rotation_backup_count: Number of backup files to keep (for time-based)
    
    Returns:
        Configured audit logger instance
    """
    audit_logger = logging.getLogger("audit")
    audit_logger.setLevel(logging.INFO)
    audit_logger.propagate = False  # Don't propagate to root logger
    
    # Clear any existing handlers
    audit_logger.handlers.clear()
    
    # Create log directory
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Audit log format
    audit_format = "%(asctime)s | %(message)s"
    formatter = logging.Formatter(audit_format, datefmt='%Y-%m-%d %H:%M:%S')
    
    # File handler for audit log
    audit_file = log_path / "audit.log"
    
    if rotation_type.lower() == "both":
        # Rotate by both time AND size
        file_handler = SizeAndTimeRotatingFileHandler(
            audit_file,
            when=rotation_when,
            interval=rotation_interval,
            backupCount=rotation_backup_count,
            maxBytes=max_bytes,
            encoding='utf-8'
        )
    elif rotation_type.lower() == "time":
        # Time-based rotation only
        file_handler = TimedRotatingFileHandler(
            audit_file,
            when=rotation_when,
            interval=rotation_interval,
            backupCount=rotation_backup_count,
            encoding='utf-8'
        )
    else:
        # Size-based rotation only (default)
        file_handler = RotatingFileHandler(
            audit_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
    
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    audit_logger.addHandler(file_handler)
    
    # Console handler for audit (optional, can be removed)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(ColoredFormatter(audit_format, datefmt='%Y-%m-%d %H:%M:%S'))
    audit_logger.addHandler(console_handler)
    
    return audit_logger


# Create a default logger instance
logger = logging.getLogger(__name__)
