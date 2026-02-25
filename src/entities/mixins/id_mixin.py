from uuid import UUID, uuid7

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

PossibleID = int | UUID


class IdMixin[T: PossibleID]:
    id: Mapped[T]


class IntIdMixin(IdMixin[int]):
    id: Mapped[int] = mapped_column(primary_key=True)


class UUIDIdMixin(IdMixin[UUID]):
    id: Mapped[UUID] = mapped_column(sa.UUID(as_uuid=True), default=uuid7)
