import asyncio

from dishka import AsyncContainer

from src.entities.schemas.character import CharacterUpdate
from src.params.char_params import CharParamns
from src.services.rio_service import RaiderIOService
from src.unit_of_work.unit_of_work import UnitOfWork


class CharacterUpdater:
    def __init__(self, container: AsyncContainer, rio_service: RaiderIOService) -> None:
        self.container = container
        self.rio_service = rio_service
        self.semaphore = asyncio.Semaphore(5)

    async def update_characters(self) -> None:
        async with self.container() as request_container:
            UoW = await request_container.get(UnitOfWork)
            characters = await UoW.char_repo.get_all_info()
        tasks = [self._update_single_character(char) for char in characters]
        await asyncio.gather(*tasks)

    async def _update_single_character(self, char: dict) -> None:
        async with self.semaphore:
            async with self.container() as request_container:
                UoW = await request_container.get(UnitOfWork)
                try:
                    params = None
                    if char["url"]:
                        params = await asyncio.to_thread(
                            self.rio_service._extract_params_from_url, char["url"]
                        )
                    else:
                        params = CharParamns(
                            region=char["region"],
                            realm=char["realm_name"],
                            name=char["character_name"],
                        )
                    if not params:
                        return
                    fresh_data = await self.rio_service.fetch_character(params)
                    if not fresh_data:
                        return
                    updated_data: dict = {}
                    if not char["url"] and fresh_data.get("profile_url"):
                        updated_data["url"] = str(fresh_data["profile_url"])
                    if char["achievement_points"] != fresh_data.get(
                        "achievement_points"
                    ):
                        updated_data["achievement_points"] = fresh_data[
                            "achievement_points"
                        ]
                    if not updated_data:
                        return
                    verified_data = CharacterUpdate(
                        **updated_data,
                    )
                    await UoW.char_repo.update_character(
                        character_name=char["character_name"],
                        **verified_data.model_dump(exclude_unset=True),
                    )
                    await UoW.commit()
                except Exception as exc:
                    await UoW.rollback()
                    print(
                        f"Failed to update character: {char['character_name']}: {exc}"
                    )
