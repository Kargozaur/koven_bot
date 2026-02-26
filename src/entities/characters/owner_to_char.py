from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class OwnerToCharacter(Base):
    __tablename__ = "owner_to_character"

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("owner.id", ondelete="CASCADE"), nullable=False, primary_key=True
    )
    character_id: Mapped[UUID] = mapped_column(
        ForeignKey("characters.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    owner = relationship("Owner", back_populates="owner")
    char = relationship("Character", back_populates="character")

    __table_args__ = (UniqueConstraint("character_id", name="uq_character_per_raider"),)
