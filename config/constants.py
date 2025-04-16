# config/constants.py
"""
Constants used throughout the Medical AI Agent System.
"""

# Default model parameters
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = 1024

# Specialist types
SPECIALIST_CARDIOLOGIST = "cardiologist"
SPECIALIST_PSYCHOLOGIST = "psychologist"
SPECIALIST_PULMONOLOGIST = "pulmonologist"

# Default specialists to include
DEFAULT_SPECIALISTS = [
    SPECIALIST_CARDIOLOGIST,
    SPECIALIST_PSYCHOLOGIST, 
    SPECIALIST_PULMONOLOGIST
]

# File extensions
JSON_EXTENSION = ".json"
TXT_EXTENSION = ".txt"

# System messages
SYSTEM_MSG_MEDICAL = "You are a helpful medical assistant specializing in medical analysis and diagnosis."