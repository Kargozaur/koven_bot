import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.exceptions import EntityCreationError
from src.entities.models.characters.character import Character
from src.entities.models.characters.owner import Owner
from src.entities.models.characters.owner_to_char import OwnerToCharacter
from src.entities.models.realm.realm import Realm
from src.entities.models.realm.realm_all import RealmsInfo
from src.entities.models.realm.region import Region
from src.entities.schemas.character import CharacterDTO


class CharacterRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_entity[ModelT](
        self, model: type[ModelT], **filters: object
    ) -> ModelT | None:
        """
        Retrieves an entity from the database based on the given filters.
        :param model: The type of the entity to retrieve
        :param filters: The filters to apply to the query
        :return: The retrieved entity, or None if no entity was found
        """
        query = select(model).filter_by(**filters)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_entity[ModelT](
        self, model: type[ModelT], **attributes: object
    ) -> ModelT:
        """
        Creates an entity in the database.
        :param model: The type of the entity to create
        :param attributes: The attributes of the entity to create
        :return: The created entity
        :raises EntityCreationError: If an error occurs while creating an entity
        """
        entity = model(**attributes)
        self.session.add(entity)
        try:
            await self.session.flush()
            return entity
        except Exception as exc:
            # If an error occurs while creating an entity, raise an EntityCreationError
            raise EntityCreationError(
                f"Failed to create {model.__name__}: {exc}"
            ) from exc

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

            region: Region | None = await self.get_entity(Region, id=target_region_id)
            if not region:
                raise ValueError("Region not found in DB")

            search_name: str = dto.realm.replace("-", " ").title()
            realm: Realm | None = await self.get_entity(Realm, realm_name=search_name)

            if not realm:
                short_name: str = await asyncio.to_thread(
                    Realm._generate_candidate, search_name
                )
                realm: Realm = await self.create_entity(
                    Realm,
                    realm_name=search_name,
                    realm_short_name=short_name,
                )
                print(f"Created realm: {realm.realm_name}")

            realm_info: RealmsInfo | None = await self.get_entity(
                RealmsInfo, realm_slug_id=realm.id, realm_region_id=region.id
            )
            if not realm_info:
                realm_info: RealmsInfo = await self.create_entity(
                    RealmsInfo,
                    realm_slug_id=realm.id,
                    realm_region_id=region.id,
                    locale_id=2,  # placeholder
                )

            owner: Owner | None = await self.get_entity(Owner, discord_id=discord_id)
            if not owner:
                owner: Owner = await self.create_entity(Owner, discord_id=discord_id)

            character: Character | None = await self.get_entity(
                Character, character_name=dto.name, realm_id=realm.id
            )
            if not character:
                character: Character = await self.create_entity(
                    Character,
                    character_name=dto.name,
                    realm_id=realm.id,
                )

            link: OwnerToCharacter | None = await self.get_entity(
                OwnerToCharacter, owner_id=owner.id, character_id=character.id
            )
            if not link:
                await self.create_entity(
                    OwnerToCharacter, owner_id=owner.id, character_id=character.id
                )

            await self.session.commit()
            print(f"Successfully saved character: {dto.name}")

        except (ValueError, EntityCreationError) as e:
            await self.session.rollback()
            print(f"Error: {e}")
        except Exception as e:
            await self.session.rollback()
            print(f"Unexpected error: {e}")
            import traceback

            traceback.print_exc()
