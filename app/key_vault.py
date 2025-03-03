from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

key_vault_name = "securevault"
key_name = "rsa-encryption-key"

credential = DefaultAzureCredential()
crypto_client = CryptographyClient(f"https://{key_vault_name}.vault.azure.net/keys/{key_name}", credential)

def encrypt_aes_key(aes_key):
    encrypted_aes_key = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, aes_key).ciphertext
    return encrypted_aes_key

def decrypt_aes_key(encrypted_aes_key):
    decrypted_aes_key = crypto_client.decrypt(EncryptionAlgorithm.rsa_oaep, encrypted_aes_key).plaintext
    return decrypted_aes_key
