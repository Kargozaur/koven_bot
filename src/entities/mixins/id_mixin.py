from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

PossibleID = int | UUID


class IdMixin[T: PossibleID]:
    id: Mapped[T] = mapped_column(primary_key=True)
