import re

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, IntIdMixin


class Realm(IntIdMixin, Base):
    __tablename__ = "realm"

    realm_name: Mapped[str] = mapped_column(
        sa.String(18), nullable=False, unique=True
    )  # Defias Brotherhood is the longest name for a realm = 18 characters
    realm_short_name: Mapped[str] = mapped_column(
        sa.String(12), nullable=False, unique=True
    )
    realm = relationship("RealmsInfo", back_populates="slug")
    character = relationship("Character", back_populates="realm")

    @staticmethod
    def _generate_candidate(name: str, attempt: int = 1) -> str:
        """method accepts either cyrillic or latinic realm names"""
        clean: str = re.sub(r"[^a-zA-Zа-яА-ЯёЁ\s]", "", name).strip()
        words: list[str] = clean.split()

        if not words:
            return f"UN{attempt}"

        if len(words) >= 2:
            return (words[0][0] + words[1][:attempt]).upper()
        else:
            return words[0][: attempt + 1].upper()
