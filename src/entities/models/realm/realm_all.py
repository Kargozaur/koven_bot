from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, IntIdMixin


class RealmsInfo(IntIdMixin, Base):
    __tablename__ = "realms_info"

    realm_slug_id: Mapped[int] = mapped_column(
        sa.ForeignKey("realm.id", ondelete="SET NULL")
    )
    realm_region_id: Mapped[int] = mapped_column(
        sa.ForeignKey("region.id", ondelete="SET NULL")
    )
    locale_id: Mapped[int] = mapped_column(
        sa.ForeignKey("locale.id", ondelete="SET NULL")
    )

    slug = relationship("Realm", back_populates="realm")
    region = relationship("Region", back_populates="names")
    locale = relationship("Locales", back_populates="name")
