import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

# ✅ Load environment variables
load_dotenv()

# 🔐 Fetch Key Vault name from .env
AZURE_KEY_VAULT_NAME = os.getenv("AZURE_KEY_VAULT_NAME")
RSA_KEY_NAME = os.getenv("AZURE_RSA_KEY_NAME")

if not AZURE_KEY_VAULT_NAME:
    raise ValueError("❌ AZURE_KEY_VAULT_NAME is missing from environment variables!")
if not RSA_KEY_NAME:
    raise ValueError("❌ AZURE_RSA_KEY_NAME is missing from environment variables!")

# 🔑 Setup Key Vault clients
key_vault_url = f"https://{AZURE_KEY_VAULT_NAME}.vault.azure.net"
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
crypto_client = CryptographyClient(key_vault_url + "/keys/" + RSA_KEY_NAME, credential)

# 📥 Retrieve secrets from Azure Key Vault
AZURE_STORAGE_CONNECTION_STRING = secret_client.get_secret("StorageConnectionString").value
AZURE_STORAGE_CONTAINER = secret_client.get_secret("StorageContainer").value
COSMOS_MONGO_CONNECTION_STRING = secret_client.get_secret("CosmosDBConnectionString").value
ENCRYPTION_KEY = secret_client.get_secret("EncryptionKey").value

# 🔐 Hybrid Encryption methods
def encrypt_aes_key(aes_key: bytes) -> bytes:
    result = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, aes_key)
    return result.ciphertext

def decrypt_aes_key(encrypted_key: bytes) -> bytes:
    result = crypto_client.decrypt(EncryptionAlgorithm.rsa_oaep, encrypted_key)
    return result.plaintext
