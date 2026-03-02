import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from . import Base, CreatedAtMixin, IsDeletedMixin, UpdatedAtMixin, UUIDIdMixin


class Character(UUIDIdMixin, CreatedAtMixin, UpdatedAtMixin, IsDeletedMixin, Base):
    __tablename__ = "characters"

    character_name: Mapped[str] = mapped_column(String(20))
    realm_id: Mapped[int] = mapped_column(
        sa.ForeignKey("realm.id", ondelete="SET NULL"), nullable=False
    )
    url: Mapped[str] = mapped_column(sa.String(2048), nullable=True)
    achievement_points: Mapped[int] = mapped_column(nullable=True)

    realm = relationship("Realm", back_populates="character")
    character = relationship(
        "OwnerToCharacter", back_populates="char", cascade="all, delete-orphan"
    )
