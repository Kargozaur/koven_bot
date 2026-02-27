from discord.ext.commands import Context
from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.character_repo import CharacterRepository


class RepositoryProvider(Provider):
    discord_context = from_context(Context, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def character_repo(self, session: AsyncSession) -> CharacterRepository:
        print("injecting character repo")
        rep = CharacterRepository(session)
        print("injected character repo")
        return rep
