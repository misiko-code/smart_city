from pymongo import MongoClient, collection
import config

def init_buildingsdb(collection_name: str) -> collection.Collection:
    """Fetches the collection from the MongoDB database specified in config.py."""
    try:
        client = MongoClient(config.MONGO_ADDRESS)  # MongoDB connection string
        db = client[config.MONGO_DB_BNAME]  # Database name
        collection_buildings = db[collection_name]  # Collection name
        return collection_buildings
    except Exception as e:
        print(f"Error: {e}")

def init_sensorsdb(collection_name: str) -> collection.Collection:
    """Fetches the collection from the MongoDB database specified in config.py."""
    try:
        client = MongoClient(config.MONGO_ADDRESS)  # MongoDB connection string
        db = client[config.MONGO_DB_SNAME]  # Database name
        collection_sensors = db[collection_name]  # Collection name
        return collection_sensors
    except Exception as e:
        print(f"Error: {e}")

def init_sensor_datadb(collection_name: str) -> collection.Collection:
    """Fetches the collection from the MongoDB database specified in config.py."""
    try:
        client = MongoClient(config.MONGO_ADDRESS)  # MongoDB connection string
        db = client[config.MONGO_DB_CNAME]  # Database name
        collection_sensor_data = db[collection_name]  # Collection name
        return collection_sensor_data
    except Exception as e:
        print(f"Error: {e}")
