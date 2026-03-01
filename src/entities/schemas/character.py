import datetime as dt

from pydantic import BaseModel, ConfigDict, Field


class CharacterBase(BaseModel):
    achievement_points: int | None = None


class CharacterInfo(CharacterBase):
    url: str | None = None
    character_name: str


class CharacterDTO(CharacterInfo):
    region: str
    realm: str


class CharacterUpdate(CharacterBase):
    url: str | None = None
    updated_at: dt.datetime = Field(default_factory=lambda: dt.datetime.now(dt.UTC))


class CharacterResponse(BaseModel):
    name: str = Field(alias="character_name")
    realm_name: str
    region: str
    url: str | None = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
