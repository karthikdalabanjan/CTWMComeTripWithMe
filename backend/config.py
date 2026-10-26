import os
from typing import List

class Settings:
    PROJECT_NAME: str = "ComeTripWithMe Backend API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database: Defaults to local SQLite file; replace with postgresql://... for Supabase / Neon
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./cometripwithme.db")
    
    # Razorpay Payment Gateway Keys (Test / Sandbox mode)
    RAZORPAY_KEY_ID: str = os.getenv("RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET: str = os.getenv("RAZORPAY_KEY_SECRET", "")
    RAZORPAY_WEBHOOK_SECRET: str = os.getenv("RAZORPAY_WEBHOOK_SECRET", "")
    
    # If keys are missing, enable Sandbox Mock Mode so testers can test full payment loop without keys
    ALLOW_MOCK_PAYMENTS: bool = os.getenv("ALLOW_MOCK_PAYMENTS", "true").lower() in ("true", "1", "yes")
    
    # CORS: Allow local dev servers and production Netlify domains
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "https://app.netlify.com",
        "*"
    ]
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "cometripwithme-super-secret-beta-key-2026")

settings = Settings()
