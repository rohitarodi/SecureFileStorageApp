# from pymongo import MongoClient
# import os

# Load connection string from environment variables
# MONGO_CONNECTION_STRING = os.getenv("mongodb+srv://arodirohit:arodirohit0207@cosmos-student-dev.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000")
# DATABASE_NAME = "FileStorageDB"
# COLLECTION_NAME = "file_metadata"

# # Connect to Cosmos DB (MongoDB API)
# client = MongoClient(MONGO_CONNECTION_STRING)
# db = client[DATABASE_NAME]
# collection = db[COLLECTION_NAME]

# # Function to store file metadata in MongoDB
# def save_file_metadata(filename, file_url, encrypted_aes_key):
#     file_entry = {
#         "filename": filename,
#         "file_url": file_url,
#         "encrypted_aes_key": encrypted_aes_key.hex(),
#     }
#     collection.insert_one(file_entry)
#     print(f"File metadata saved for {filename}")

# # Function to retrieve file metadata from MongoDB
# def get_file_metadata(filename):
#     file_entry = collection.find_one({"filename": filename})
#     if file_entry:
#         return {
#             "file_url": file_entry["file_url"],
#             "encrypted_aes_key": bytes.fromhex(file_entry["encrypted_aes_key"]),
#         }
#     return None

from pymongo import MongoClient
from key_vault import COSMOS_MONGO_CONNECTION_STRING
import os

# Load CosmosDB connection string from environment or Key Vault
# COSMOS_MONGO_CONNECTION_STRING = os.getenv("COSMOS_MONGO_CONNECTION_STRING")

# Initialize MongoDB Client
client = MongoClient(COSMOS_MONGO_CONNECTION_STRING)
db = client["FileStorageDB"]  # Database name
keys_collection = db["encrypted_keys"]  # Collection for storing AES keys

def store_encrypted_key(file_name, encrypted_aes_key):
    """
    Stores an encrypted AES key in CosmosDB (MongoDB API).
    
    Args:
        file_name (str): The name of the file.
        encrypted_aes_key (bytes): The AES key encrypted with RSA.
    
    Returns:
        dict: MongoDB response.
    """
    key_data = {
        "file_name": file_name,
        "encrypted_aes_key": encrypted_aes_key.hex()  # Store as a hex string
    }
    result = keys_collection.insert_one(key_data)
    return result.inserted_id

def retrieve_encrypted_key(file_name):
    """
    Retrieves the encrypted AES key from CosmosDB.
    
    Args:
        file_name (str): The name of the file.

    Returns:
        bytes: Encrypted AES key.
    """
    key_data = keys_collection.find_one({"file_name": file_name})
    if key_data:
        return bytes.fromhex(key_data["encrypted_aes_key"])
    return None

