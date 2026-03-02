import asyncio
from collections.abc import Sequence
from uuid import UUID

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

    async def _get_or_validate_region(self, region_name: str) -> Region:
        region_map = {"na": 1, "eu": 2, "kr": 3, "tw": 4}
        target_id = region_map.get(region_name.lower())

        if not target_id:
            raise ValueError(f"Region is not supported: {region_name}")

        region = await super().get_entity(Region, id=target_id)
        if not region:
            raise ValueError("Region not found in DB")
        return region

    async def _get_or_create_realm(self, realm_raw_name: str) -> Realm:
        search_name = realm_raw_name.replace("-", " ").title()
        realm = await super().get_entity(Realm, realm_name=search_name)

        if not realm:
            short_name = await asyncio.to_thread(Realm._generate_candidate, search_name)
            realm = await super().create_entity(
                Realm,
                realm_name=search_name,
                realm_short_name=short_name,
            )
            print(f"Created realm: {realm.realm_name}")
        return realm

    async def _ensure_realm_info(self, realm_id: int, region_id: int) -> None:
        realm_info = await super().get_entity(
            RealmsInfo, realm_slug_id=realm_id, realm_region_id=region_id
        )
        if not realm_info:
            await super().create_entity(
                RealmsInfo,
                realm_slug_id=realm_id,
                realm_region_id=region_id,
                locale_id=2,  # placeholder
            )

    async def _ensure_realm_info(self, realm_id: int, region_id: int) -> None:
        realm_info = await super().get_entity(
            RealmsInfo, realm_slug_id=realm_id, realm_region_id=region_id
        )
        if not realm_info:
            await super().create_entity(
                RealmsInfo,
                realm_slug_id=realm_id,
                realm_region_id=region_id,
                locale_id=2,  # placeholder
            )

    async def _get_or_create_character(
        self, dto: CharacterDTO, realm_id: int
    ) -> Character:
        character = await super().get_entity(
            Character, character_name=dto.character_name, realm_id=realm_id
        )
        if not character:
            character_data = CharacterInfo(**dto.model_dump())
            character = await super().create_entity(
                Character,
                **character_data.model_dump(exclude_unset=True),
                realm_id=realm_id,
            )
        return character

    async def _link_owner_to_character(
        self, owner_id: UUID, character_id: UUID
    ) -> None:
        link = await super().get_entity(
            OwnerToCharacter, owner_id=owner_id, character_id=character_id
        )

        if link:
            if link.is_deleted:
                link.is_deleted = False
            return

        await super().create_entity(
            OwnerToCharacter, owner_id=owner_id, character_id=character_id
        )

    async def _get_or_create_owner(self, discord_id: int) -> Owner | str:
        owner = await super().get_entity(Owner, discord_id=discord_id)
        if owner:
            if owner.is_deleted:
                return "Author is deleted"
            return owner

        return await super().create_entity(Owner, discord_id=discord_id)

    async def _get_or_create_owner(self, discord_id: int) -> Owner | str:
        owner = await super().get_entity(Owner, discord_id=discord_id)
        if owner:
            if owner.is_deleted:
                return "Author is deleted"
            return owner

        return await super().create_entity(Owner, discord_id=discord_id)

    async def save_character(self, discord_id: int, dto: CharacterDTO) -> None | str:
        """
        Saves a character to the database.

        Parameters
        ----------
        discord_id : int
            The Discord ID of the user associated with the character.
        dto : CharacterDTO
            A data transfer object containing the character's information.

        Returns
        -------
        None | str
            If successful, returns None. Otherwise, returns a string
            describing the error.

        Raises
        ------
        ValueError
            If the region is not supported.
        EntityCreationError
            If the character or associated realm could not be created.
        """
        try:
            region = await self._get_or_validate_region(dto.region)
            realm = await self._get_or_create_realm(dto.realm)

            await self._ensure_realm_info(realm.id, region.id)

            owner = await self._get_or_create_owner(discord_id)
            if isinstance(owner, str):
                return owner

            character: Character = await self._get_or_create_character(dto, realm.id)
            await self._link_owner_to_character(owner.id, character.id)

            print(f"Successfully saved character: {dto.character_name}")
            return None

        except (ValueError, EntityCreationError) as e:
            print(f"Error: {e}")
            return str(e)
        except Exception as e:
            print(f"Unexpected error: {e}")
            import traceback

            traceback.print_exc()
            return "Internal error"
        except (ValueError, EntityCreationError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            import traceback

            traceback.print_exc()

    async def get_characters(self, discord_id: int) -> Sequence:
        """
        Get a list of all characters associated with a given Discord ID.

        Parameters
        ----------
        discord_id : int
            The Discord ID of the user whose characters we want to get.

        Returns
        -------
        Sequence
            A list of tuples, each containing the character name, URL, realm name,
            and region of the associated characters.
        """
        try:
            query = sa.text("""SELECT
                c.character_name, c.url, r.realm_name,re.region
                FROM characters c
                JOIN owner_to_character otc on c.id = otc.character_id
                    and otc.is_deleted is false
                JOIN owner o on otc.owner_id = o.id
                    and o.discord_id = :discord_id
                    and o.is_deleted is false
                JOIN realm r on c.realm_id = r.id
                JOIN realms_info ri on r.id = ri.realm_slug_id
                JOIN region re on ri.realm_region_id = re.id
                WHERE c.is_deleted is false
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
        """
        Updates a character in the database.

        Parameters
        ----------
        character_name : str
            The name of the character to update.
        **updated_data : object
            A dictionary containing the fields of the character to update and their
            corresponding values.

        Returns
        -------
        bool | None
            True if the character was successfully updated, None if an error
            occurred.
        """
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

    async def delete_character(
        self, discord_id: int, character_name: str
    ) -> bool | None | str:
        """
        Deletes a character from the database.

        Parameters
        ----------
        discord_id : int
            The Discord ID of the user whose character we want to delete.
        character_name : str
            The name of the character to delete.

        Returns
        -------
        bool | None | str
            True if the character was successfully deleted, None if an error occurred,
            or a string if the author or character was not found.
        """
        try:
            author: Owner | None = await super().get_entity(
                Owner, discord_id=discord_id
            )
            if not author or author.is_deleted is True:
                return "Author not found or deleted"
            character: Character | None = await super().get_entity(
                Character, character_name=character_name
            )
            if not character:
                return f"{character_name} not found"
            return await super().delete_entity(
                OwnerToCharacter, owner_id=author.id, character_id=character.id
            )
        except Exception as exc:
            print(f"Error: {exc}")
            return "Techical error"

    async def get_all_info(self) -> Sequence:
        """
        Gets all information about all characters in the database.

        Returns
        -------
        Sequence
            A list of dicts, each containing the character name, realm name, URL,
            achievement points, updated at timestamp, and region of the associated
            characters.
        """
        query = sa.text("""SELECT
        c.character_name, r.realm_name, c.url, c.achievement_points,
        c.updated_at, re.region
        FROM characters c
        JOIN realm r on c.realm_id = r.id
        JOIN realms_info ri on r.id = ri.realm_slug_id
        JOIN region re on ri.realm_region_id = re.id
        where c.is_deleted is false
        """)
        result = await self.session.execute(query)
        rows = result.mappings().all()
        return rows
