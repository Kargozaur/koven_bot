from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, IsDeletedMixin, UUIDIdMixin


class Owner(UUIDIdMixin, IsDeletedMixin, Base):
    __tablename__ = "owner"

    discord_id: Mapped[int] = mapped_column(BigInteger, index=True)

    owner = relationship(
        "OwnerToCharacter", cascade="all, delete-orphan", back_populates="owner"
    )
