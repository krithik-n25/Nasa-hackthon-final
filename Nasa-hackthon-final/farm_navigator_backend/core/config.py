# nasa_api_app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

# Set the path relative to the directory where uvicorn is executed (nasa_feature_dev/)
# This is often more reliable than using relative paths inside a package
PROJECT_ROOT = Path(__file__).parent.parent.parent # C:\Users\HP\OneDrive\Desktop\manager\nasa_feature_dev
ENV_PATH = PROJECT_ROOT / ".env" # Path object pointing to nasa_feature_dev/.env

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    model_config = SettingsConfigDict(
        # Pass the explicit Path object to the env_file setting
        env_file=ENV_PATH, 
        extra="ignore" 
    )

    NASA_API_KEY: str = Field(..., description="API key for NASA data access.")
    NASA_BASE_URL: str = "https://api.nasa.gov/"
    
settings = Settings()