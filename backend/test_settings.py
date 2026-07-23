import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="/c/SIGAP/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    # ... existing fields ...
    JWT_SECRET_KEY: str

# Test loading settings
try:
    settings = Settings()
    print(f"✅ Settings loaded successfully")
    print(f"JWT_SECRET_KEY: {settings.JWT_SECRET_KEY[:20]}...")
except Exception as e:
    print(f"❌ Settings load failed: {e}")
    import traceback
    traceback.print_exc()
