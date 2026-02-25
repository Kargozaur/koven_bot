from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from . import Base, IntIdMixin


class Owner(IntIdMixin, Base):
    __tablename__ = "owner"

    discord_id: Mapped[int] = mapped_column(BigInteger, index=True)
