"""
Core data models for the job scraper pipeline.
"""
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict, HttpUrl

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


class SalaryInfo(BaseModel):
    """Salary information model."""

    min_amount: Optional[float] = Field(None, ge=0, description="Minimum salary amount")
    max_amount: Optional[float] = Field(None, ge=0, description="Maximum salary amount")
    currency: Optional[Currency] = None # Currency of the salary
    period: Optional[str] = None # e.g., 'per month', 'per year'
    is_negotiable: bool = False # Indicates if the salary is negotiable
    original_text: Optional[str] = None # Original salary text from the listing

    @model_validator(mode='after')
    def validate_salary_range(self) -> "SalaryInfo":
        if (self.min_amount is not None and self.max_amount is not None and
            self.min_amount > self.max_amount):
            raise ValueError('min_amount cannot be greater than max_amount')
        return self
    
    def __str__(self) -> str:
        """String representation of the SalaryInfo."""
        if self.min_amount and self.max_amount:
            return f"{self.min_amount} - {self.max_amount} {self.currency or ''} ({self.period})"
        elif self.min_amount:
            return f"From {self.min_amount} {self.currency or ''} ({self.period})"
        elif self.original_text:
            return self.original_text
        else:
            return "Salary not specified"


class ExperienceRequirement(BaseModel):
    """Experience requirements model."""
    
    min_years: Optional[int] = Field(None, ge=0, le=50)
    max_years: Optional[int] = Field(None, ge=0, le=50)
    original_text: Optional[str] = None # Original experience text from the listing
    
    @model_validator(mode='after')
    def validate_experience_range(self) -> "ExperienceRequirement":
        """Ensure min <= max if both present."""
        min_years = self.min_years
        max_years = self.max_years
        if (min_years is not None and max_years is not None and
            min_years > max_years):
            raise ValueError('min_years cannot be greater than max_years')
        return self

    
    def __str__(self) -> str:
        """Human-readable experience string."""
        if self.min_years is not None and self.max_years is not None:
            return f"{self.min_years}-{self.max_years} years"
        elif self.min_years is not None:
            return f"{self.min_years}+ years"
        elif self.original_text:
            return self.original_text
        return "Not specified"


class Company(BaseModel):
    """Company information model."""
    
    name: str = Field(..., min_length=1, max_length=200)
    industry: Optional[str] = Field(None, max_length=100)
    size: Optional[str] = None # e.g., '50-100 employees'
    location: Optional[str] = None
    website: Optional[HttpUrl] = None
    
    @field_validator('name')
    def clean_company_name(cls, v):
        """Clean company name."""
        return ' '.join(v.split()).strip()
    
    def __str__(self):
        return self.name
    

