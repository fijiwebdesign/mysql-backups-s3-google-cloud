#!/usr/bin/env python3

import os
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from utils.mysql_utils import mysqldump_from_url
from utils.s3_utils import upload_to_s3
from utils.gcs_utils import upload_to_gcs
from datetime import datetime


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get database URL from environment variable
    db_url = os.getenv('DATABASE_URL')

    if db_url:
      
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        
        # Get output file name from environment variable or default to "backup.sql"
        output_file = os.getenv('BACKUP_FILE', f"/app/backups/db-bk-{current_date}.sql")

        print(f"Creating backup to {output_file}")
        mysqldump_from_url(db_url, output_file)
        print(f"Backup completed. Output saved to {output_file}")

        # Get S3 bucket name and GCS bucket name from environment variables
        s3_bucket_name = os.getenv('S3_BUCKET_NAME')
        gcs_bucket_name = os.getenv('GCS_BUCKET_NAME')

        

        if s3_bucket_name:
            # Upload the file to S3
            # @todo and show progress
            upload_to_s3(
              output_file, 
              s3_bucket_name,
              object_name=f"db-bk-{current_date}.sql",
            )

        if gcs_bucket_name:
            # Upload the file to GCS 
            # @todo progress
            upload_to_gcs(
              output_file,
              gcs_bucket_name, 
              object_name=f"db-bk-{current_date}.sql",
            )

        if not s3_bucket_name and not gcs_bucket_name:
            print("Error: Neither S3_BUCKET_NAME nor GCS_BUCKET_NAME environment variables found.")
    else:
        print("Error: DATABASE_URL environment variable not found.")

if __name__ == "__main__":
    main()
