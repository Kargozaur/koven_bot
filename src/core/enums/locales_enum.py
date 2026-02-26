from enum import StrEnum

from .region_enum import RegionEnum


class LocalesEnum(StrEnum):
    EN_US = "en_US"
    RU_RU = "ru_RU"
    EN_EN = "en_EN"


REGION_LOCALE_MAP = {
    RegionEnum.EU: {LocalesEnum.EN_EN, LocalesEnum.RU_RU},
    RegionEnum.NA: {LocalesEnum.EN_US},
}
