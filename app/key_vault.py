from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

# Load Key Vault Name from environment variables or use default
KEY_VAULT_NAME = "kv-student-001"  
KV_URL = f"https://{KEY_VAULT_NAME}.vault.azure.net/"

# Authenticate using DefaultAzureCredential (Ensure you have logged in with `az login`)
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=KV_URL, credential=credential)

# Function to retrieve secrets
def get_secret(secret_name):
    retrieved_secret = secret_client.get_secret(secret_name)
    return retrieved_secret.value

# Fetch Secrets from Key Vault
AZURE_STORAGE_CONNECTION_STRING = get_secret("StorageConnectionString")  # Corrected Secret Name
AZURE_STORAGE_CONTAINER = get_secret("StorageContainer")  # Corrected Secret Name
ENCRYPTION_KEY = get_secret("EncryptionKey")  # Corrected Secret Name
COSMOS_MONGO_CONNECTION_STRING = get_secret("CosmosDBConnectionString")  # Corrected Secret Name

# Print for debugging
print(f"✅ Storage Connection String Retrieved: {AZURE_STORAGE_CONNECTION_STRING[:10]}****")
print(f"✅ Storage Container: {AZURE_STORAGE_CONTAINER}")
print(f"✅ Encryption Key Retrieved: {ENCRYPTION_KEY[:10]}****")
print(f"✅ CosmosDB Connection Retrieved: {COSMOS_MONGO_CONNECTION_STRING[:10]}****")
