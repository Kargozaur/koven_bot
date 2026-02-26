import re

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
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
    def _generate_candidate(name: str, attempt: int) -> str:
        """method accepts either cyrillic or latinic realm names"""
        clean: str = re.sub(r"[^a-zA-Zа-яА-ЯёЁ\s]", "", name).strip()
        words: list[str] = clean.split()

        if not words:
            return f"UN{attempt}"

        if len(words) >= 2:
            return (words[0][0] + words[1][:attempt]).upper()
        else:
            return words[0][: attempt + 1].upper()

    @classmethod
    async def sync_realms(
        cls, session: AsyncSession, incoming_names: list[str]
    ) -> list:
        query = sa.select(cls.realm_name, cls.realm_short_name)
        result = await session.execute(query)
        rows = result.all()

        existing_names = {r.realm_name for r in rows}
        used_shorts = {r.realm_short_name for r in rows}

        new_objects = []

        for full_name in dict.fromkeys(incoming_names):
            if not full_name or full_name in existing_names:
                continue

            attempt = 1
            while True:
                candidate: str = cls._generate_candidate(full_name, attempt)

                if candidate not in used_shorts:
                    new_realm = cls(name=full_name, short_name=candidate)
                    new_objects.append(new_realm)
                    used_shorts.add(candidate)
                    break

                attempt += 1
                if attempt > 3:
                    candidate = f"{candidate[:2]}{len(used_shorts)}"
                    used_shorts.add(candidate)
                    new_objects.append(cls(name=full_name, short_name=candidate))
                    break

        if new_objects:
            session.add_all(new_objects)
            await session.commit()

        return new_objects
