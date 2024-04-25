from pymongo import MongoClient

from . import config

client = MongoClient(
    f"mongodb://{config.MONGO_HOST}:{config.MONGO_PORT}"
)
db = client[config.MONGO_DB]