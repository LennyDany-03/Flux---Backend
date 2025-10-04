from typing import List, Optional
import json
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # === required secrets ===
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str

    # === misc ===
    API_BASE_URL: str = "http://localhost:8000"

    # Read as a raw string so pydantic doesn't try to JSON-decode it prematurely
    ALLOWED_ORIGINS_RAW: Optional[str] = None
    # Optional regex for wildcard origins (e.g., all vercel previews)
    ALLOWED_ORIGIN_REGEX: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        """Return a clean list of origins from RAW (accept JSON array or CSV)."""
        v = self.ALLOWED_ORIGINS_RAW
        if v is None:
            return []
        s = v.strip()
        if not s:
            return []
        if s.startswith("["):  # JSON array form
            try:
                parsed = json.loads(s)
                return [p.strip() for p in parsed if isinstance(p, str) and p.strip()]
            except Exception:
                return []
        # CSV form
        return [p.strip() for p in s.split(",") if p.strip()]

settings = Settings()
