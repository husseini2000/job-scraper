"""
Logging configuration for the job scraper pipeline.
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
from typing import Optional

from core.helpers import get_data_dir


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter to add colors to log levels for console output.
    """

    # ANSI escape codes for colors
    COLORS = {
        'DEBUG': '\033[94m',    # Blue
        'INFO': '\033[92m',     # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',    # Red
        'CRITICAL': '\033[95m'  # Magenta
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with colors based on the log level.
        """

        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
            )

        # Format the message
        result = super().format(record)    

        # Reset levelname for other handlers
        record.levelname = levelname

        return result
    

def setup_logging(
    log_level: str = "INFO",
    log_dir: Optional[Path] = None,
    enable_console: bool = True,
    enable_file: bool = True,
    enable_rotation: bool = True
) -> None:
    """
    Configure logging for the application.
    
    Args:
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files (default: data/logs)
        enable_console: Enable console output
        enable_file: Enable file output
        enable_rotation: Enable log rotation
    """
    # Get log directory
    if log_dir is None:
        log_dir = get_data_dir("logs")
    else:
        log_dir = Path(log_dir)
    
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Capture all, filter at handler level
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Convert log level string to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Console Handler (colored output)
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        
        console_formatter = ColoredFormatter(
            fmt='%(levelname)-8s | %(name)-25s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    
    # File Handler (detailed logs)
    if enable_file:
        # Main log file with all logs
        log_file = log_dir / f"pipeline_{datetime.now().strftime('%Y%m%d')}.log"
        
        if enable_rotation:
            # Rotate when file reaches 10MB, keep 5 backups
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5,
                encoding='utf-8'
            )
        else:
            file_handler = logging.FileHandler(
                log_file,
                encoding='utf-8'
            )
        
        file_handler.setLevel(logging.DEBUG)  # Log everything to file
        
        file_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)-30s | %(funcName)-20s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
        
        # Error log file (errors only)
        error_log_file = log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
        error_handler = RotatingFileHandler(
            error_log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        root_logger.addHandler(error_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        Logger instance
    
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing started")
    """
    return logging.getLogger(name)


class LoggerContext:
    """
    Context manager for temporary log level changes.
    
    Example:
        >>> with LoggerContext('extract.wuzzuf', 'DEBUG'):
        ...     scrape_wuzzuf()  # Will log DEBUG messages
    """
    
    def __init__(self, logger_name: str, level: str):
        """
        Initialize context manager.
        
        Args:
            logger_name: Name of logger to modify
            level: Temporary log level
        """
        self.logger = logging.getLogger(logger_name)
        self.original_level = self.logger.level
        self.new_level = getattr(logging, level.upper())
    
    def __enter__(self):
        """Enter context - set new level."""
        self.logger.setLevel(self.new_level)
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - restore original level."""
        self.logger.setLevel(self.original_level)


def log_function_call(func):
    """
    Decorator to log function calls.
    
    Example:
        >>> @log_function_call
        ... def scrape_jobs(site: str):
        ...     pass
    """
    logger = get_logger(func.__module__)
    
    def wrapper(*args, **kwargs):
        logger.debug(
            f"Calling {func.__name__}",
            extra={
                'function': func.__name__,
                'args': str(args)[:100],  # Truncate long args
                'kwargs': str(kwargs)[:100]
            }
        )
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Completed {func.__name__} successfully")
            return result
        except Exception as e:
            logger.error(
                f"Error in {func.__name__}: {e}",
                exc_info=True,
                extra={'function': func.__name__}
            )
            raise
    
    return wrapper


# Initialize logging on module import
def init_logging_from_env():
    """Initialize logging from environment variables."""
    import os
    
    log_level = os.getenv('JOB_SCRAPER_LOG_LEVEL', 'INFO')
    
    setup_logging(
        log_level=log_level,
        enable_console=True,
        enable_file=True,
        enable_rotation=True
    )


# Auto-initialize if not in test mode
if 'pytest' not in sys.modules:
    init_logging_from_env()