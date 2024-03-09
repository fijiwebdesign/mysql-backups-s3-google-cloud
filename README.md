# MYSQL BACKUPS 

Mysql backups created with mysqldump and uploaded to S3 compatible or Google Cloud

## Install

Clone this repo

```sh
git clone git@github.com:treks-app/mysql-backup.git
```

Run install script

```sh
sh ./scripts/install.sh
```

## Usage

Create a `.env` file with the following example:

```sh

DATABASE_URL=mysql://user:pass@localhost:3306/db_name

S3_BUCKET_NAME=bucket-name
S3_ENDPOINT_URL=https://sgp1.vultrobjects.com
S3_ACCESS_KEY=key
S3_SECRET_KEY=***
S3_REGION=sg

GOOGLE_APPLICATION_CREDENTIALS=../x-catwalk-224203-f34812eb7d22.json
GCS_BUCKET_NAME=treks-db

MAIL_FROM=gabe@fijiwebdesign.com
MAIL_TO=gabe@fijiwebdesign.com
MAIL_SUBJECT_ERROR="DB backup error"
MAIL_BODY_ERROR="Database backup failed for  production"
```

## Run locally

```sh
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
python3 mysql_backup.py 
```

## Deploy to Google Cloud

Run gcloud run deploy script

```sh
sh ./scripts/gcloud-build.sh
```

1) Go to Google Cloud Run dashboard and add a new "Cloud Run Job". 

2) Choose the mysql-backup docker image. 

3) Add the env vars and secrets 

4) Set the cron schedule. eg: `0 */1 * * *` to run hourly

5) Run it to test

## Deploy elsewhere

Deploy to any devops based deployment by pointing it to the git repo. 
It will pickup the `Dockerfile` and build it.

Railway.app is very easy to deploy to

Deploy to any docker container cloud by building the docker image and pushing it. 
See: `scripts/gcloud-build.sh` for an example