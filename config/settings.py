# config/settings.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")

# Application settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MAX_WORKERS = int(os.getenv("MAX_WORKERS", 3))

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(DATA_DIR, "sample_reports")
RESULTS_DIR = os.path.join(DATA_DIR, "results")

# Ensure directories exist
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)