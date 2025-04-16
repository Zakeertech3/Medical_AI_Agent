# utils/file_handler.py
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Union, List

from config.settings import REPORTS_DIR, RESULTS_DIR

logger = logging.getLogger(__name__)

class FileHandler:
    """Utility for handling file operations for medical reports and results."""
    
    @staticmethod
    def load_report(filename: str) -> str:
        """
        Load a medical report from the reports directory.
        
        Args:
            filename: Name of the report file
            
        Returns:
            The content of the report
            
        Raises:
            FileNotFoundError: If the report file doesn't exist
        """
        file_path = os.path.join(REPORTS_DIR, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                logger.debug(f"Loaded report from {file_path}")
                return content
        except FileNotFoundError:
            logger.error(f"Report file not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading report {filename}: {str(e)}")
            raise
    
    @staticmethod
    def save_result(data: Union[str, Dict[str, Any]], 
                   filename: str = None, 
                   format_type: str = "txt") -> str:
        """
        Save analysis results to the results directory.
        
        Args:
            data: The content to save (string or dictionary)
            filename: Name for the result file (without extension)
            format_type: File format (txt or json)
            
        Returns:
            Path to the saved file
        """
        # Generate a filename if none was provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"result_{timestamp}"
        
        # Ensure filename has no extension
        filename = os.path.splitext(filename)[0]
        
        # Add the appropriate extension
        if format_type.lower() == "json":
            filename = f"{filename}.json"
        else:
            filename = f"{filename}.txt"
        
        file_path = os.path.join(RESULTS_DIR, filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                if format_type.lower() == "json" and isinstance(data, dict):
                    json.dump(data, file, indent=2)
                else:
                    if isinstance(data, dict):
                        # Convert dict to formatted string
                        content = json.dumps(data, indent=2)
                    else:
                        content = str(data)
                    file.write(content)
                
            logger.info(f"Saved result to {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error saving result {filename}: {str(e)}")
            raise
    
    @staticmethod
    def list_reports() -> List[str]:
        """
        List all available medical reports.
        
        Returns:
            List of report filenames
        """
        try:
            files = [f for f in os.listdir(REPORTS_DIR) if os.path.isfile(os.path.join(REPORTS_DIR, f))]
            return sorted(files)
        except Exception as e:
            logger.error(f"Error listing reports: {str(e)}")
            return []