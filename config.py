import os

# Target URL
URL = "https://staging.squadhealth.ai/interview"

# File Paths
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
PDF_FILENAME = "interview_data.pdf" # Desired filename after download
PDF_PATH = os.path.join(DOWNLOAD_DIR, PDF_FILENAME)

# API Keys (Set these in your environment variables for security)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-key-here")