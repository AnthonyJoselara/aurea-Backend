import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    port: int = 3000
    host: str = "0.0.0.0"
    environment: str = "development"
    debug: bool = True

    # Supabase y JWT
    supabase_url: str = "https://example.supabase.co"
    supabase_anon_key: str = "anon-key-placeholder"
    supabase_service_role_key: str = "service-role-placeholder"
    supabase_jwt_secret: str = "super-secret-jwt-key-for-testing-purposes-32-chars-min"
    database_url: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
