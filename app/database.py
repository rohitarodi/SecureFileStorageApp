from pymongo import MongoClient
from key_vault import COSMOS_MONGO_CONNECTION_STRING
import base64
from bson.binary import Binary
import os

# COSMOS_MONGO_CONNECTION_STRING = os.getenv("COSMOS_MONGO_CONNECTION_STRING")
client = MongoClient(COSMOS_MONGO_CONNECTION_STRING)
db = client.secure_storage
aes_keys_collection = db.aes_keys


def store_encrypted_key(filename, encrypted_key):
    aes_keys_collection.update_one(
        {"filename": filename},
        {"$set": {"encrypted_key": Binary(encrypted_key)}},
        upsert=True
    )


def get_encrypted_key(filename):
    record = aes_keys_collection.find_one({"filename": filename})
    if record and "encrypted_key" in record:
        return record["encrypted_key"]  # Already bytes
    return None