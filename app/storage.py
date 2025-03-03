from azure.storage.blob import BlobServiceClient

blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=stgsustudentdata001;AccountKey=WNm4ZCLuS/ut7pf/5vO3bDVTEdKh5dvrastyVbEQUGiNBcVP70D1S/Nnl0VXSIRnfpTZYYedF9di+AStzSzE2A==;EndpointSuffix=core.windows.net")
container_name = "encrypted-files"

def upload_file(filename, encrypted_data):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    blob_client.upload_blob(encrypted_data)
    return blob_client.url

def download_file(file_url):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_url.split('/')[-1])
    return blob_client.download_blob().readall()
