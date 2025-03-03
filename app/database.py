from pymongo import MongoClient
import os

# Load connection string from environment variables
MONGO_CONNECTION_STRING = os.getenv("mongodb+srv://arodirohit:arodirohit0207@cosmos-student-dev.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000")
DATABASE_NAME = "FileStorageDB"
COLLECTION_NAME = "file_metadata"

# Connect to Cosmos DB (MongoDB API)
client = MongoClient(MONGO_CONNECTION_STRING)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Function to store file metadata in MongoDB
def save_file_metadata(filename, file_url, encrypted_aes_key):
    file_entry = {
        "filename": filename,
        "file_url": file_url,
        "encrypted_aes_key": encrypted_aes_key.hex(),
    }
    collection.insert_one(file_entry)
    print(f"File metadata saved for {filename}")

# Function to retrieve file metadata from MongoDB
def get_file_metadata(filename):
    file_entry = collection.find_one({"filename": filename})
    if file_entry:
        return {
            "file_url": file_entry["file_url"],
            "encrypted_aes_key": bytes.fromhex(file_entry["encrypted_aes_key"]),
        }
    return None
