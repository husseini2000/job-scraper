"""
Helper utilities used across the pipeline.
"""
import os
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict
from slugify import slugify
from pathvalidate import sanitize_filename


def get_project_root() -> Path:
    """Get the project root directory.

    Args:
        None
    Returns:
        Path to the project root
    """
    return Path(__file__).parent.parent


def get_data_dir(subdir: str = "") -> Path:
    """Get a data directory, creating it if needed.

    Args:
        subdir: Subdirectory within data directory
    Returns:
        Path to the data directory
    """
    data_dir = get_project_root() / "data" / subdir
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_timestamp() -> str:
    """Get current timestamp in ISO format.

    Args:
        None
    Returns:
        ISO formatted timestamp string
    """
    return datetime.now(timezone.utc).isoformat()


def get_date_string() -> str:
    """Get current date as string (YYYY-MM-DD).
    
    Args:
        None
    Returns:
        Date string in YYYY-MM-DD format
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def save_json(data: Any, filepath: Path) -> None:
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        filepath: Path to save to
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)


def load_json(filepath: Path) -> Any:
    """
    Load data from JSON file.
    
    Args:
        filepath: Path to load from
        
    Returns:
        Loaded data
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def ensure_dir(path: Path) -> Path:
    """
    Ensure a directory exists, creating it if needed.
    
    Args:
        path: Directory path
        
    Returns:
        The path (for chaining)
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def slugify_string(text: str) -> str:
    """
    Convert text to URL-safe slug.
    
    Args:
        text: Text to slugify
        
    Returns:
        Slugified text
    """
    
    # Make a slug from the given text.
    slug = slugify(text)
    
    return slug

def sanitized_filename(filename: str) -> str:
    """
    Sanitize a filename to be filesystem-safe.
    
    Args:
        filename: Original filename
    Returns:
        Sanitized filename
    """
    return sanitize_filename(filename)