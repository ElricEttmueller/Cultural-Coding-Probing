"""Configuration management for Cultural Probes."""

import yaml
from pathlib import Path
from typing import Dict, Any

class ProbeConfig:
    """Manages configuration for the Cultural Probes framework."""
    
    def __init__(self, config_path: str = "probe_config.yaml"):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path).resolve()
        self.config = self._load_config()
        
        # Set up directory paths
        self.base_dir = self.config_path.parent
        self.response_dir = (self.base_dir / self.config['directories']['responses']).resolve()
        self.submission_dir = (self.base_dir / self.config['directories']['submissions']).resolve()
        self.template_dir = (self.base_dir / self.config['directories']['templates']).resolve()
        
        # Ensure directories exist
        self.response_dir.mkdir(exist_ok=True)
        self.submission_dir.mkdir(exist_ok=True)
        self.template_dir.mkdir(exist_ok=True)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_setting(self, *keys: str, default: Any = None) -> Any:
        """Get a configuration setting using dot notation.
        
        Args:
            *keys: Sequence of keys to traverse
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value or default
        """
        current = self.config
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    
    def get_email_template(self, **kwargs) -> str:
        """Get formatted email template with provided values.
        
        Args:
            **kwargs: Values to format into template
            
        Returns:
            Formatted email template
        """
        template = self.get_setting('email_template', default='')
        return template.format(**kwargs) if template else ''
    
    @property
    def receiver_email(self) -> str:
        """Get configured receiver email."""
        return self.get_setting('submission_settings', 'receiver_email', default='')
