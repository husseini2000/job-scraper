"""
Demonstration of logging functionality.
"""
import time
from extract.utils.logger import get_logger, LoggerContext, log_function_call

# Get logger for this module
logger = get_logger(__name__)


def demo_basic_logging():
    """Demonstrate basic logging at different levels."""
    print("\n" + "="*60)
    print("Demo 1: Basic Logging Levels")
    print("="*60 + "\n")
    
    logger.debug("This is a DEBUG message - detailed diagnostic info")
    logger.info("This is an INFO message - general information")
    logger.warning("This is a WARNING message - something unexpected")
    logger.error("This is an ERROR message - something failed")
    logger.critical("This is a CRITICAL message - system failure")
    
    print("\nNote: DEBUG messages may not appear if log level is INFO or higher")


def demo_structured_logging():
    """Demonstrate structured logging with extra fields."""
    print("\n" + "="*60)
    print("Demo 2: Structured Logging")
    print("="*60 + "\n")
    
    # Log with structured data
    logger.info(
        "Starting job scraper",
        extra={
            'scraper': 'wuzzuf',
            'max_pages': 50,
            'location': 'Cairo'
        }
    )
    
    # Simulate scraping
    for page in range(1, 4):
        jobs_found = page * 10
        logger.info(
            f"Scraped page {page}",
            extra={
                'page': page,
                'jobs_found': jobs_found,
                'scraper': 'wuzzuf'
            }
        )
        time.sleep(0.1)
    
    logger.info(
        "Scraping completed",
        extra={
            'scraper': 'wuzzuf',
            'total_jobs': 30,
            'duration_seconds': 0.3
        }
    )


def demo_error_logging():
    """Demonstrate error logging with exception info."""
    print("\n" + "="*60)
    print("Demo 3: Error Logging with Stack Traces")
    print("="*60 + "\n")
    
    try:
        # Simulate an error
        result = 10 / 0
    except ZeroDivisionError as e:
        logger.error(
            "Division by zero error occurred",
            exc_info=True,  # Include full stack trace
            extra={
                'operation': 'division',
                'error_type': type(e).__name__
            }
        )
    
    try:
        # Another error
        data = {'name': 'John'}
        age = data['age']  # KeyError
    except KeyError as e:
        logger.error(
            f"Missing required field: {e}",
            exc_info=True,
            extra={
                'operation': 'data_access',
                'missing_field': str(e)
            }
        )


@log_function_call
def demo_function_decorator(site: str, max_pages: int):
    """Demonstrate function call logging with decorator."""
    print("\n" + "="*60)
    print("Demo 4: Function Call Logging")
    print("="*60 + "\n")
    
    logger.info(f"Processing {site} with {max_pages} pages")
    time.sleep(0.1)
    return f"Completed {site}"


def demo_context_manager():
    """Demonstrate temporary log level changes."""
    print("\n" + "="*60)
    print("Demo 5: Context Manager for Log Levels")
    print("="*60 + "\n")
    
    logger.info("Normal INFO message - visible")
    logger.debug("Normal DEBUG message - may not be visible")
    
    # Temporarily enable DEBUG logging for this section
    with LoggerContext('__main__', 'DEBUG'):
        logger.debug("DEBUG message inside context - now visible!")
        logger.info("INFO message inside context")
    
    logger.debug("DEBUG message after context - not visible again")


def demo_performance_logging():
    """Demonstrate performance logging."""
    print("\n" + "="*60)
    print("Demo 6: Performance Logging")
    print("="*60 + "\n")
    
    start_time = time.time()
    
    logger.info("Starting data processing")
    
    # Simulate work
    for i in range(5):
        step_start = time.time()
        time.sleep(0.05)
        step_duration = time.time() - step_start
        
        logger.debug(
            f"Processed batch {i+1}",
            extra={
                'batch': i+1,
                'duration_ms': round(step_duration * 1000, 2)
            }
        )
    
    total_duration = time.time() - start_time
    logger.info(
        "Processing completed",
        extra={
            'total_batches': 5,
            'total_duration_seconds': round(total_duration, 2),
            'avg_batch_time_ms': round((total_duration / 5) * 1000, 2)
        }
    )


def demo_hierarchical_loggers():
    """Demonstrate hierarchical logger naming."""
    print("\n" + "="*60)
    print("Demo 7: Hierarchical Loggers")
    print("="*60 + "\n")
    
    # Create loggers with hierarchy
    extract_logger = get_logger('extract')
    wuzzuf_logger = get_logger('extract.wuzzuf')
    transform_logger = get_logger('transform')
    
    extract_logger.info("Extract phase starting")
    wuzzuf_logger.info("Wuzzuf scraper initialized")
    wuzzuf_logger.debug("Fetching page 1")
    transform_logger.info("Transform phase starting")
    
    print("\nNotice: Logger names show module hierarchy")


def demo_conditional_logging():
    """Demonstrate conditional and lazy logging."""
    print("\n" + "="*60)
    print("Demo 8: Conditional Logging")
    print("="*60 + "\n")
    
    jobs = ['Job 1', 'Job 2', 'Job 3']
    
    # Check if DEBUG is enabled before expensive operations
    if logger.isEnabledFor(logging.DEBUG):
        # This expensive operation only runs if DEBUG is enabled
        detailed_info = '\n'.join([f"  - {job}" for job in jobs])
        logger.debug(f"Jobs found:\n{detailed_info}")
    
    logger.info(f"Found {len(jobs)} jobs")


def run_all_demos():
    """Run all logging demonstrations."""
    print("\n" + "█"*60)
    print("  JOB SCRAPER PIPELINE - LOGGING DEMONSTRATION")
    print("█"*60)
    
    demo_basic_logging()
    demo_structured_logging()
    demo_error_logging()
    demo_function_decorator('wuzzuf', 50)
    demo_context_manager()
    demo_performance_logging()
    demo_hierarchical_loggers()
    demo_conditional_logging()
    
    print("\n" + "="*60)
    print("All demos completed!")
    print("="*60)
    print("\nCheck the log files in data/logs/ for detailed output")
    print("  - pipeline_YYYYMMDD.log: All logs")
    print("  - errors_YYYYMMDD.log: Errors only")


if __name__ == "__main__":
    # Import here to ensure logging is set up
    import logging
    
    run_all_demos()