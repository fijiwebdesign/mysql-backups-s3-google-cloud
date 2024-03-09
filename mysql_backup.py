#!/usr/bin/env python3

import os
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from utils.mysql_utils import mysqldump_from_url
from utils.s3_utils import upload_to_s3
from utils.gcs_utils import upload_to_gcs
from datetime import datetime
from utils.resend_utils import resend_send_email

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get database URL from environment variable
    db_url = os.getenv('DATABASE_URL')

    if db_url:
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Get output file name from environment variable or default to "backup.sql"
        output_file = os.getenv('BACKUP_FILE', f"/tmp/db-bk-{current_date}.sql")

        print(f"Creating backup to {output_file}")
        mysqldump_from_url(db_url, output_file)
        print(f"Backup completed. Output saved to {output_file}")

        # Get S3 bucket name and GCS bucket name from environment variables
        s3_bucket_name = os.getenv('S3_BUCKET_NAME')
        gcs_bucket_name = os.getenv('GCS_BUCKET_NAME')

        # Upload to S3 if bucket name is provided
        if s3_bucket_name:
            try:
                upload_to_s3(
                    output_file, 
                    s3_bucket_name,
                    object_name=f"db-bk-{current_date}.sql",
                )
            except Exception as e:
                send_error_email('S3 upload failed', str(e))

        # Upload to GCS if bucket name is provided
        if gcs_bucket_name:
            try:
                upload_to_gcs(
                    output_file,
                    gcs_bucket_name, 
                    object_name=f"db-bk-{current_date}.sql",
                )
            except Exception as e:
                send_error_email('GCS upload failed', str(e))

        # If neither S3 nor GCS bucket name is provided, send error email
        if not s3_bucket_name and not gcs_bucket_name:
            send_error_email('No storage bucket provided', 'Neither S3_BUCKET_NAME nor GCS_BUCKET_NAME environment variables found.')
    else:
        send_error_email('No database URL provided', 'DATABASE_URL environment variable not found.')

def send_error_email(subject, body):
    
    # Example usage of resend_send_email function
    from_email = os.getenv('MAIL_FROM')
    to_email = os.getenv('MAIL_TO')
    subject = os.getenv('MAIL_SUBJECT_ERROR')
    body = os.getenv('MAIL_BODY_ERROR')
    resend_send_email(from_email, to_email, subject, body)
    
if __name__ == "__main__":
    main()
