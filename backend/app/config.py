from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    environment: str = "development"
    
    # CORS Settings
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # Supabase Configuration
    supabase_url: str | None = None
    supabase_key: str | None = None
    supabase_service_key: str | None = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
    @property
    def supabase_configured(self) -> bool:
        """Check if Supabase is properly configured"""
        return bool(self.supabase_url and self.supabase_key)

settings = Settings()

