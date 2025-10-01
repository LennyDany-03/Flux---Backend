from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str

    API_BASE_URL: str = "http://localhost:8000"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    # pydantic-settings parses list from comma-separated string when annotated as List[str]
    # e.g. ALLOWED_ORIGINS="http://localhost:3000,https://your-frontend.com"

settings = Settings()
