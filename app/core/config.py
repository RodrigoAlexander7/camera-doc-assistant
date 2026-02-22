import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    LEGAL_COPILOT_API_URL = os.getenv(
        "LEGAL_COPILOT_API_URL",
        "https://law-copilot-backend-537825049720.us-central1.run.app/api/v1/query",
    )


settings = Settings()
