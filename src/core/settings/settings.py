from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.settings.db_settings import AbstractDBConfig, create_db_settings
from src.core.settings.discord_settings import DiscordSettings
from src.core.settings.rio_settings import RioSettings


class Settings(BaseSettings):
    db: AbstractDBConfig = Field(default_factory=create_db_settings)
    discord: DiscordSettings = Field(default_factory=DiscordSettings)
    rio: RioSettings = Field(default_factory=RioSettings)

    model_config = SettingsConfigDict(
        arbitrary_types_allowed=True, case_sensitive=False
    )
