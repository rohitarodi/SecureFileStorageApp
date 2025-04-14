from pymongo import MongoClient
from key_vault import COSMOS_MONGO_CONNECTION_STRING
import base64
import os

# COSMOS_MONGO_CONNECTION_STRING = os.getenv("COSMOS_MONGO_CONNECTION_STRING")
client = MongoClient(COSMOS_MONGO_CONNECTION_STRING)
db = client.secure_storage
aes_keys_collection = db.aes_keys


def store_encrypted_key(filename, encrypted_key):
    encoded_key = base64.b64encode(encrypted_key).decode('utf-8')
    aes_keys_collection.update_one(
        {"filename": filename},
        {"$set": {"encrypted_key": encoded_key}},
        upsert=True
    )


def get_encrypted_key(filename):
    record = aes_keys_collection.find_one({"filename": filename})
    if record and "encrypted_key" in record:
        return base64.b64decode(record["encrypted_key"])
    return None