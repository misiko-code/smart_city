from pymongo import MongoClient, collection
import config

def init_buildingsdb(collection_name: str) -> collection.Collection:
    """Fetches the collection from the MongoDB database specified in config.py."""
    try:
        client = MongoClient(config.MONGO_ADDRESS)
        db = client[config.MONGO_DB_NAME]  # Database name
        collection = db[collection_name]  # Collection name
        return collection
    except Exception as e:
        print(f"Error: {e}")

def init_sensorsdb(collection_name: str) -> collection.Collection:
    """Fetches the collection from the MongoDB database specified in config.py."""
    try:
        client = MongoClient(config.MONGO_ADDRESS)
        db = client[config.MONGO_DB_NAME]  # Database name
        collection = db[collection_name]  # Collection name
        return collection
    except Exception as e:
        print(f"Error: {e}")