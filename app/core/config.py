# app/core/config.py
from typing import List, Optional
import json, os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str

    API_BASE_URL: str = "http://localhost:8000"

    # read as a *string* so pydantic doesn't try JSON parsing
    ALLOWED_ORIGINS_RAW: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        v = self.ALLOWED_ORIGINS_RAW
        if v is None:
            return []  # fallback to empty -> you can default in CORS
        s = v.strip()
        if not s:
            return []
        if s.startswith("["):  # JSON array
            try:
                return json.loads(s)
            except Exception:
                return []
        # CSV list
        return [p.strip() for p in s.split(",") if p.strip()]

settings = Settings()
