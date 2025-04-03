from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def generate_aes_key():
    """
    Generates a random 256-bit AES key.
    
    Returns:
        bytes: AES key (32 bytes)
    """
    return os.urandom(32)  # 256-bit AES key

def encrypt_data(data, aes_key):
    """
    Encrypts data using AES-256 encryption.
    
    Args:
        data (bytes): Data to encrypt.
        aes_key (bytes): 32-byte AES key.

    Returns:
        bytes: Encrypted data including IV.
    """
    iv = os.urandom(16)  # Generate a random IV (16 bytes)

    # Apply PKCS7 padding to ensure the data is a multiple of block size (16 bytes)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Encrypt the data
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return iv + encrypted_data  # Combine IV and encrypted data

def decrypt_data(encrypted_data, aes_key):
    """
    Decrypts AES-256 encrypted data.
    
    Args:
        encrypted_data (bytes): Data to decrypt (IV + Encrypted Data).
        aes_key (bytes): 32-byte AES key.

    Returns:
        bytes: Decrypted plaintext data.
    """
    iv = encrypted_data[:16]  # Extract IV
    encrypted_content = encrypted_data[16:]

    # Decrypt the data
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_content) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data
