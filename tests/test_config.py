"""
Tests for configuration management.
"""
import pytest
from pathlib import Path

from core.config import (
    ConfigLoader, AppConfig, get_config_loader,
    get_site_config, get_rules, get_enabled_sites
)
from core.exceptions import ConfigurationError


class TestConfigLoader:
    """Tests for ConfigLoader class."""
    
    def test_load_sites_config(self):
        """Test loading sites configuration."""
        loader = get_config_loader()
        sites = loader.load_sites_config()
        
        assert isinstance(sites, dict)
        assert 'wuzzuf' in sites
        assert 'bayt' in sites
        assert len(sites) > 0
    
    def test_get_site_config(self):
        """Test getting configuration for a specific site."""
        loader = get_config_loader()
        wuzzuf_config = loader.get_site_config('wuzzuf')
        
        assert wuzzuf_config['enabled'] is True
        assert 'base_url' in wuzzuf_config
        assert 'rate_limit' in wuzzuf_config
        assert wuzzuf_config['base_url'] == "https://wuzzuf.net"
    
    def test_get_site_config_invalid_site(self):
        """Test that invalid site raises error."""
        loader = get_config_loader()
        
        with pytest.raises(ConfigurationError) as exc:
            loader.get_site_config('invalid_site')
        
        assert "not found" in str(exc.value)
    
    def test_load_salary_rules(self):
        """Test loading salary parsing rules."""
        loader = get_config_loader()
        rules = loader.load_rules('salary')
        
        assert 'currencies' in rules
        assert 'range_patterns' in rules
        assert 'EGP' in rules['currencies']
        assert 'AED' in rules['currencies']
    
    def test_load_seniority_rules(self):
        """Test loading seniority detection rules."""
        loader = get_config_loader()
        rules = loader.load_rules('seniority')
        
        assert 'levels' in rules
        assert 'junior' in rules['levels']
        assert 'senior' in rules['levels']
        assert 'detection_strategy' in rules
    
    def test_get_enabled_sites(self):
        """Test getting list of enabled sites."""
        loader = get_config_loader()
        enabled = loader.get_enabled_sites()
        
        assert isinstance(enabled, list)
        assert 'wuzzuf' in enabled
        assert len(enabled) > 0


class TestAppConfig:
    """Tests for AppConfig model."""
    
    def test_app_config_defaults(self):
        """Test AppConfig with default values."""
        config = AppConfig()
        
        assert config.environment == "development"
        assert config.debug is False
        assert config.log_level == "INFO"
        assert config.default_timeout == 30
        assert config.max_retries == 3
    
    def test_app_config_validation(self):
        """Test AppConfig validation."""
        # Invalid environment
        with pytest.raises(ValueError):
            AppConfig(environment="invalid")
        
        # Invalid log level
        with pytest.raises(ValueError):
            AppConfig(log_level="INVALID")
        
        # Invalid timeout range
        with pytest.raises(ValueError):
            AppConfig(default_timeout=200)  # Too high
    
    def test_app_config_custom_values(self):
        """Test AppConfig with custom values."""
        config = AppConfig(
            environment="production",
            debug=True,
            log_level="DEBUG",
            default_timeout=45
        )
        
        assert config.environment == "production"
        assert config.debug is True
        assert config.log_level == "DEBUG"
        assert config.default_timeout == 45


class TestConvenienceFunctions:
    """Tests for convenience functions."""
    
    def test_get_site_config_function(self):
        """Test get_site_config convenience function."""
        config = get_site_config('wuzzuf')
        assert config['base_url'] == "https://wuzzuf.net"
    
    def test_get_rules_function(self):
        """Test get_rules convenience function."""
        rules = get_rules('salary')
        assert 'currencies' in rules
    
    def test_get_enabled_sites_function(self):
        """Test get_enabled_sites convenience function."""
        sites = get_enabled_sites()
        assert isinstance(sites, list)
        assert len(sites) > 0