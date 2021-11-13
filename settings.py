from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY", "")
API_HOST = "goverlytics.p.rapidapi.com"
API_BASE_URL = "https://goverlytics.p.rapidapi.com/division-legislation/ca/bc"