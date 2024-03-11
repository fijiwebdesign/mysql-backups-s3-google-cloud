import os
from google.cloud import storage
from google.oauth2 import service_account
import googleapiclient.discovery  # type: ignore
import json

def initialize_gcs_client():
  
    # Check if service account key info is provided as a JSON String
    key_info_dict = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if key_info_dict:
        # Initialize a client with service account key info from dictionary
        client = storage.Client.from_service_account_info(
          json.loads(key_info_dict)
        )
        return client
    
    # Check if service account key file path is provided
    key_file_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if key_file_path:
        # Initialize a client with service account key file
        client = storage.Client.from_service_account_json(key_file_path)
        return client
    
    # Handle the case when neither dictionary nor file path is provided
    raise ValueError("Environment variables not set for service account key information")

def create_bucket_if_not_exists(bucket_name):
    """Create a Google Cloud Storage bucket if it does not exist."""
    
    client = initialize_gcs_client()

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

    client = initialize_gcs_client()


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
