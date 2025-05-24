from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import List, Union
import json

class Settings(BaseSettings):
    """Application configuration settings with environment variable support"""
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./qubix_events.db"
    
    # Application settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # SEO and Web settings
    BASE_URL: str = "https://qubixsolutions.in"
    SITE_NAME: str = "Qubix Events & Conferences Pvt. Ltd."
    
    # Fixed ALLOWED_HOSTS with proper validation
    ALLOWED_HOSTS: List[str] = Field(default=["*"])
    
    # Email settings
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    EMAIL_USERNAME: str = ""
    EMAIL_PASSWORD: str = ""
    CONTACT_EMAIL: str = "info@qubixsolutions.in"
    
    # Social media links
    FACEBOOK_URL: str = "https://www.facebook.com/profile.php?id=100069058346547"
    INSTAGRAM_URL: str = "https://www.instagram.com/qubix12/"
    YOUTUBE_URL: str = "https://www.youtube.com/@qubixsolutions1702/featured"
    LINKEDIN_URL: str = "https://www.linkedin.com/company/qubix-events"
    
    # Contact information - Fixed parsing
    PHONE_NUMBERS: List[str] = Field(default=["+91-98993-39005", "+91-11401-91417", "+91-85850-56488"])
    ADDRESSES: List[dict] = Field(default=[
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
    ])

    @field_validator('ALLOWED_HOSTS', mode='before')
    @classmethod
    def parse_allowed_hosts(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse ALLOWED_HOSTS from various formats"""
        if isinstance(v, str):
            if v.strip() == "" or v.strip() == "*":
                return ["*"]
            # Handle JSON string format
            if v.startswith('[') and v.endswith(']'):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            # Handle comma-separated values
            if "," in v:
                return [host.strip() for host in v.split(",")]
            # Single host
            return [v.strip()]
        return v if isinstance(v, list) else ["*"]

    @field_validator('PHONE_NUMBERS', mode='before')
    @classmethod
    def parse_phone_numbers(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse phone numbers from comma-separated string or list"""
        if isinstance(v, str):
            if "," in v:
                return [phone.strip() for phone in v.split(",")]
            return [v.strip()]
        return v if isinstance(v, list) else []

    @field_validator('ADDRESSES', mode='before')
    @classmethod
    def parse_addresses(cls, v: Union[str, List[dict]]) -> List[dict]:
        """Parse addresses from JSON string or list"""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v if isinstance(v, list) else []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

# Create settings instance
settings = Settings()
