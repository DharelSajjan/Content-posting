import os
from pathlib import Path

API_KEY = os.getenv("TW_API_KEY")
API_SECRET_KEY = os.getenv("TW_API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("TW_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TW_ACCESS_TOKEN_SECRET")

APP_PATH = Path(__file__).resolve().parent.parent
