"""
Tests for logging functionality.
"""
import logging
import tempfile
from pathlib import Path

import pytest

from extract.utils.logger import (
    setup_logging, get_logger, LoggerContext, log_function_call
)


@pytest.fixture
def temp_log_dir():
    """Create temporary directory for logs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestLoggingSetup:
    """Tests for logging setup."""
    
    def test_setup_logging_creates_handlers(self, temp_log_dir):
        """Test that setup_logging creates console and file handlers."""
        setup_logging(
            log_level='INFO',
            log_dir=temp_log_dir,
            enable_console=True,
            enable_file=True
        )
        
        root_logger = logging.getLogger()
        
        # Should have handlers
        assert len(root_logger.handlers) > 0
        
        # Check for file handler
        file_handlers = [
            h for h in root_logger.handlers
            if isinstance(h, logging.FileHandler)
        ]
        assert len(file_handlers) > 0
    
    def test_log_files_created(self, temp_log_dir):
        """Test that log files are created."""
        setup_logging(log_dir=temp_log_dir)
        
        logger = get_logger(__name__)
        logger.info("Test message")
        
        # Check log files exist
        log_files = list(temp_log_dir.glob("*.log"))
        assert len(log_files) >= 1
    
    def test_error_log_file_created(self, temp_log_dir):
        """Test that error log file is created."""
        setup_logging(log_dir=temp_log_dir)
        
        logger = get_logger(__name__)
        logger.error("Test error message")
        
        # Check error log file exists
        error_logs = list(temp_log_dir.glob("errors_*.log"))
        assert len(error_logs) == 1
    
    def test_log_level_filtering(self, temp_log_dir, caplog):
        """Test that log level filtering works."""
        setup_logging(log_level='WARNING', log_dir=temp_log_dir)
        
        logger = get_logger(__name__)
        
        with caplog.at_level(logging.WARNING):
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
        
        # Only WARNING should appear in console
        messages = [record.message for record in caplog.records]
        assert "Warning message" in messages
        # DEBUG and INFO shouldn't appear (if console level is WARNING)


class TestGetLogger:
    """Tests for get_logger function."""
    
    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a Logger instance."""
        logger = get_logger(__name__)
        assert isinstance(logger, logging.Logger)
    
    def test_get_logger_with_name(self):
        """Test that logger has correct name."""
        logger = get_logger('test.module')
        assert logger.name == 'test.module'
    
    def test_multiple_calls_same_logger(self):
        """Test that multiple calls return same logger instance."""
        logger1 = get_logger('test.module')
        logger2 = get_logger('test.module')
        assert logger1 is logger2


class TestLoggerContext:
    """Tests for LoggerContext manager."""
    
    def test_context_changes_level(self):
        """Test that context manager changes log level."""
        logger = get_logger('test.context')
        original_level = logger.level
        
        with LoggerContext('test.context', 'DEBUG'):
            assert logger.level == logging.DEBUG
        
        # Should restore original level
        assert logger.level == original_level
    
    def test_context_restores_on_exception(self):
        """Test that level is restored even if exception occurs."""
        logger = get_logger('test.context')
        original_level = logger.level
        
        try:
            with LoggerContext('test.context', 'DEBUG'):
                raise ValueError("Test error")
        except ValueError:
            pass
        
        # Should still restore original level
        assert logger.level == original_level


class TestLogFunctionCall:
    """Tests for log_function_call decorator."""
    
    def test_decorator_logs_function_call(self, caplog):
        """Test that decorator logs function calls."""
        
        @log_function_call
        def test_function(x, y):
            return x + y
        
        with caplog.at_level(logging.DEBUG):
            result = test_function(1, 2)
        
        assert result == 3
        
        # Check that function call was logged
        messages = [record.message for record in caplog.records]
        assert any("Calling test_function" in msg for msg in messages)
    
    def test_decorator_logs_errors(self, caplog):
        """Test that decorator logs errors."""
        
        @log_function_call
        def failing_function():
            raise ValueError("Test error")
        
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                failing_function()
        
        # Check that error was logged
        messages = [record.message for record in caplog.records]
        assert any("Error in failing_function" in msg for msg in messages)


class TestStructuredLogging:
    """Tests for structured logging with extra fields."""
    
    def test_extra_fields_captured(self, caplog):
        """Test that extra fields are captured in log records."""
        logger = get_logger(__name__)
        
        with caplog.at_level(logging.INFO):
            logger.info(
                "Test message",
                extra={
                    'scraper': 'wuzzuf',
                    'job_count': 100
                }
            )
        
        record = caplog.records[0]
        assert hasattr(record, 'scraper')
        assert record.scraper == 'wuzzuf'
        assert record.job_count == 100


class TestLogRotation:
    """Tests for log rotation."""
    
    def test_rotating_handler_configured(self, temp_log_dir):
        """Test that rotating file handler is configured."""
        from logging.handlers import RotatingFileHandler
        
        setup_logging(
            log_dir=temp_log_dir,
            enable_rotation=True
        )
        
        root_logger = logging.getLogger()
        rotating_handlers = [
            h for h in root_logger.handlers
            if isinstance(h, RotatingFileHandler)
        ]
        
        assert len(rotating_handlers) > 0
        
        # Check max bytes configured
        handler = rotating_handlers[0]
        assert handler.maxBytes == 10 * 1024 * 1024  # 10 MB