# utils/logger.py
import os
import logging
import sys
from logging.handlers import RotatingFileHandler

from config.settings import LOG_LEVEL, BASE_DIR

def setup_logger(name: str = None, level: str = None) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: Logger name (defaults to root logger if None)
        level: Log level (defaults to value from settings)
        
    Returns:
        Configured logger instance
    """
    # Default to root logger if no name provided
    logger = logging.getLogger(name)
    
    # Only configure if this logger hasn't been set up already
    if not logger.handlers:
        # Determine log level
        level = level or LOG_LEVEL
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        logger.setLevel(numeric_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler
        log_dir = os.path.join(BASE_DIR, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'medical_agents.log')
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger