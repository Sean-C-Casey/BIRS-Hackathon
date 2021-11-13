from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY", "")
API_HOST = "goverlytics.p.rapidapi.com"
API_BASE_URL = "https://goverlytics.p.rapidapi.com"

API_DIV_LEGISLATION = "/division-legislation"
API_DIV_LEGISLATORS = "/division-legislators"

API_FED_LEGISLATION = "/federal-legislation"
API_FED_LEGISLATORS = "/federal-legislators"