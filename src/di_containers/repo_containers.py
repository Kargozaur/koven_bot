from discord.ext.commands import Context
from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.character_repo import CharacterRepository


class RepositoryProvider(Provider):
    scope = Scope.REQUEST
    discord_context = from_context(Context, scope=Scope.REQUEST)

    @provide
    def character_repo(self, session: AsyncSession) -> CharacterRepository:
        return CharacterRepository(session)
