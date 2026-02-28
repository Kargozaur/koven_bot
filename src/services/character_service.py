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
    ) -> None:
        await self.UoW.char_repo.save_character(
            discord_id=discord_id, dto=character_dto
        )

    @read_only
    async def get_characters(self, discord_id: int) -> list[CharacterResponse]:
        print("fetching result")
        result = await self.UoW.char_repo.get_characters(discord_id=discord_id)
        print(result, type(result))
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
