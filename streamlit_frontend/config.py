# config.py
import os

from dotenv import load_dotenv

load_dotenv()  # reads .env into os.environ

API_URL = os.getenv("API_URL", "http://localhost:8090/api")  # second argument = fallback
