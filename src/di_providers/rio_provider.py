from dishka import Provider, Scope, provide
from httpx import AsyncClient

from src.core.settings.rio_settings import RioSettings
from src.services.rio_service import RaiderIOService


class RioProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_rio_service(
        self, http_client: AsyncClient, rio_settings: RioSettings
    ) -> RaiderIOService:
        return RaiderIOService(http_client, rio_settings)
