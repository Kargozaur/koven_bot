from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.exceptions import EntityCreationError, EntityUpdateError


class BaseRepository:
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
            # If an error occurs while creating an entity, raise an EntityUpdateError
            raise EntityCreationError(
                f"Failed to create {model.__name__}: {exc}"
            ) from exc

    async def update_entity[ModelT](
        self, model: type[ModelT], entity_id: int | UUID, **attributes: object
    ) -> ModelT | None:
        """
        Updates an entity in the database.
        :param model: The type of the entity to update
        :param attributes: The attributes of the entity to update
        :return: The updated entity
        :raises EntityUpdateError: If an error occurs while updating an entity
        """
        entity = await self.session.get(model, entity_id)
        if not entity:
            return None

        for key, value in attributes.items():
            setattr(entity, key, value)

        try:
            await self.session.flush()
            return entity
        except Exception as exc:
            # If an error occurs while updating an entity, raise an EntityUpdateError
            raise EntityUpdateError(
                f"Failed to update {model.__name__}: {exc}"
            ) from exc
