from azure.storage.blob import BlobServiceClient
from key_vault import AZURE_STORAGE_CONNECTION_STRING, AZURE_STORAGE_CONTAINER

# Initialize Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

def upload_file(filename, encrypted_data):
    blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=filename)
    blob_client.upload_blob(encrypted_data, overwrite=True)
    return blob_client.url

def download_file(filename):
    blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=filename)
    return blob_client.download_blob().readall()
