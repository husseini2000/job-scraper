"""
Unit tests for the models module.
"""
import pytest
from datetime import datetime, timezone, timedelta

from core.models import JobListing, JobType, SeniorityLevel, Currency
from pydantic import ValidationError

def test_job_listing_creation():
    """
    Test creating a valid job listing.
    """
    job = JobListing(
        job_id="wazzuf_12345",
        source="wuzzuf",
        source_url="https://wuzzuf.net/jobs/software-engineer-12345",
        title="Software Engineer",
        company="Tech Corp",
        location="Cairo, Egypt",
        description="An exciting role in a dynamic company.",
    )

    assert job.job_id == "wazzuf_12345"
    assert job.title == "Software Engineer"
    assert job.company == "Tech Corp"
    assert job.is_active is True
    assert isinstance(job.scraped_at, datetime)


def test_job_listing_with_salary():
    """Test job listing with salary information."""
    job = JobListing(
        job_id="bayt_67890",
        source="bayt",
        source_url="https://bayt.com/jobs/67890",
        title="Data Engineer",
        company="DataCo",
        location="Dubai, UAE",
        description="Work with big data",
        salary_min=15000,
        salary_max=20000,
        currency=Currency.AED
    )
    assert job.salary_min == 15000
    assert job.salary_max == 20000
    assert job.currency == Currency.AED

def test_job_listing_whitespace_cleaning():
    """
    Test that leading/trailing whitespace is cleaned from string fields.
    """
    job = JobListing(
        job_id="  wazzuf_12345  ",
        source="  wuzzuf  ",
        source_url="  https://wuzzuf.net/jobs/software-engineer-12345  ",
        title="  Software Engineer  ",
        company="  Tech Corp  ",
        location="Cairo, Egypt",
        description="  An exciting role in a dynamic company.  "
    )

    # Whitespace should be normalized
    assert job.job_id == "wazzuf_12345"
    assert job.source == "wuzzuf"
    assert job.description == "An exciting role in a dynamic company."


def test_job_listing_empty_fields():
    """ Test that empty required fields raise validation errors. """
    with pytest.raises(ValidationError) as exc_info:
        JobListing(
            job_id="",
            source="wuzzuf",
            source_url="https://wuzzuf.net/jobs/software-engineer-12345",
            title="",
            company="Tech Corp",
            location="Cairo, Egypt",
            description=""
        )
    
    errors = exc_info.value.errors()
    error_fields = {error['loc'][0] for error in errors}
    assert 'job_id' in error_fields
    assert 'title' in error_fields
    assert 'description' in error_fields


def test_job_listing_required_fields():
    """
    Test that missing required fields raise validation errors.
    """
    with pytest.raises(ValidationError) as exc_info:
        JobListing(
            job_id="wazzuf_12345",
            source="wuzzuf",
            source_url="https://wuzzuf.net/jobs/software-engineer-12345",
            title="Software Engineer",
            company="Tech Corp",
            location="Cairo, Egypt",
            description="an exciting role"
        )
    
    errors = exc_info.value.errors()
    assert any(error['loc'][0] == 'description' for error in errors)


def test_job_listing_enums():
    """
    Test that invalid enum values raise validation errors.
    """
    with pytest.raises(ValidationError) as exc_info:
        JobListing(
            job_id="wazzuf_12345",
            source="wuzzuf",
            source_url="https://wuzzuf.net/jobs/software-engineer-12345",
            title="Software Engineer",
            company="Tech Corp",
            location="Cairo, Egypt",
            description="An exciting role in a dynamic company.",
            job_type=JobType.FULL_TIME  # Invalid enum value
        )
    
    errors = exc_info.value.errors()
    assert any(error['loc'][0] == 'job_type' for error in errors)


def test_job_listing_string_representation():
    """Test __str__ and __repr__ methods."""
    job = JobListing(
        job_id="test_123",
        source="test",
        source_url="https://test.com",
        title="Python Dev",
        company="PyCompany",
        location="Cairo",
        description="Code Python",
    )
    
    str_repr = str(job)
    assert "test_123" in str_repr
    assert "Python Dev" in str_repr
    assert "PyCompany" in str_repr
    
    repr_str = repr(job)
    assert "JobListing" in repr_str
    assert "test_123" in repr_str