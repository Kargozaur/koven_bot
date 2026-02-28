import asyncio
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.exceptions import EntityCreationError
from src.entities.models.characters.character import Character
from src.entities.models.characters.owner import Owner
from src.entities.models.characters.owner_to_char import OwnerToCharacter
from src.entities.models.realm.realm import Realm
from src.entities.models.realm.realm_all import RealmsInfo
from src.entities.models.realm.region import Region
from src.entities.schemas.character import (
    CharacterDTO,
    CharacterInfo,
)
from src.repositories.base_repository import BaseRepository


class CharacterRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def save_character(self, discord_id: int, dto: CharacterDTO) -> None:
        """
        Saves character information to the database.

        :param discord_id: The Discord ID of the user to save the character for
        :param dto: The character information to save

        :raises ValueError: If the region is not supported
        :raises EntityCreationError: If an error occurs while creating an entity
        :raises Exception: If any other unexpected error occurs
        """
        try:
            region_map = {"na": 1, "eu": 2, "kr": 3, "tw": 4}
            target_region_id = region_map.get(dto.region.lower())

            if not target_region_id:
                raise ValueError(f"Region is not supported: {dto.region}")

            region: Region | None = await super().get_entity(
                Region, id=target_region_id
            )
            if not region:
                raise ValueError("Region not found in DB")

            search_name: str = dto.realm.replace("-", " ").title()
            realm: Realm | None = await super().get_entity(
                Realm, realm_name=search_name
            )

            if not realm:
                short_name: str = await asyncio.to_thread(
                    Realm._generate_candidate, search_name
                )
                realm: Realm = await super().create_entity(
                    Realm,
                    realm_name=search_name,
                    realm_short_name=short_name,
                )
                print(f"Created realm: {realm.realm_name}")

            realm_info: RealmsInfo | None = await super().get_entity(
                RealmsInfo, realm_slug_id=realm.id, realm_region_id=region.id
            )
            if not realm_info:
                realm_info: RealmsInfo = await super().create_entity(
                    RealmsInfo,
                    realm_slug_id=realm.id,
                    realm_region_id=region.id,
                    locale_id=2,  # placeholder
                )

            owner: Owner | None = await super().get_entity(Owner, discord_id=discord_id)
            if not owner:
                owner: Owner = await super().create_entity(Owner, discord_id=discord_id)
            character: Character | None = await super().get_entity(
                Character, character_name=dto.character_name, realm_id=realm.id
            )
            if not character:
                character_data: CharacterInfo = CharacterInfo(**dto.model_dump())
                character: Character = await super().create_entity(
                    Character,
                    **character_data.model_dump(exclude_unset=True),
                    realm_id=realm.id,
                )

            link: OwnerToCharacter | None = await super().get_entity(
                OwnerToCharacter, owner_id=owner.id, character_id=character.id
            )
            if not link:
                await super().create_entity(
                    OwnerToCharacter, owner_id=owner.id, character_id=character.id
                )
            print(f"Successfully saved character: {dto.character_name}")

        except (ValueError, EntityCreationError) as e:
            await self.session.rollback()
            print(f"Error: {e}")
        except Exception as e:
            await self.session.rollback()
            print(f"Unexpected error: {e}")
            import traceback

            traceback.print_exc()

    async def get_characters(self, discord_id: int) -> Sequence:
        try:
            query = sa.text("""SELECT
                c.character_name, c.url, r.realm_name,re.region
                FROM characters c JOIN owner_to_character otc on c.id = otc.character_id
                JOIN owner o on otc.owner_id = o.id
                    and o.discord_id = :discord_id
                JOIN realm r on c.realm_id = r.id
                JOIN realms_info ri on r.id = ri.realm_slug_id
                JOIN region re on ri.realm_region_id = re.id
                """)
            result = await self.session.execute(
                query.bindparams(
                    sa.bindparam("discord_id", value=discord_id, type_=sa.BigInteger)
                ),
            )
            rows = result.mappings().all()
            return rows
        except Exception as e:
            print(f"Error: {e}")
            return []

    async def update_character(
        self,
        character_name: str,
        **updated_data: object,
    ) -> bool | None:
        character: Character | None = await super().get_entity(
            Character, character_name=character_name
        )
        if not character:
            return None
        result: Character | None = await super().update_entity(
            Character, character.id, **updated_data
        )
        if not result:
            return None
        return True
