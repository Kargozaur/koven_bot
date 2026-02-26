from pydantic import BaseModel


class CharacterDTO(BaseModel):
    name: str
    region: str
    realm: str
