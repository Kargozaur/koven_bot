from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.character_repo import CharacterRepository
from src.unit_of_work.iuow import IUnitOfWork


class UnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.char_repo: CharacterRepository = CharacterRepository(session)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self: Self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        if exc_val:
            await self.rollback()
        await self.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def close(self) -> None:
        await self.session.close()
