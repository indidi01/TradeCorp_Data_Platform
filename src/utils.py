import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from pathlib import Path

# Configuration
load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

# Vérification
if not CONNECTION_STRING:
    raise ValueError("La variable d'environnement AZURE_STORAGE_CONNECTION_STRING n'est pas définie.")

if not CONTAINER_NAME:
    raise ValueError("La variable d'environnement AZURE_STORAGE_CONTAINER_NAME n'est pas définie.")

RAW_DATA_DIR = Path("data/raw")
CLEAN_DATA_DIR = Path("data/clean")

# Fonction
def download_from_blobstorage(blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            CONNECTION_STRING
        )

        container_client = blob_service_client.get_container_client(
            CONTAINER_NAME
        )

        blob_client = container_client.get_blob_client(blob_name)

        download_file_path = os.path.join(
            RAW_DATA_DIR,
            blob_name
        )

        os.makedirs(
            os.path.dirname(download_file_path),
            exist_ok=True
        )

        with open(download_file_path, "wb") as download_file:
            download_file.write(
                blob_client.download_blob().readall()
            )

    except Exception as e:
        print(
            f"Erreur lors du téléchargement du blob {blob_name} : {e}"
        )