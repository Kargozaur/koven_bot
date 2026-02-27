from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class CharParamns(BaseModel):
    region: Annotated[str, Field(..., min_length=2, max_length=3)]
    realm: Annotated[str, Field(..., min_length=1)]
    name: Annotated[str, Field(..., min_length=2, max_length=12)]

    @field_validator("region")
    def normalize_region(cls, v: str) -> str:
        return v.lower()

    @field_validator("realm")
    def normalize_realm(cls, v: str) -> str:
        return v.lower().replace(" ", "-")
