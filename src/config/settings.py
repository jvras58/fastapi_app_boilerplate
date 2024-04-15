"""Settings module for the project."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the project."""

    model_config: str = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

    ENVIROMENT: str
    LOG_LEVEL: str


@lru_cache
def get_settings() -> Settings:
    """Return the settings."""
    return Settings()
