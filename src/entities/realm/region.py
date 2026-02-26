import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.enums.region_enum import RegionEnum

from . import Base, IntIdMixin


class Region(IntIdMixin, Base):
    __tablename__ = "region"

    region: Mapped[RegionEnum] = mapped_column(sa.Enum(RegionEnum), unique=True)
    names = relationship("RealmsInfo", back_populates="region")
