import os
import boto3

def create_s3_client():
    s3 = boto3.client('s3',
                      endpoint_url=os.environ.get('S3_ENDPOINT_URL'),
                      aws_access_key_id=os.environ.get('S3_ACCESS_KEY'),
                      aws_secret_access_key=os.environ.get('S3_SECRET_KEY'),
                      region_name=os.environ.get('S3_REGION')
                      )
    return s3

def create_bucket_if_not_exist(bucket_name, s3_client):
    try:
        # Check if the bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} already exists")
    except s3_client.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            # Bucket does not exist, create it
            try:
                s3_client.create_bucket(Bucket=bucket_name)
                print(f"Bucket {bucket_name} created successfully")
            except Exception as e:
                print(f"Error creating bucket {bucket_name}: {e}")
        else:
            print(f"Error checking bucket {bucket_name}: {e}")

def upload_to_s3(file_path, bucket_name, object_name=None, progress_callback=None):
    if object_name is None:
        object_name = os.path.basename(file_path)
    else:
        # Ensure that object_name is a string
        object_name = str(object_name)

    # Log Boto3 client parameters
    print("Creating S3 client with the following parameters:")
    print(f"  Endpoint URL: {os.environ.get('S3_ENDPOINT_URL')}")
    print(f"  Access key ID: {os.environ.get('S3_ACCESS_KEY')}")
    print(f"  Secret access key: {'*****' if os.environ.get('S3_SECRET_KEY') else 'None (using IAM credentials)'}")
    print(f"  Region name: {os.environ.get('S3_REGION')}")

    # Create the S3 client
    s3_client = create_s3_client()

    # Create the bucket if it doesn't exist
    create_bucket_if_not_exist(bucket_name, s3_client)

    # Upload the file
    try:
        # Use the progress callback if provided
        extra_args = {'Callback': progress_callback} if progress_callback else {}
        response = s3_client.upload_file(file_path, bucket_name, object_name, ExtraArgs=extra_args)
        print(f"File uploaded successfully to S3 bucket: {bucket_name} with key: {object_name}")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
