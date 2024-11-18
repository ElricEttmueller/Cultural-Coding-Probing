"""Utility functions for Cultural Probes."""

import hashlib
import platform
import datetime
from pathlib import Path
from typing import Dict, Any

def calculate_checksum(file_path: Path) -> str:
    """Calculate SHA-256 checksum of a file.
    
    Args:
        file_path: Path to file
        
    Returns:
        Hexadecimal checksum string
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_system_info() -> Dict[str, str]:
    """Collect system information.
    
    Returns:
        Dictionary of system information
    """
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "timestamp": datetime.datetime.now().isoformat()
    }

def generate_submission_id() -> str:
    """Generate a unique submission ID.
    
    Returns:
        Formatted timestamp-based ID
    """
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def clean_old_submissions(directory: Path, max_age_days: int = 30) -> None:
    """Clean up old submission files.
    
    Args:
        directory: Directory containing submissions
        max_age_days: Maximum age of files to keep
    """
    cutoff = datetime.datetime.now() - datetime.timedelta(days=max_age_days)
    
    for item in directory.glob("*"):
        if item.is_file() and item.stat().st_mtime < cutoff.timestamp():
            item.unlink()

def sanitize_filename(filename: str) -> str:
    """Sanitize a filename for safe filesystem usage.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # Ensure reasonable length
    max_length = 255
    if len(filename) > max_length:
        name, ext = os.path.splitext(filename)
        filename = name[:max_length-len(ext)] + ext
    
    return filename
