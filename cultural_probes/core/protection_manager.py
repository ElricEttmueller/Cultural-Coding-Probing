"""Protection manager for Cultural Probes."""

import fnmatch
from pathlib import Path
from typing import List, Union
import logging

from .config import ProbeConfig
from .file_protection import FileProtection

logger = logging.getLogger(__name__)

class ProtectionManager:
    """Manages file and directory protection based on configuration."""
    
    def __init__(self, config: ProbeConfig):
        """Initialize protection manager.
        
        Args:
            config: ProbeConfig instance
        """
        self.config = config
        self.protection = FileProtection()
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if a path should be excluded from protection.
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if path should be excluded
        """
        exclude_patterns = self.config.get_setting(
            'security', 'file_protection', 'exclude_from_protection',
            default=[]
        )
        
        return any(
            fnmatch.fnmatch(path.name, pattern)
            for pattern in exclude_patterns
        )
    
    def protect_configured_paths(self) -> bool:
        """Protect all paths specified in configuration.
        
        Returns:
            bool: True if all operations successful
        """
        if not self.config.get_setting('security', 'file_protection', 'enabled', default=False):
            logger.info("File protection is disabled in configuration")
            return True
        
        success = True
        protected_paths = self.config.get_setting(
            'security', 'file_protection', 'protected_paths',
            default=[]
        )
        
        for path in protected_paths:
            full_path = self.config.base_dir / path
            if not full_path.exists():
                logger.warning(f"Protected path does not exist: {full_path}")
                continue
            
            exclude = self.config.get_setting(
                'security', 'file_protection', 'exclude_from_protection',
                default=[]
            )
            
            if not self.protection.protect_directory(full_path, exclude):
                success = False
                logger.error(f"Failed to protect path: {full_path}")
        
        return success
    
    def unprotect_path(self, path: Union[str, Path]) -> bool:
        """Unprotect a specific path.
        
        Args:
            path: Path to unprotect
            
        Returns:
            bool: True if successful
        """
        path = Path(path)
        if not path.exists():
            logger.error(f"Path does not exist: {path}")
            return False
        
        if path.is_dir():
            return self.protection.unprotect_directory(path)
        else:
            return self.protection.make_writable(path)
    
    def temporarily_unprotect(self, path: Union[str, Path]):
        """Context manager for temporarily unprotecting a path.
        
        Args:
            path: Path to temporarily unprotect
            
        Usage:
            with protection_manager.temporarily_unprotect(path):
                # Modify files here
        """
        class TemporaryUnprotection:
            def __init__(self, manager, target_path):
                self.manager = manager
                self.path = Path(target_path)
                
            def __enter__(self):
                success = self.manager.unprotect_path(self.path)
                if not success:
                    raise RuntimeError(f"Failed to unprotect path: {self.path}")
                return self.path
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                if self.path.is_dir():
                    self.manager.protection.protect_directory(
                        self.path,
                        self.manager.config.get_setting(
                            'security', 'file_protection', 'exclude_from_protection',
                            default=[]
                        )
                    )
                else:
                    self.manager.protection.make_readonly(self.path)
        
        return TemporaryUnprotection(self, path)
