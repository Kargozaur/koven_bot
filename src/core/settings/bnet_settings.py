from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BnetSettings(BaseSettings):
    secret: SecretStr
    id: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="BNET_", extra="ignore"
    )
