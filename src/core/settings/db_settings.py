import os
from typing import Annotated

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Doc

Port = Annotated[
    int,
    Field(ge=1, le=65535, default=5432),
    Doc("Assuming that our default db is postgres"),
]


class AbstractDBConfig(BaseSettings):
    ...

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

    model_config = SettingsConfigDict(
        env_file=".db.env", extra="ignore", env_prefix="DB_"
    )

    @property
    def dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme=f"postgres+{self.driver}",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.name,
            )
        )


def create_db_settings() -> AbstractDBConfig:
    from dotenv import load_dotenv

    load_dotenv(".env.db")
    db_type = os.getenv("DB_TYPE", "postgres").lower()
    configs: dict[str, type[AbstractDBConfig]] = {"postgres": PostgresConfig}
    config_class = configs.get(db_type)
    if not config_class:
        raise ValueError(f"Unsupported DB type: {db_type}")
    return config_class()
