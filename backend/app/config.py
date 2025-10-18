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
    
    # Cloudflare Configuration
    cloudflare_account_id: str | None = None
    cloudflare_api_token: str | None = None
    cloudflare_d1_database_id: str | None = None
    cloudflare_r2_access_key_id: str | None = None
    cloudflare_r2_secret_access_key: str | None = None
    cloudflare_r2_bucket_name: str | None = None
    cloudflare_kv_namespace_id: str | None = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
    @property
    def cloudflare_configured(self) -> bool:
        """Check if Cloudflare is properly configured"""
        return bool(self.cloudflare_account_id and self.cloudflare_api_token)
    
    @property
    def cloudflare_d1_configured(self) -> bool:
        """Check if Cloudflare D1 database is configured"""
        return bool(self.cloudflare_account_id and self.cloudflare_api_token and self.cloudflare_d1_database_id)

settings = Settings()

