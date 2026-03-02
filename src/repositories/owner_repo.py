from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.models.characters.owner import Owner
from src.repositories.base_repository import BaseRepository


class OwnerRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def deactivate_owner(self, discord_id: int) -> bool | None:
        return await super().delete_entity(Owner, discord_id=discord_id)
