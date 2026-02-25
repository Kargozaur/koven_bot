from dishka import Provider, Scope, provide

from src.core.settings.db_settings import AbstractDBConfig
from src.core.settings.discord_settings import DiscordSettings
from src.core.settings.rio_settings import RioSettings
from src.core.settings.settings import Settings


class SetingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()

    @provide(scope=Scope.APP)
    def get_db_config(self, settings: Settings) -> AbstractDBConfig:
        return settings.db

    @provide(scope=Scope.APP)
    def get_discord_settings(self, settings: Settings) -> DiscordSettings:
        return settings.discord

    @provide(scope=Scope.APP)
    def get_rio_settings(self, settings: Settings) -> RioSettings:
        return settings.rio
