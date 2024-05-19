from fastapi import APIRouter, HTTPException, Query
from typing import List

from .db_client import db
from .models.game import Game
from .models.publisher import Publisher

router = APIRouter(prefix='/game_info')


@router.get('/')
async def get_all_games(page: int = Query(1, gt=0),
                        size: int = Query(30, gt=0),
                        genres: List[str] = Query(None),
                        platforms: List[str] = Query(None),
                        sort: str = Query(None)):
    offset = (page - 1) * size
    query = {}
    sort_by = {}
    if genres:
        query['genres'] = {'$all': genres}
    if platforms:
        query['platforms'] = {'$all': platforms}
    if sort:
        if sort.lower() == 'date':
            sort_by['date.year'] = -1
        elif sort.lower() == 'rating':
            sort_by['score'] = -1

    games = db.game_info.find(query)

    if sort_by:
        games = games.sort(list(sort_by.items()))

    games = list(games.skip(offset).limit(size))
    # games = list(db.game_info.find(query).skip(offset).limit(size))

    for game in games:
        game["_id"] = str(game["_id"])

    total_games = db.game_info.count_documents(query)
    total_pages = total_games // size + 1

    result = {
        "games": games,
        "info": {
            "page": page,
            "size": len(games),
            "total_pages": total_pages
        }
    }

    return result


@router.get('/publishers', response_model=List[Publisher])
async def get_all_publishers():
    publishers = list(db.publisher_info.find({}))

    if not publishers:
        raise HTTPException(status_code=404, detail="WTF")

    for publisher in publishers:
        publisher["_id"] = str(publisher["_id"])

    return publishers


@router.get('/filters')
async def get_all_filters():
    filters = {}
    genres = list(db.game_info.distinct("genres"))
    platforms = list(db.game_info.distinct("platforms"))
    filters['genres'], filters['platforms'] = genres, platforms

    return filters


@router.get('/{game_slug}')
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


@router.get('/search/{name}')
async def get_info_by_name(name: str):
    query = {}
    if name:
        query['name'] = {'$regex': name, '$options': 'i'}

    all_info = list(db.game_info.find(query).limit(10))
    for info in all_info:
        info["_id"] = str(info["_id"])

    return all_info


@router.get('/publishers/{publisher_slug}/all_games')
async def get_all_games_of_publisher(publisher_slug: str):
    query = {
        "publishers": {
            "$elemMatch": {
                "name": {"$regex": ".*", "$options": "i"},
                "slug": publisher_slug
            }
        }
    }
    all_games = list(db.game_info.find(query))

    if not all_games:
        raise HTTPException(status_code=404, detail="Games Not Found")

    for game in all_games:
        game["_id"] = str(game["_id"])

    return all_games
