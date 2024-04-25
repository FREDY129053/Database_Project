from fastapi import APIRouter, HTTPException
from typing import List
from async_lru import alru_cache

from .db_client import db
from .models.game import Game
from .models.publisher import Publisher

router = APIRouter(prefix='/game_info')


@router.get('', response_model=List[Game])
@alru_cache
async def get_all_games():
    games = list(db.game_info.find({}))

    for game in games:
        game["_id"] = str(game["_id"])

    return games


@router.get('/publishers', response_model=List[Publisher])
@alru_cache
async def get_all_publishers():
    publishers = list(db.publisher_info.find({}))

    if not publishers:
        raise HTTPException(status_code=404, detail="WTF")

    for publisher in publishers:
        publisher["_id"] = str(publisher["_id"])

    return publishers


@router.get('/{game_slug}', response_model=Game)
async def get_game_by_slug(game_slug: str):
    game = db.game_info.find_one({"slug": game_slug})

    if not game:
        raise HTTPException(status_code=404, detail="Game Not Found")

    game["_id"] = str(game["_id"])

    return game



@router.get('/publishers/{publisher_slug}', response_model=Publisher)
async def get_publisher_by_slug(publisher_slug: str):
    publisher = db.publisher_info.find_one({"slug": publisher_slug})

    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher Not Found")

    publisher["_id"] = str(publisher["_id"])

    return publisher
