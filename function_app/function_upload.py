import azure.functions as func
from flask import jsonify
from storage import upload_file
from encryption import encrypt_file
from key_vault import encrypt_aes_key
from database import save_file_metadata

def main(req: func.HttpRequest) -> func.HttpResponse:
    file = req.files['file']
    encrypted_data, aes_key, iv = encrypt_file(file.read())  # Encrypt file
    encrypted_aes_key = encrypt_aes_key(aes_key)  # Encrypt AES key using RSA
    file_url = upload_file(file.filename, encrypted_data)  # Upload to Blob Storage
    save_file_metadata(file.filename, file_url, encrypted_aes_key)  # Save metadata in DB
    return func.HttpResponse(jsonify({"message": "File uploaded successfully", "file_url": file_url}))
