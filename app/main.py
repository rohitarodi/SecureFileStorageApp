# main.py
from flask import Flask, request, jsonify
from flasgger import Swagger
from azure.storage.blob import BlobServiceClient
from encryption import encrypt_data, decrypt_data, generate_aes_key
from key_vault import AZURE_STORAGE_CONNECTION_STRING, AZURE_STORAGE_CONTAINER, encrypt_aes_key, decrypt_aes_key
from database import store_encrypted_key, get_encrypted_key
import os, re

app = Flask(__name__)
swagger = Swagger(app)

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Uploads an encrypted file to Azure Blob Storage.
    ---
    tags:
      - File Upload
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The file to be uploaded
    responses:
      200:
        description: File uploaded successfully
      400:
        description: Bad Request
      500:
        description: Internal Server Error
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        sanitized_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', file.filename.strip().replace('"', ''))
        aes_key = generate_aes_key()
        encrypted_data = encrypt_data(file.read(), aes_key)
        encrypted_aes_key = encrypt_aes_key(aes_key)
        store_encrypted_key(sanitized_filename, encrypted_aes_key)

        blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=sanitized_filename)
        blob_client.upload_blob(encrypted_data, overwrite=True)

        return jsonify({"message": "File uploaded successfully", "filename": sanitized_filename}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download_save', methods=['GET'])
def download_file_save():
    """
    Downloads, decrypts, and saves a file on the server.
    ---
    tags:
      - File Download & Save
    parameters:
      - name: filename
        in: query
        type: string
        required: true
        description: Name of the file to download and save
    responses:
      200:
        description: File saved successfully on the server
      400:
        description: Missing filename parameter
      500:
        description: Internal server error
    """
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "Filename parameter is required"}), 400

    try:
        blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=filename)
        stream = blob_client.download_blob()
        encrypted_data = stream.readall()

        encrypted_aes_key = get_encrypted_key(filename)
        aes_key = decrypt_aes_key(encrypted_aes_key)
        decrypted_data = decrypt_data(encrypted_data, aes_key)

        save_folder = "A:\\Masters\\SEM 2\\Cryptography\\Project\\Files"
        # save_folder = "downloads"
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, filename)

        with open(save_path, "wb") as file:
            file.write(decrypted_data)

        return jsonify({"message": f"File saved at {save_path}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
  
@app.route('/list_files', methods=['GET'])
def list_files():
    """
    Lists all files available in Azure Blob Storage.
    ---
    tags:
      - File Listing
    responses:
      200:
        description: A list of filenames
        schema:
          type: object
          properties:
            files:
              type: array
              items:
                type: string
              example: ["file1.pdf", "file2.docx"]
      500:
        description: Internal server error
    """
    try:
        container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER)
        blob_list = container_client.list_blobs()

        filenames = [blob.name for blob in blob_list]
        return jsonify({"files": filenames}), 200

    except Exception as e:
        print(f"❌ Error listing files: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
