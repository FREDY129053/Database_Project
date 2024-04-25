from pydantic import BaseModel, Field
from typing import List


class Publisher(BaseModel):
    id: str = Field(..., alias='_id')
    name: str
    description: str
    photo_url: str
    site_url: str | None = None
    slug: str

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "_id": "662903ec9d64aa614182008c",
                "name": "Rockstar Games, Inc.",
                "description": "The Rockstar Games label, founded in 1998 by Sam Houser, Terry Donovan, Dan Houser, Jamie King and Gary Foreman, is a wholly-owned subsidiary of Take-Two Interactive Software and is an umbrella/label for all other studios with the Rockstar name.",
                "photo_url": "https://cdn.mobygames.com/fac5854e-bc79-11ed-bde2-02420a000179.webp",
                "site_url": "http://www.rockstargames.com/",
                "slug": "rockstar-games-inc"
              },
            }