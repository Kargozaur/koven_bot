from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String

from . import Base, IntIdMixin


class Raider(IntIdMixin, Base):
    __tablename__ = "raider"

    raider_name: Mapped[str] = mapped_column(String(20))
    realm_id: Mapped[int] = mapped_column(
        ForeignKey("realm.id", ondelete="CASCADE"), nullable=False
    )
    is_raider: Mapped[bool] = mapped_column(default=True, server_default=text("true"))
