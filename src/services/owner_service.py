from src.core.decorators.transactional import transactional
from src.unit_of_work.unit_of_work import UnitOfWork


class OwnerService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.UoW = uow

    @transactional
    async def deactivate_owner(self, discord_id: int) -> bool | None:
        return await self.UoW.owner_repo.deactivate_owner(discord_id=discord_id)
