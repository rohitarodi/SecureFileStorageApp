from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm
from azure.keyvault.secrets import SecretClient
import os

# Load Key Vault Name from environment variables or use default
KEY_VAULT_NAME = "kv-student-001"  
KV_URL = f"https://{KEY_VAULT_NAME}.vault.azure.net/"

# Authenticate using DefaultAzureCredential (Ensure you have logged in with `az login`)
credential = DefaultAzureCredential()

# Initialize Clients
key_name = "rsa-key-FileStorageSystem"
crypto_client = CryptographyClient(f"{KV_URL}/keys/{key_name}", credential)
secret_client = SecretClient(vault_url=KV_URL, credential=credential)

# Function to retrieve secrets
def get_secret(secret_name):
    retrieved_secret = secret_client.get_secret(secret_name)
    return retrieved_secret.value

def encrypt_aes_key(aes_key):
    """Encrypts AES key using RSA from Azure Key Vault"""
    encrypted_aes_key = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, aes_key).ciphertext
    return encrypted_aes_key

def decrypt_aes_key(encrypted_aes_key):
    """Decrypts AES key using RSA from Azure Key Vault"""
    decrypted_aes_key = crypto_client.decrypt(EncryptionAlgorithm.rsa_oaep, encrypted_aes_key).plaintext
    return decrypted_aes_key

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