from dishka import Provider, Scope, provide
from httpx import AsyncClient

from src.services.rio_service import RaiderIOService


class RioContainer(Provider):
    @provide(scope=Scope.REQUEST)
    def get_rio_service(self, http_client: AsyncClient) -> RaiderIOService:
        return RaiderIOService(http_client)
