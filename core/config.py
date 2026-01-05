"""
This module provides a centralized, reliable, and scalable way to manage:
   - Environment variables
   - Application-level settings
   - Per-site scraping configurations
   - Parsing and scraping rules
   - Feature flags
   - Default behaviors (timeouts, retries, rate limits)
It ensures scraper behaves consistently,
can be configured without editing Python,
and is ready for production deployment.
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from functools import lru_cache

from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

from core.helpers import get_project_root
from core.exceptions import ConfigurationError

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


class AppConfig(BaseModel):
    """Application-wide configuration.
    
    This class controls the general behaviors of your pipeline.
    Examples:
        What environment are we running in? "development" / "production"
        Should Selenium be used?
        What is the default timeout for all scrapers?
        What is the rate limit?
    """
    
    # Environment
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    
    # Data directories
    data_dir: Path = Field(default_factory=lambda: get_project_root() / "data")
    
    # Database
    db_path: Optional[Path] = None
    
    # Scraping defaults
    default_timeout: int = Field(30, ge=5, le=120)
    default_rate_limit: int = Field(10, ge=1, le=100)
    max_retries: int = Field(3, ge=1, le=10)
    
    # Feature flags
    enable_selenium: bool = Field(default=False)
    enable_caching: bool = Field(default=True)
    
    @field_validator('environment')
    def validate_environment(cls, v):
        """Ensure valid environment."""
        valid_envs = ['development', 'staging', 'production']
        if v not in valid_envs:
            raise ValueError(f"environment must be one of {valid_envs}")
        return v
    
    @field_validator('log_level')
    def validate_log_level(cls, v):
        """Ensure valid log level."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v
    
    class Config:
        """Pydantic config."""
        env_prefix = 'JOB_SCRAPER_'  # Environment variables prefix


class ConfigLoader:
    """
    Centralized configuration loader.
    
    Loads and validates configuration from YAML files and environment variables.
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize configuration loader.
        
        Args:
            config_dir: Path to configuration directory
        """
        if config_dir is None:
            config_dir = get_project_root() / "configs"
        
        self.config_dir = Path(config_dir)
        
        if not self.config_dir.exists():
            logger.error(f"Configuration directory not found: {self.config_dir}")
            raise ConfigurationError(
                f"Configuration directory not found: {self.config_dir}"
            )
        
        logger.info(f"Initialized ConfigLoader with directory: {self.config_dir}")
        
        self._sites_config: Optional[Dict[str, Any]] = None
        self._rules_config: Dict[str, Any] = {}
        self._app_config: Optional[AppConfig] = None


    def load_sites_config(self) -> Dict[str, Any]:
        """
        Load sites configuration.
        
        Returns:
            Dictionary of site configurations
        """
        if self._sites_config is None:
            sites_file = self.config_dir / "sites.yml"
            logger.debug(f"Loading sites configuration from {sites_file}")
            self._sites_config = self._load_yaml(sites_file)
            logger.info(f"Loaded configuration for {len(self._sites_config)} sites")
        
        return self._sites_config
    
    def get_site_config(self, site_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific site.
        
        Args:
            site_name: Name of the site (e.g., 'wuzzuf')
        
        Returns:
            Site configuration dictionary
        
        Raises:
            ConfigurationError: If site not found
        """
        logger.debug(f"Requesting config for site: {site_name}")

        sites = self.load_sites_config()
        
        if site_name not in sites:
            available = ', '.join(sites.keys())

            logger.warning(
                f"Site '{site_name}' not found",
                extra={'requested_site': site_name, 'available_sites': list(sites.keys())}
            )
            raise ConfigurationError(
                f"Site '{site_name}' not found in configuration. "
                f"Available sites: {available}"
            )
        
        config = sites[site_name]
        
        # Check if site is enabled
        if not config.get('enabled', True):
            logger.info(f"Site '{site_name}' is disabled in configuration")
            raise ConfigurationError(f"Site '{site_name}' is disabled")
        logger.info(
            f"Loaded configuration for {site_name}",
            extra={'site': site_name, 'rate_limit': config.get('rate_limit')}
        )
        
        return config
    
    def load_rules(self, rule_name: str) -> Dict[str, Any]:
        """
        Load rules from rules directory.
        
        Args:
            rule_name: Name of rules file (without .yml extension)
        
        Returns:
            Rules dictionary
        """
        if rule_name not in self._rules_config:
            rules_file = self.config_dir / "rules" / f"{rule_name}.yml"
            
            if not rules_file.exists():
                raise ConfigurationError(
                    f"Rules file not found: {rules_file}"
                )
            
            self._rules_config[rule_name] = self._load_yaml(rules_file)
        
        return self._rules_config[rule_name]
    
    def load_app_config(self) -> AppConfig:
        """
        Load application configuration.
        
        Returns:
            AppConfig instance
        """
        if self._app_config is None:
            # Load from environment variables
            config_dict = {
                'environment': os.getenv('JOB_SCRAPER_ENVIRONMENT', 'development'),
                'debug': os.getenv('JOB_SCRAPER_DEBUG', 'false').lower() == 'true',
                'log_level': os.getenv('JOB_SCRAPER_LOG_LEVEL', 'INFO'),
                'enable_selenium': os.getenv('JOB_SCRAPER_ENABLE_SELENIUM', 'false').lower() == 'true',
            }
            
            self._app_config = AppConfig(**config_dict)
        
        return self._app_config
    
    def get_enabled_sites(self) -> list[str]:
        """
        Get list of enabled site names.
        
        Returns:
            List of enabled site names
        """
        sites = self.load_sites_config()
        return [
            name for name, config in sites.items()
            if config.get('enabled', True)
        ]
    
    def _load_yaml(self, filepath: Path) -> Dict[str, Any]:
        """
        Load YAML file.
        
        Args:
            filepath: Path to YAML file
        
        Returns:
            Parsed YAML content
        
        Raises:
            ConfigurationError: If file cannot be loaded
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
            
            if content is None:
                raise ConfigurationError(f"Empty configuration file: {filepath}")
            
            return content
        
        except yaml.YAMLError as e:
            raise ConfigurationError(
                f"Invalid YAML in {filepath}: {e}"
            )
        except Exception as e:
            raise ConfigurationError(
                f"Error loading configuration from {filepath}: {e}"
            )
    
    def reload(self):
        """Reload all configuration from files."""
        self._sites_config = None
        self._rules_config = {}
        self._app_config = None
    


# Singleton instance
@lru_cache(maxsize=1)
def get_config_loader() -> ConfigLoader:
    """
    Get singleton ConfigLoader instance.
    
    Returns:
        ConfigLoader instance
    """
    return ConfigLoader()


# Convenience functions
def get_site_config(site_name: str) -> Dict[str, Any]:
    """Get configuration for a site."""
    return get_config_loader().get_site_config(site_name)


def get_rules(rule_name: str) -> Dict[str, Any]:
    """Get rules configuration."""
    return get_config_loader().load_rules(rule_name)


def get_app_config() -> AppConfig:
    """Get application configuration."""
    return get_config_loader().load_app_config()


def get_enabled_sites() -> list[str]:
    """Get list of enabled sites."""
    return get_config_loader().get_enabled_sites()
    