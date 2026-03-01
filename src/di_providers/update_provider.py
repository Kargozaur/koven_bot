from dishka import AsyncContainer, Provider, Scope, provide

from src.polling.character_updater import CharacterUpdater
from src.services.rio_service import RaiderIOService


class UpdateProvider(Provider):
    @provide(scope=Scope.APP)
    def get_character_updater(
        self, container: AsyncContainer, rio_service: RaiderIOService
    ) -> CharacterUpdater:
        print("injecting character updater")
        updater = CharacterUpdater(container, rio_service)
        print("injected character updater")
        return updater
