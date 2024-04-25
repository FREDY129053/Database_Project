from pydantic import BaseModel, Field
from typing import List, Dict, Any, Union


class Game(BaseModel):
    id: str = Field(..., alias='_id')
    name: str
    description: str
    platforms: List[str]
    score: int | None = None
    genres: List[str]
    date: Dict[str, Any]
    publishers: List[str]
    age: Union[int, str]
    playtime: int | None = None
    preview_photo: str
    photos: List[str]
    slug: str

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "6629025a9d64aa6141820085",
                "name": "Grand Theft Auto V",
                "description": "Rockstar Games went bigger, since their previous installment of the series.",
                "platforms": [
                    "PC",
                    "Playstation 5",
                    "Xbox Series X/S",
                    "Xbox 360"
                ],
                "score": 92,
                "genres": [
                    "Action",
                    "Adventure"
                ],
                "date": {
                    "day": 23,
                    "month": "Sep",
                    "year": 2013
                },
                "publishers": [
                    "Rockstar Games"
                ],
                "age": 17,
                "playtime": 74,
                "preview_photo": "https://media.rawg.io/media/crop/600/400/games/20a/20aa03a10cda45239fe22d035c0ebe64.jpg",
                "photos": [
                    "https://media.rawg.io/media/resize/200/-/screenshots/a7c/a7c43871a54bed6573a6a429451564ef.jpg",
                    "https://media.rawg.io/media/resize/200/-/screenshots/f95/f9518b1d99210c0cae21fc09e95b4e31.jpg",
                    "https://media.rawg.io/media/resize/200/-/screenshots/592/592e2501d8734b802b2a34fee2df59fa.jpg"
                ],
                "slug": "grand-theft-auto-v"
            }
        }