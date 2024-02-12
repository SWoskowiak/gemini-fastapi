"""Simple Google Cloud Storage client to upload files to a bucket."""
import logging
import time
import os
from google.cloud import storage
from fastapi import UploadFile

logger = logging.getLogger(__name__)

# We are just using a single bucket for this project so just grab the name from the environment.
bucket_name = os.environ["BUCKET_NAME"]

async def upload_file(file: UploadFile) -> str:
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    # Append a unix timestamp to the filename to make it unique
    blob_name = f"{int(time.time())}_{file.filename}"
    blob = bucket.blob(blob_name)

    data = await file.read()
    blob.upload_from_file(data)

    logger.info("File %s uploaded to %s.", file.filename, bucket_name)

    return blob_name

async def upload_file_bytestream(file_data: bytes, filename: str) -> str:
    """Uploads a file to the bucket using a byte stream."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    # Append a unix timestamp to the filename to make it unique
    blob_name = f"{int(time.time())}_{filename}"
    blob = bucket.blob(blob_name)

    blob.upload_from_string(file_data)

    logger.info("File %s uploaded to %s.", filename, bucket_name)

    return blob_name

def download_file(blob_name: str) -> bytes:
    """Downloads a blob from the bucket and returns it as bytes."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    file_data = blob.download_as_bytes()

    return file_data
