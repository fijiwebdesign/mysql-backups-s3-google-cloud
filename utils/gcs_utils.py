import os
from google.cloud import storage
from google.oauth2 import service_account
import googleapiclient.discovery  # type: ignore


def upload_to_gcs(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_path)

    # Initialize a client with service account key file
    client = storage.Client.from_service_account_json(
      os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    )


    # Get the bucket
    bucket = client.bucket(bucket_name)

    # Get the blob (object)
    blob = bucket.blob(object_name)
    
    # Upload the file with progress callback
    try:
        blob.upload_from_filename(file_path)
        print(f"File uploaded successfully to GCS bucket: {bucket_name} with key: {object_name}")
    except Exception as e:
        print(f"Error uploading file to GCS: {e}")


