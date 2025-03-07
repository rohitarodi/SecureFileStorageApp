from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import base64
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

# Load a 32-byte encryption key from the environment
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# Ensure the key is valid
if not ENCRYPTION_KEY:
    raise ValueError("Missing ENCRYPTION_KEY in environment variables")

# Convert base64 key to bytes
ENCRYPTION_KEY = base64.b64decode(ENCRYPTION_KEY)

def encrypt_data(data):
    """
    Encrypts the given data using AES encryption (CBC mode).
    Returns the IV prepended to the encrypted data.
    """
    iv = os.urandom(16)  # Generate a random IV
    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad data to be a multiple of 16 bytes
    padding_length = 16 - (len(data) % 16)
    data += bytes([padding_length]) * padding_length

    encrypted_data = encryptor.update(data) + encryptor.finalize()
    return iv + encrypted_data  # Prepend IV to the encrypted data

def decrypt_data(encrypted_data):
    """
    Decrypts AES-encrypted data.
    Expects IV (16 bytes) to be prepended to the data.
    """
    iv = encrypted_data[:16]  # Extract IV
    encrypted_content = encrypted_data[16:]  # Extract encrypted content

    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_content) + decryptor.finalize()

    # Remove padding
    padding_length = decrypted_data[-1]
    return decrypted_data[:-padding_length]
