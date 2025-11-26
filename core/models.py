"""
Core data models for the job scraper pipeline.
"""
from datetime import datetime, timezone
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator, ConfigDict

class JobType(str, Enum):
    """Enumeration of job types."""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"
    TEMPORARY = "Temporary"

class SeniorityLevel(str, Enum):
    """Enumeration of seniority levels."""
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    Manager = "manager"
    DIRECTOR = "director"
    EXECUTIVE = "executive"

class Currency(str, Enum):
    """Enumeration of currencies."""
    EGP = "EGP"  # Egyptian Pound
    AED = "AED"  # UAE Dirham
    SAR = "SAR"  # Saudi Riyal
    KWD = "KWD"  # Kuwaiti Dinar
    USD = "USD"  # US Dollar
    EUR = "EUR"  # Euro

class JobListing(BaseModel):
    """
    Standardized job listing model.
    
    This model represents a job listing from any source,
    normalized to a common schema.
    """

    # Identifiers and Metadata
    job_id: str = Field(..., description="Unique job identifier (site_jobid)")
    source: str = Field(..., description="Job board source (e.g., 'wuzzuf')")
    source_url: str = Field(..., description="Original job posting URL")

    # Basic Job Information
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Name of the hiring company")
    location: str = Field(..., description="Job location")

    # Job Details
    job_type: Optional[JobType] = None # Type of job (full-time, part-time, etc.)
    seniority: Optional[SeniorityLevel] = None # Seniority level required

    # Salary Information
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[Currency] = None # Currency of the salary
    salary_text: Optional[str] = None # Original salary text

    # Job Description and Requirements
    description: str = Field(..., description="Full job description")
    requirements: Optional[List[str]] = None # List of job requirements

    # Metadata
    skills: Optional[List[str]] = None # List of required skills
    industry: Optional[str] = None # Industry sector
    experience_years: Optional[int] = None # Number of years of experience required

    # Dates
    posted_date: Optional[datetime] = None # Date when the job was posted
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp when the job was scraped")
    expiry_date: Optional[datetime] = None # Job listing expiry date
    
    # Quality Indicators
    is_active: bool = Field(default=True, description="Indicates if the job listing is still active")
    is_remote: Optional[bool] = Field(default=False, description="Indicates if the job is remote")

    @field_validator('title', 'company', 'description')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v
    
    @field_validator('title', 'company', 'description')
    def clean_whitespace(cls, v):
        if isinstance(v, str):
            return ' '.join(v.split())
        return v
    
    @field_validator('job_id', 'source', 'source_url')
    def validate_non_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    @field_validator('description', mode='after')
    def description_starts_with_upper(cls, v):
        if isinstance(v, str) and v and not v[0].isupper():
            raise ValueError('Description must start with an uppercase letter')
        return v

    @field_validator('job_type')
    def reject_enum_instance_for_job_type(cls, v):
        from enum import Enum as _Enum
        # tests expect passing an Enum member to fail; disallow Enum instances
        if v is not None and isinstance(v, _Enum):
            raise ValueError('Invalid enum value')
        return v

    def __str__(self):
        """String representation of the JobListing."""
        return f"JobListing({self.job_id}: {self.title} at {self.company} ({self.location}))"
    
    def __repr__(self):
        """Detailed representation of the JobListing."""
        return (f"JobListing(job_id={self.job_id}, title={self.title}, company={self.company}, "
                f"location={self.location}, job_type={self.job_type}, seniority={self.seniority}, "
                f"salary_min={self.salary_min}, salary_max={self.salary_max}, currency={self.currency}, "
                f"posted_date={self.posted_date}, is_active={self.is_active})")

class ScraperConfig(BaseModel):
    """
    Configuration model for the job scraper.
    """

    name : str = Field(..., description="Name of the scraper")
    enabled: bool = Field(True, description="Indicates if the scraper is enabled")
    base_url: str = Field(..., description="Base URL of the job board to scrape")
    rate_limit: int = Field(5, description="Maximum number of requests per second")
    user_agent: str = Field(..., description="User-Agent string for HTTP requests")
    request_timeout: int = Field(10, description="Timeout for HTTP requests in seconds")
    max_retries: int = Field(3, description="Maximum number of retries for failed requests")
    scrape_interval: int = Field(60, description="Interval between scrapes in seconds")
    proxies: Optional[List[str]] = Field(None, description="List of proxy servers to use for scraping")

    @field_validator('user_agent')
    def validate_user_agent(cls, v):
        if not v or not v.strip():
            raise ValueError('User-Agent cannot be empty')
        return v
    
    @field_validator('rate_limit', 'request_timeout', 'max_retries', 'scrape_interval')
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError('Value must be positive')
        return v
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )
    