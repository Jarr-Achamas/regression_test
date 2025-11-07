import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

ADMIN_URL = "https://pre.bonp.me/member/"
WAITING_TIMEOUT_MS = 15000 # 15 seconds

# Dictionary to hold version-specific bot names
BOT_NAMES = {
    "1.0": {"name": "Jarr_regression_2509_API1"},
    "2.0": {"name": "Jarr_regression_2509_API2"}
}