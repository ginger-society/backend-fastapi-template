import enum
from pathlib import Path
from tempfile import gettempdir
from typing import Optional

from pydantic import BaseSettings
from yarl import URL

import sys
import logging
from dotenv import dotenv_values

from loguru import logger

from core.logging import InterceptHandler

TEMP_DIR = Path(gettempdir())

config = dotenv_values("../.env")


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    API_PREFIX = "/api"
    VERSION = "0.1.0"
    DEBUG: bool = True
    SECRET_KEY: str = config["SECRET_KEY"]

    PROJECT_NAME: str = config["PROJECT_NAME"]

    # logging configuration
    LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
    logging.basicConfig(
        handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
    )
    logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

    FROM_DOCKER_COMPOSE: str = config["FROM_DOCKER_COMPOSE"]

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    # Variables for the database
    db_host: str = config["db_host"]
    db_port: int = 5432
    db_user: str = "postgres"
    db_pass: str = "postgres"
    db_base: str = "Test-db"
    db_echo: bool = True

    # Variables for Redis
    redis_host: str = config["redis_host"]
    redis_port: int = 6379
    redis_user: Optional[str] = None
    redis_pass: Optional[str] = None
    redis_base: Optional[int] = None

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = ""
        if self.redis_base is not None:
            path = f"/{self.redis_base}"
        return URL.build(
            scheme="redis",
            host=config["redis_host"],
            port=self.redis_port,
            user=self.redis_user,
            password=self.redis_pass,
            path=path,
        )


settings = Settings()
