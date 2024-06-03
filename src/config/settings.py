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
    DB_URL: str
    SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECURITY_ALGORITHM: str
    # SECRETS
    SECURITY_API_SECRET_KEY: str

    def build_logger(self) -> Logger:
        """Build logger."""
        datefmt_str = (
            '[%X]' if self.ENVIROMENT == 'development' else '[%Y-%m-%d %X]'
        )
        logging.basicConfig(
            #FIXME: Porque não ta conseguindo pegar o log_level do env?
            # level=getattr(logging, self.LOG_LEVEL),  # noqa: ERA001
            level=getattr(logging, 'WARNING'),  # noqa: B009
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
