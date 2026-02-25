from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class RioSettings(BaseSettings):
    key: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="RIO_", extra="ignore"
    )
