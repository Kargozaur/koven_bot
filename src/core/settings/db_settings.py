import os
from typing import Annotated

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Doc

Port = Annotated[
    int,
    Field(ge=1, le=65535, default=5432),
    Doc("Assuming that db is postgres with port 5432"),
]


class AbstractDBConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".db.env", extra="ignore", env_prefix="DB_"
    )

    @property
    def dsn(self) -> str:
        raise NotImplementedError()


class PostgresConfig(AbstractDBConfig):
    user: str
    password: str
    driver: str = Field(default="asyncpg")
    host: str
    name: str
    port: Port

    @property
    def dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme=f"postgresql+{self.driver}",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.name,
            )
        )


class SQLiteConfig(AbstractDBConfig):
    path: str = Field(default="database.db")
    driver: str = Field(default="aiosqlite")

    @property
    def dsn(self) -> str:
        return f"sqlite+{self.driver}:///{self.path}"


def create_db_settings() -> AbstractDBConfig:
    from dotenv import load_dotenv

    load_dotenv(".db.env")
    db_type = os.getenv("DB_TYPE", "sqlite").lower()
    configs: dict[str, type[AbstractDBConfig]] = {
        "postgres": PostgresConfig,
        "sqlite": SQLiteConfig,
    }
    config_class = configs.get(db_type)
    if not config_class:
        raise ValueError(f"Unsupported DB type: {db_type}")
    return config_class()
