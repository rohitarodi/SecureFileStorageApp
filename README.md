# Secure File Storage System using Hybrid Encryption

This project demonstrates a secure way to store and retrieve files using **AES** for fast encryption and **RSA** for secure key handling. It uses:
- **Azure Blob Storage** for storing encrypted files,
- **Azure Key Vault** for RSA key management,
- **Streamlit** for frontend,
- **Flask** for backend APIs.

## Folder Structure

```
.
├── app/
│   ├── main.py                  # Flask backend
│   ├── front.py                 # Streamlit frontend
│   ├── encryption.py            # AES encrypt/decrypt logic
│   ├── key_vault.py             # RSA key handling + secrets
│   ├── database.py              # Store encrypted AES key
│   ├── storage.py               # Azure blob helper (optional)
│   ├── swagger.yaml             # API docs
│   ├── downloads/               # Downloads folder (volume mounted)
├── Dockerfile
├── requirements.txt
├── .env                         # Secrets like key vault name, etc.
└── README.md
```

## Prerequisites

- Python 3.10+
- Azure subscription
- Azure CLI (logged in: `az login`)
- Docker installed

## Running Locally

### 1. Clone the repo and set up your virtual environment

```bash
git clone https://github.com/rohitarodi/SecureFileStorageApp
cd secure-file-storage
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Create a `.env` file in root (use the .env file only for local development)

```
AZURE_KEY_VAULT_NAME=kv-yourvault
AZURE_RSA_KEY_NAME=rsa-encryption-key
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=...
AZURE_STORAGE_CONTAINER=file-storage
COSMOS_MONGO_CONNECTION_STRING=your-mongo-uri (optional)
ENCRYPTION_KEY=optional-default-key
```

### 3. Run the Flask app

```bash
cd app
python main.py
```

### 4. Run the Streamlit frontend

In another terminal:

```bash
cd app
streamlit run front.py
```

> Open: `http://localhost:8501`

## 🐳 Docker Build & Run (Local)

### 1. Build the Docker image

```bash
docker build -t secure-file-storage-app .
```

### 2. Run with environment and volume

```bash
docker run -d -p 5000:5000 -p 8501:8501 \
  --env-file .env \
  -v "${PWD}/DownloadsFromDocker:/app/downloads" \
  --name secure-storage-container \
  secure-file-storage-app
```

### Access

- Flask: `http://localhost:5000`
- Streamlit: `http://localhost:8501`

## ☁️ Deploying to Azure Container Instance or Web App

### 1. Create an Azure Container Registry

```bash
az acr create --resource-group your-rg --name youracrname --sku Basic
az acr login --name youracrname
```

### 2. Tag and push Docker image

```bash
docker tag secure-file-storage-app youracrname.azurecr.io/secure-file-storage-app:latest
docker push youracrname.azurecr.io/secure-file-storage-app:latest
```

### 3. Deploy to Azure Web App (Container)

```bash
az appservice plan create --name your-app-plan --resource-group your-rg --is-linux
az webapp create --resource-group your-rg \
  --plan your-app-plan \
  --name your-app-name \
  --deployment-container-image-name youracrname.azurecr.io/secure-file-storage-app:latest \
  --registry-login-server youracrname.azurecr.io \
  --registry-username <acr-username> \
  --registry-password <acr-password>
```
