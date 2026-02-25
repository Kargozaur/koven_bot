from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DiscordSettings(BaseSettings):
    token: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_prefix="DISCORD_"
    )
