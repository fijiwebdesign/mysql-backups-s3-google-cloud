import os
from google.cloud import storage
from google.oauth2 import service_account
import googleapiclient.discovery  # type: ignore

def create_bucket_if_not_exists(bucket_name):
    """Create a Google Cloud Storage bucket if it does not exist."""
    
    # Initialize a client with service account key file
    client = storage.Client.from_service_account_json(
      os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    )

    # Get the bucket
    bucket = client.bucket(bucket_name)

    # Check if the bucket exists, create it if it doesn't
    if not bucket.exists():
        print(f"Bucket '{bucket_name}' does not exist. Creating...")
        try:
            client.create_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        except Exception as e:
            print(f"Error creating bucket '{bucket_name}': {e}")
            return

def upload_to_gcs(file_path, bucket_name, object_name=None):
    """Upload a file to a Google Cloud Storage bucket."""
    if object_name is None:
        object_name = os.path.basename(file_path)

    # Check if the bucket exists, create it if it doesn't
    create_bucket_if_not_exists(bucket_name)

    # Initialize a client with service account key file
    client = storage.Client.from_service_account_json(
      os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    )


    # Get the bucket
    bucket = client.bucket(bucket_name)

    # Get the blob (object)
    blob = bucket.blob(object_name)

    # Upload the file
    try:
        blob.upload_from_filename(file_path)
        print(f"File uploaded successfully to GCS bucket: {bucket_name} with key: {object_name}")
    except Exception as e:
        print(f"Error uploading file to GCS: {e}")
