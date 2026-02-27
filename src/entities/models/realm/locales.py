import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.enums.locales_enum import LocalesEnum

from . import Base, IntIdMixin


class Locales(IntIdMixin, Base):
    """Table to work with the blizzard API"""

    __tablename__ = "locale"

    locales: Mapped[LocalesEnum] = mapped_column(sa.Enum(LocalesEnum), nullable=True)

    name = relationship(
        "RealmsInfo",
        back_populates="locale",
    )
