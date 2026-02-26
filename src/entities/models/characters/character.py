import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from . import Base, UUIDIdMixin


class Character(UUIDIdMixin, Base):
    __tablename__ = "characters"

    character_name: Mapped[str] = mapped_column(String(20))
    realm_id: Mapped[int] = mapped_column(
        sa.ForeignKey("realm.id", ondelete="SET NULL"), nullable=False
    )
    realm = relationship("Realm", back_populates="character")
    character = relationship(
        "OwnerToCharacter", back_populates="char", cascade="all, delete-orphan"
    )
