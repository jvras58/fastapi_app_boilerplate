"""Settings module for the project."""

import logging
from functools import lru_cache
from logging import Logger

from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.logging import RichHandler


class Settings(BaseSettings):
    """Settings for the project."""

    model_config: str = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        secrets_dir='secrets',
    )

    ENVIROMENT: str
    LOG_LEVEL: str

    def build_logger(self) -> Logger:
        """Build logger."""
        datefmt_str = (
            '[%X]' if self.ENVIROMENT == 'development' else '[%Y-%m-%d %X]'
        )
        logging.basicConfig(
            level=getattr(logging, self.LOG_LEVEL),
            format='%(message)s',
            datefmt=datefmt_str,
            handlers=[RichHandler()],
        )

        return logging.getLogger()


@lru_cache
def get_settings() -> Settings:
    """Return the settings."""
    return Settings()


def get_logger() -> Logger:
    """Return the logger."""
    return get_settings().build_logger()
