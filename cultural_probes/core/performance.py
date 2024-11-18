"""Performance monitoring utilities for Cultural Probes."""

import time
import functools
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Optional, TypeVar

# Type variables for generic function decorators
F = TypeVar('F', bound=Callable[..., Any])

@dataclass
class PerformanceMetrics:
    """Container for performance metrics."""
    execution_time: float
    memory_usage: float
    function_name: str
    timestamp: float
    success: bool
    error: Optional[str] = None

class PerformanceMonitor:
    """Performance monitoring and logging utility."""
    
    def __init__(self, log_dir: Path):
        """Initialize performance monitor.
        
        Args:
            log_dir: Directory for log files
        """
        self.log_dir = log_dir
        self.log_dir.mkdir(exist_ok=True)
        
        # Set up logging
        self.logger = logging.getLogger('performance')
        self.logger.setLevel(logging.INFO)
        
        # Use thread-safe rotating handler
        handler = ConcurrentRotatingFileHandler(
            filename=str(log_dir / 'performance.log'),
            maxBytes=1024 * 1024,  # 1MB
            backupCount=5
        )
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def measure(self, func: F) -> F:
        """Decorator to measure function performance.
        
        Args:
            func: Function to measure
            
        Returns:
            Wrapped function with performance monitoring
        """
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            start_memory = self._get_memory_usage()
            
            try:
                result = func(*args, **kwargs)
                success = True
                error = None
            except Exception as e:
                success = False
                error = str(e)
                raise
            finally:
                end_time = time.time()
                end_memory = self._get_memory_usage()
                
                metrics = PerformanceMetrics(
                    execution_time=end_time - start_time,
                    memory_usage=end_memory - start_memory,
                    function_name=func.__name__,
                    timestamp=end_time,
                    success=success,
                    error=error
                )
                
                self._log_metrics(metrics)
            
            return result
        return wrapper  # type: ignore
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage."""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # MB
        except ImportError:
            return 0.0
    
    def _log_metrics(self, metrics: PerformanceMetrics) -> None:
        """Log performance metrics."""
        message = (
            f"Function: {metrics.function_name} | "
            f"Time: {metrics.execution_time:.3f}s | "
            f"Memory: {metrics.memory_usage:.2f}MB | "
            f"Success: {metrics.success}"
        )
        
        if metrics.error:
            message += f" | Error: {metrics.error}"
        
        if metrics.execution_time > 1.0:  # Slow execution warning
            self.logger.warning(f"Slow execution detected: {message}")
        else:
            self.logger.info(message)

# Global performance monitor instance
monitor = PerformanceMonitor(Path("logs"))

def measure_performance(func: F) -> F:
    """Convenience decorator for performance monitoring."""
    return monitor.measure(func)
