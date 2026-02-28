from pydantic import BaseModel, ConfigDict, Field


class CharacterDTO(BaseModel):
    name: str
    region: str
    realm: str


class CharacterResponse(BaseModel):
    name: str = Field(alias="character_name")
    realm_name: str
    region: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
