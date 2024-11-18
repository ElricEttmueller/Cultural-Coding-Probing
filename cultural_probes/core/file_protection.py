"""File protection utilities for Cultural Probes."""

import os
import stat
from pathlib import Path
from typing import Union, List
import logging

logger = logging.getLogger(__name__)

class FileProtection:
    """Manages file protection and permissions."""
    
    @staticmethod
    def make_readonly(path: Union[str, Path]) -> bool:
        """Make a file or directory read-only.
        
        Args:
            path: Path to file or directory
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            path = Path(path)
            if not path.exists():
                logger.error(f"Path does not exist: {path}")
                return False
            
            # Remove write permissions for user, group, and others
            current_mode = path.stat().st_mode
            readonly_mode = current_mode & ~(
                stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
            )
            
            os.chmod(path, readonly_mode)
            logger.info(f"Made read-only: {path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to make read-only: {path}. Error: {str(e)}")
            return False
    
    @staticmethod
    def make_writable(path: Union[str, Path]) -> bool:
        """Make a file or directory writable.
        
        Args:
            path: Path to file or directory
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            path = Path(path)
            if not path.exists():
                logger.error(f"Path does not exist: {path}")
                return False
            
            # Add write permissions for user
            current_mode = path.stat().st_mode
            writable_mode = current_mode | stat.S_IWUSR
            
            os.chmod(path, writable_mode)
            logger.info(f"Made writable: {path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to make writable: {path}. Error: {str(e)}")
            return False
    
    @staticmethod
    def protect_directory(directory: Union[str, Path], exclude: List[str] = None) -> bool:
        """Recursively protect a directory and its contents.
        
        Args:
            directory: Directory to protect
            exclude: List of file/directory names to exclude
            
        Returns:
            bool: True if all operations successful, False otherwise
        """
        try:
            directory = Path(directory)
            exclude = exclude or []
            success = True
            
            if not directory.is_dir():
                logger.error(f"Not a directory: {directory}")
                return False
            
            # Process all files and subdirectories
            for item in directory.rglob('*'):
                if item.name in exclude:
                    logger.info(f"Skipping excluded item: {item}")
                    continue
                    
                if not FileProtection.make_readonly(item):
                    success = False
            
            # Protect the directory itself
            if not FileProtection.make_readonly(directory):
                success = False
                
            return success
            
        except Exception as e:
            logger.error(f"Failed to protect directory: {directory}. Error: {str(e)}")
            return False
    
    @staticmethod
    def unprotect_directory(directory: Union[str, Path]) -> bool:
        """Recursively unprotect a directory and its contents.
        
        Args:
            directory: Directory to unprotect
            
        Returns:
            bool: True if all operations successful, False otherwise
        """
        try:
            directory = Path(directory)
            success = True
            
            if not directory.is_dir():
                logger.error(f"Not a directory: {directory}")
                return False
            
            # First make the directory writable
            if not FileProtection.make_writable(directory):
                success = False
            
            # Then process all files and subdirectories
            for item in directory.rglob('*'):
                if not FileProtection.make_writable(item):
                    success = False
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to unprotect directory: {directory}. Error: {str(e)}")
            return False
