import azure.functions as func
from storage import download_file
from key_vault import decrypt_aes_key
from database import get_file_metadata
from encryption import decrypt_file

def main(req: func.HttpRequest) -> func.HttpResponse:
    filename = req.params.get("filename")
    file_metadata = get_file_metadata(filename)
    encrypted_data = download_file(file_metadata["file_url"])
    aes_key = decrypt_aes_key(file_metadata["encrypted_aes_key"])
    decrypted_data = decrypt_file(encrypted_data, aes_key)
    return func.HttpResponse(decrypted_data, mimetype='application/octet-stream')
