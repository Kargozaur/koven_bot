from dishka import Provider, Scope, provide
from httpx import AsyncClient

from src.core.settings.rio_settings import RioSettings
from src.services.character_service import CharacterService
from src.services.owner_service import OwnerService
from src.services.rio_service import RaiderIOService
from src.unit_of_work.unit_of_work import UnitOfWork


class ServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def get_rio_service(
        self, http_client: AsyncClient, rio_settings: RioSettings
    ) -> RaiderIOService:
        return RaiderIOService(http_client, rio_settings)

    @provide(scope=Scope.REQUEST)
    def get_character_service(self, uow: UnitOfWork) -> CharacterService:
        print("injecting character service")
        svc = CharacterService(uow)
        print("injected character service")
        return svc

    @provide(scope=Scope.REQUEST)
    def get_owner_service(self, uow: UnitOfWork) -> OwnerService:
        print("injecting owner service")
        svc = OwnerService(uow)
        print("injected owner service")
        return svc
