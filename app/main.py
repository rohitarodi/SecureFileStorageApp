from flask import Flask, request, jsonify, send_file
from flasgger import Swagger
from azure.storage.blob import BlobServiceClient
from encryption import encrypt_data, decrypt_data
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
swagger = Swagger(app, template_file="swagger.yaml")  # Load API spec from external file

# Azure Blob Storage Configuration
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")

# Initialize Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

# def upload_file_to_blob(file_path):
#     """
#     Uploads a file to Azure Blob Storage.
    
#     :param file_path: Path to the file to be uploaded.
#     """
#     try:
#         # Get file name
#         filename = os.path.basename(file_path)

#         # Get blob client
#         blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=filename)

#         print(f"🔹 Uploading {filename} to Azure Blob Storage...")

#         # Upload file
#         with open(file_path, "rb") as file:
#             blob_client.upload_blob(file, overwrite=True)

#         print(f"✅ Upload successful: {filename}")

#     except Exception as e:
#         print(f"❌ Upload failed: {str(e)}")
# Test the function
# file_to_upload = "testfile.txt"  # Change this to your actual file
# upload_file_to_blob(file_to_upload)

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Uploads an encrypted file to Azure Blob Storage.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        print(f"🔹 Received file: {file.filename}")

        encrypted_data = encrypt_data(file.read())  # Encrypt file data

        print("✅ Encryption successful")

        # Get blob client
        blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=file.filename)

        print(f"🔹 Uploading encrypted file to Blob Storage: {blob_client.url}")

        # Upload encrypted file
        blob_client.upload_blob(encrypted_data, overwrite=True)

        print(f"✅ Upload successful: {file.filename}")

        return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200

    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/download', methods=['GET'])
def download_file():
    """
    Downloads and decrypts a file from Azure Blob Storage.
    ---
    tags:
      - File Download
    parameters:
      - name: filename
        in: query
        type: string
        required: true
        description: Name of the file to download
    responses:
      200:
        description: Decrypted file content
        content:
          application/octet-stream:
            schema:
              type: string
              format: binary
      400:
        description: Missing filename parameter
      404:
        description: File not found
      500:
        description: Internal server error
    """
    filename = request.args.get('filename')

    if not filename:
        return jsonify({"error": "Filename parameter is required"}), 400

    try:
        # Get blob client
        blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=filename)

        # Download encrypted file
        stream = blob_client.download_blob()
        encrypted_data = stream.readall()

        # Decrypt file data
        decrypted_data = decrypt_data(encrypted_data)

        # Return decrypted file as response
        return decrypted_data, 200, {'Content-Type': 'application/octet-stream',
                                     'Content-Disposition': f'attachment; filename="{filename}"'}

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
        schema:
          type: object
          properties:
            message:
              type: string
              example: "File saved at downloads/example.txt"
      400:
        description: Missing filename parameter
      404:
        description: File not found
      500:
        description: Internal server error
    """
    filename = request.args.get('filename')

    if not filename:
        return jsonify({"error": "Filename parameter is required"}), 400

    try:
        # Get blob client
        blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=filename)

        # Download encrypted file
        stream = blob_client.download_blob()
        encrypted_data = stream.readall()

        # Decrypt file data
        decrypted_data = decrypt_data(encrypted_data)

        # Save the decrypted file on the server
        save_folder = "downloads"
        os.makedirs(save_folder, exist_ok=True)  # Ensure directory exists
        save_path = os.path.join(save_folder, filename)

        with open(save_path, "wb") as file:
            file.write(decrypted_data)

        return jsonify({"message": f"File saved at {save_path}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
