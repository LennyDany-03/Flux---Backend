# app/core/config.py
from typing import List
import json
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # other settings ... e.g.
    SUPABASE_URL: str | None = None
    SUPABASE_SERVICE_ROLE_KEY: str | None = None

    # make ALLOWED_ORIGINS robust to JSON, CSV, or missing
    ALLOWED_ORIGINS: List[str] = Field(default_factory=list)

    @field_validator("ALLOWED_ORIGINS", mode="before")
    def parse_allowed_origins(cls, v):
        # Accept None, empty, JSON list string, or comma-separated string
        if v is None:
            return []
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return []
            if s.startswith("["):          # JSON array form
                return json.loads(s)
            return [p.strip() for p in s.split(",") if p.strip()]  # CSV form
        return v

settings = Settings()
