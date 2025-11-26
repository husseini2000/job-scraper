"""
Custom exceptions for the job scraper pipeline.
"""

class JobScraperError(Exception):
    """Base exception for all job scraper errors."""
    pass

class JobNotFoundError(JobScraperError):
    """Exception raised when a job listing is not found."""
    def __init__(self, job_id: str):
        self.job_id = job_id
        super().__init__(f"Job listing with ID '{job_id}' not found.")

class ScraperError(JobScraperError):
    """Exception raised for errors during the scraping process."""
    def __init__(self, message: str):
        super().__init__(f"Scraper error: {message}")

class ParsingError(JobScraperError):
    """Exception raised for errors during parsing of job data."""
    def __init__(self, message: str):
        super().__init__(f"Parsing error: {message}")

class ValidationError(JobScraperError):
    """Exception raised for data validation errors."""
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"Data validation error on field '{field}': {message}")

class NetworkError(JobScraperError):
    """Exception raised for network-related errors."""
    def __init__(self, message: str):
        super().__init__(f"Network error: {message}")

class RateLimitError(JobScraperError):
    """Exception raised when rate limits are exceeded."""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after {retry_after} seconds.")

class ConfigurationError(JobScraperError):
    """Exception raised for configuration-related errors."""
    def __init__(self, message: str):
        super().__init__(f"Configuration error: {message}")

class TransformError(JobScraperError):
    """Exception raised for errors during data transformation."""
    def __init__(self, message: str):
        super().__init__(f"Transformation error: {message}")

class LoadError(JobScraperError):
    """Exception raised for errors during data loading."""
    def __init__(self, message: str):
        super().__init__(f"Load error: {message}")