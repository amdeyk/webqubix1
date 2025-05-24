# Section 1: Configuration settings for the application
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application configuration settings with environment variable support"""
    
    # Section 2: Database settings
    DATABASE_URL: str = "sqlite:///./qubix_events.db"
    
    # Section 3: Application settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Section 4: SEO and Web settings
    BASE_URL: str = "https://qubixsolutions.in"
    SITE_NAME: str = "Qubix Events & Conferences Pvt. Ltd."
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Section 5: Email settings
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    EMAIL_USERNAME: str = ""
    EMAIL_PASSWORD: str = ""
    CONTACT_EMAIL: str = "info@qubixsolutions.in"
    
    # Section 6: Social media links
    FACEBOOK_URL: str = "https://www.facebook.com/profile.php?id=100069058346547"
    INSTAGRAM_URL: str = "https://www.instagram.com/qubix12/"
    YOUTUBE_URL: str = "https://www.youtube.com/@qubixsolutions1702/featured"
    LINKEDIN_URL: str = "https://www.linkedin.com/company/qubix-events"
    
    # Section 7: Contact information
    PHONE_NUMBERS: List[str] = ["+91-98993-39005", "+91-11401-91417", "+91-85850-56488"]
    ADDRESSES: List[dict] = [
        {
            "city": "Delhi",
            "address": "C 32 Madhu Vihar, IP Extension, Delhi 110092",
            "type": "Headquarters"
        },
        {
            "city": "Kolkata", 
            "address": "7b Allenby Road, Kolkata 700020",
            "type": "Branch"
        },
        {
            "city": "Bangalore",
            "address": "19/C, Vyshya Bank Colony, BTM 2nd Stage",
            "type": "Branch"
        }
    ]
    
    class Config:
        env_file = ".env"

# Section 8: Create settings instance
settings = Settings()