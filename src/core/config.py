import os

from dotenv import load_dotenv, find_dotenv
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
    AlembicAsyncConfig,
)


load_dotenv(find_dotenv())


class DBVars:
    """Database env variables"""

    HOST: str = os.environ.get("DB_HOST")
    PORT: str = os.environ.get("DB_PORT")
    NAME: str = os.environ.get("DB_NAME")
    USER: str = os.environ.get("DB_USER")
    PASS: str = os.environ.get("DB_PASS")


class SQLAlchemy:
    plugin: SQLAlchemyPlugin

    def __init__(self):
        self.plugin = SQLAlchemyPlugin(
            config=SQLAlchemyAsyncConfig(
                connection_string=self.generate_postgresql_dsn(),
                before_send_handler="autocommit",
                session_config=AsyncSessionConfig(expire_on_commit=False),
                alembic_config=AlembicAsyncConfig(
                    script_location="./alembic",
                ),
                create_all=True,
            ),
        )

    def generate_postgresql_dsn(self) -> str:
        """Returns PostgreSQL DSN string"""
        return (
            "postgresql+asyncpg://"
            f"{DBVars.USER}:{DBVars.PASS}"
            "@"
            f"{DBVars.HOST}:{DBVars.PORT}"
            "/"
            f"{DBVars.NAME}"
        )


class Settings:
    """Config settings"""

    sqlalchemy: SQLAlchemy = SQLAlchemy()


settings = Settings()
