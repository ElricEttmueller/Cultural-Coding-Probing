"""Configuration management for Cultural Probes."""

import functools
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from cachetools import TTLCache, cached
import os

class ProbeConfig:
    """Manages configuration for the Cultural Probes framework."""
    
    # Cache configuration for 5 minutes
    _config_cache = TTLCache(maxsize=100, ttl=300)
    
    def __init__(self, config_path: str = "probe_config.yaml"):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path).resolve()
        self._load_and_validate_config()
        
        # Set up directory paths
        self.base_dir = self.config_path.parent
        self._setup_directories()
    
    def _setup_directories(self) -> None:
        """Set up and validate directory structure."""
        directories = self.config['directories']
        
        # Create path attributes with validation
        for dir_name, dir_path in directories.items():
            full_path = (self.base_dir / dir_path).resolve()
            setattr(self, f"{dir_name}_dir", full_path)
            
            # Ensure directory exists and is writable
            full_path.mkdir(exist_ok=True)
            if not os.access(full_path, os.W_OK):
                raise PermissionError(f"Directory {full_path} is not writable")
    
    @cached(_config_cache)
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file with caching."""
        try:
            with open(self.config_path) as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise ConfigError(f"Failed to load config: {e}")
    
    def _load_and_validate_config(self) -> None:
        """Load and validate configuration."""
        self.config = self._load_config()
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate configuration structure."""
        required_sections = {'directories', 'security', 'submission'}
        missing = required_sections - set(self.config.keys())
        if missing:
            raise ConfigError(f"Missing required sections: {missing}")
    
    @property
    @functools.lru_cache()
    def security_settings(self) -> Dict[str, Any]:
        """Get security settings with caching."""
        return self.config.get('security', {})
    
    @property
    @functools.lru_cache()
    def submission_settings(self) -> Dict[str, Any]:
        """Get submission settings with caching."""
        return self.config.get('submission', {})
    
    def get_path(self, name: str) -> Optional[Path]:
        """Get a configured path by name."""
        dir_attr = f"{name}_dir"
        return getattr(self, dir_attr, None)
    
    def reload(self) -> None:
        """Reload configuration from disk."""
        self._config_cache.clear()
        self._load_and_validate_config()
        self._setup_directories()

class ConfigError(Exception):
    """Configuration related errors."""
    pass
