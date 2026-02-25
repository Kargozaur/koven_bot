from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from . import Base, IdMixin


class Owner(IdMixin[int], Base):
    __tablename__ = "owner"

    discord_id: Mapped[int] = mapped_column(BigInteger, index=True)
