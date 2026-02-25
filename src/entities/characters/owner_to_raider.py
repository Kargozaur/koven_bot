from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class OwnerToRaider(Base):
    __tablename__ = "owner_to_raider"

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("owner.id", ondelete="CASCADE"), nullable=False
    )
    character_id: Mapped[int] = mapped_column(
        ForeignKey("raider.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    __table_args__ = (UniqueConstraint("character_id", name="uq_character_per_raider"),)
