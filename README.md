# MYSQL BACKUPS 

Mysql backups created with mysqldump and uploaded to S3 compatible or Google Cloud

## Usage

Create a `.env` file with the following example:

```

DATABASE_URL=mysql://user:pass@localhost:3306/db_name

S3_BUCKET_NAME=bucket-name
S3_ENDPOINT_URL=https://sgp1.vultrobjects.com
S3_ACCESS_KEY=key
S3_SECRET_KEY=***
S3_REGION=sg

GOOGLE_APPLICATION_CREDENTIALS=../x-catwalk-224203-f34812eb7d22.json
GCS_BUCKET_NAME=treks-db
```