class JobListing(BaseModel):
    """
    Standardized job listing model.
    
    This model represents a job listing from any source,
    normalized to a common schema.
    """

    # Identifiers and Metadata
    job_id: str = Field(..., description="Unique job identifier (site_jobid)")
    source: str = Field(..., description="Job board source (e.g., 'wuzzuf')")
    source_url: HttpUrl = Field(..., description="Original job posting URL")

    # Basic Job Information
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Name of the hiring company")

    # Job Details
    job_type: Optional[JobType] = None # Type of job (full-time, part-time, etc.)
    seniority: Optional[SeniorityLevel] = None # Seniority level required
    work_arrangement: Optional[str] = Field(
        None, 
        description="Remote, Hybrid, On-site"
    )

    # Salary Information
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary: Optional[SalaryInfo] = None
    currency: Optional[Currency] = None # Currency of the salary

    # Job Description and Requirements
    description: str = Field(..., description="Full job description")
    requirements: Optional[List[str]] = None # List of job requirements

    # Metadata
    skills: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    experience: Optional[ExperienceRequirement] = None # Number of years of experience required

    # Dates
    posted_date: Optional[datetime] = None # Date when the job was posted
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp when the job was scraped")
    expiry_date: Optional[datetime] = None # Job listing expiry date
    
    # Quality Indicators
    is_active: bool = Field(default=True, description="Indicates if the job listing is still active")
    is_remote: Optional[bool] = Field(default=False, description="Indicates if the job is remote")
    has_salary_info: bool = False # Indicates if salary info is provided

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
        s = str(v) if v is not None else ''
        if not s or not s.strip():
            raise ValueError('Field cannot be empty')
        return v
    
    @field_validator('job_id')
    def validate_job_id(cls, v):
        if not v or  not v.strip() or ' ' in v:
            raise ValueError('job_id cannot be empty or contain spaces')
        
        v = v.strip()
        if '-' in v:
            raise ValueError("job_id must not contain '-'")
        return v
    
    @field_validator('skills', 'languages')
    def clean_list_items(cls, v):
        if v is None:
            return []
        # Clean each item, remove duplicates, filter empty
        cleaned = [item.strip() for item in v if item and item.strip()]
        return list(dict.fromkeys(cleaned))  # Preserve order, remove dupes
    
    @field_validator('description', mode='after')
    def description_starts_with_upper(cls, v):
        if isinstance(v, str) and v and not v[0].isupper():
            raise ValueError('Description must start with an uppercase letter')
        return v
    

    @field_validator('job_type', mode='before')
    def reject_enum_instance_for_job_type(cls, v):
        from enum import Enum as _Enum
        # tests expect passing an Enum member to fail; disallow Enum instances
        if v is not None and isinstance(v, _Enum):
            raise ValueError('Invalid enum value')
        return v
    
    @model_validator(mode='after')
    def set_computed_flags(self) -> "JobListing":
        """Set computed flags based on available data."""
        # if legacy flat salary fields are provided, populate SalaryInfo
        if self.salary is None and (self.salary_min is not None or self.salary_max is not None):
            self.salary = SalaryInfo(min_amount=self.salary_min, max_amount=self.salary_max, currency=self.currency)

        self.has_salary_info = bool(
            self.salary and 
            (self.salary.min_amount is not None or self.salary.max_amount is not None)
        )

        self.is_remote = (self.work_arrangement is not None and 
                          self.work_arrangement.lower() == 'remote')

        return self

    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        use_enum_values=True,
    )


    def __str__(self):
        """String representation of the JobListing."""
        return f"JobListing({self.job_id}: {self.title} at {self.company})"
    
    def __repr__(self):
        """Detailed representation of the JobListing."""
        return (f"JobListing(job_id={self.job_id}, title={self.title},\
            company={self.company}, source={self.source})")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert JobListing to a dictionary."""
        return self.model_dump()

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
    requires_auth: bool = False # Indicates if authentication is required
    auth_credentials: Optional[Dict[str, str]] = None # e.g., {'username': 'user', 'password': 'pass'}

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
        use_enum_values=True
    )
    
    def __str__(self):
        """String representation of the ScraperConfig."""
        return f"ScraperConfig({self.name}, enabled={self.enabled}, base_url={self.base_url})"
    
class PipelineRun(BaseModel):
    """Model for tracking pipeline execution."""
    
    run_id: str
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    status: str = Field("running", pattern="^(running|success|failed|partial)$")
    
    # Statistics
    scrapers_run: List[str] = Field(default_factory=list)
    jobs_extracted: int = 0
    jobs_transformed: int = 0
    jobs_loaded: int = 0
    errors_count: int = 0
    
    # Details
    errors: List[str] = Field(default_factory=list, max_length=1000)
    warnings: List[str] = Field(default_factory=list, max_length=1000)
    
    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate run duration in seconds."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.jobs_extracted == 0:
            return 0.0
        return (self.jobs_loaded / self.jobs_extracted) * 100
    
    def __str__(self):
        return f"PipelineRun({self.run_id}, status={self.status})"
