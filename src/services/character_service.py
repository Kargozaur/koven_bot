from src.core.decorators.read_only import read_only
from src.core.decorators.transactional import transactional
from src.entities.schemas.character import (
    CharacterDTO,
    CharacterResponse,
    CharacterUpdate,
)
from src.unit_of_work.unit_of_work import UnitOfWork


class CharacterService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.UoW = uow

    @transactional
    async def create_character(
        self, discord_id: int, character_dto: CharacterDTO
    ) -> None | str:
        result = await self.UoW.char_repo.save_character(
            discord_id=discord_id, dto=character_dto
        )
        if result is not None:
            return result

    @read_only
    async def get_characters(self, discord_id: int) -> list[CharacterResponse]:
        result = await self.UoW.char_repo.get_characters(discord_id=discord_id)
        return [
            CharacterResponse.model_validate(row) for row in result if row is not None
        ]

    @transactional
    async def update_character(
        self, character_name: str, data: CharacterUpdate
    ) -> bool | None:
        result: bool | None = await self.UoW.char_repo.update_character(
            character_name=character_name, **data.model_dump(exclude_unset=True)
        )
        return result

    @transactional
    async def delete_character(
        self, discord_id: int, character_name: str
    ) -> bool | None | str:
        result: bool | None | str = await self.UoW.char_repo.delete_character(
            discord_id=discord_id, character_name=character_name
        )
        return result
