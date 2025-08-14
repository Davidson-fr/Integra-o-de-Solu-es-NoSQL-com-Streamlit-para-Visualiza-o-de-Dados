import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
MONGO_DB = os.getenv("MONGO_DB", "eshop")
DEFAULT_COLLECTION = os.getenv("DEFAULT_COLLECTION", "customers")

_client = None

def get_client():
    global _client
    if _client is None:
        _client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return _client

def get_db():
    return get_client()[MONGO_DB]

def get_collection(name: str | None = None):
    if not name:
        name = DEFAULT_COLLECTION
    return get_db()[name]

def ensure_indexes(col):
    # Índices úteis para consultas
    col.create_index("email", unique=False, background=True)
    col.create_index("city", background=True)
    col.create_index("created_at", background=True)
