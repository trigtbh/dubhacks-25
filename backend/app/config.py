from pydantic_settings import BaseSettings
from typing import List
import json

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
    cloudflare_r2_account_id: str | None = None
    cloudflare_r2_access_key_id: str | None = None
    cloudflare_r2_secret_access_key: str | None = None
    cloudflare_r2_bucket_name: str | None = None
    cloudflare_kv_namespace_id: str | None = None

    # Google SSO Configuration
    google_client_id: str | None = None
    google_client_secret: str | None = None
    google_redirect_uri: str | None = None
    
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
    
    @property
    def cloudflare_r2_configured(self) -> bool:
        """Check if Cloudflare R2 storage is configured"""
        return bool(
            self.cloudflare_r2_account_id and 
            self.cloudflare_r2_access_key_id and 
            self.cloudflare_r2_secret_access_key and 
            self.cloudflare_r2_bucket_name
        )

    @property
    def google_sso_configured(self) -> bool:
        """Check if Google SSO is properly configured"""
        return bool(self.google_client_id and self.google_client_secret and self.google_redirect_uri)

try:
    with open("secrets/googlesso.json", "r") as gsso:
        gsettings = json.load(gsso)
        settings = Settings(google_login="/auth/google/callback", google_client_id=gsettings["web"]["client_id"], google_client_secret=gsettings["web"]["client_secret"])
except FileNotFoundError:
    import sys
    print("Error! Could not import `secrets/googlesso.json`!")
    sys.exit(1)
