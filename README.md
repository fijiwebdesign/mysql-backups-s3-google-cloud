# MYSQL BACKUPS 

Mysql backups created with mysqldump and uploaded to S3 compatible or Google Cloud

## Install

Clone this repo

```sh
git clone git@github.com:treks-app/mysql-backup.git
```

## Usage

Create a `.env` file with the following example:

```sh

DATABASE_URL=mysql://user:pass@localhost:3306/db_name

# create this from s3 console
# this example uses vultr which is compatible to S3 but much cheaper
S3_BUCKET_NAME=mysql-backups # auto created
S3_ENDPOINT_URL=https://sgp1.vultrobjects.com
S3_ACCESS_KEY=s3-key-xyz
S3_SECRET_KEY=***
S3_REGION=sg

# create this from google cloud console
GOOGLE_APPLICATION_CREDENTIALS=../project-224203-f34812eb7d22.json
GCS_BUCKET_NAME=mysql-backups # auto created

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

Or run install script (runs commands above)

```sh
sh ./scripts/python-env-install.sh
```

## Deploy to Google Cloud

Run gcloud run docker deploy script to build a docker image and push it to gcr.io/$PROJECT_ID/mysql-backup then deploy this image

```sh
sh ./scripts/gcloud-deploy-docker.sh
```

Alternatively you can deploy the source code and have gcloud run build the image

```sh
sh ./scripts/gcloud-deploy-source.sh
```

Note that you will receive an error 

```
ERROR: (gcloud.run.deploy) Revision 'mysql-backup-00004-rlz' is not ready and cannot serve traffic. The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable. Logs for this revision might contain more information.
```

Ignore this error as we are not trying to deploy it as a HTTP server. 

Follow instructions below to setup the Cloud run job which acts similar to a cron job. 

## Setup Google Cloud Run Job (cron job)

1) Go to Google Cloud Run dashboard and add a new "Cloud Run Job". 

2) Choose the mysql-backup docker image. 

3) Add the env vars and secrets 

4) Set the cron schedule. eg: `0 */1 * * *` to run hourly

5) Run it to test

## Deploy to Railway

1) Log into Railway and create a new project
2) Connect Railway to your github account
3) Create a new service from the github repository
4) In the new railway service settings set the Cron Schedule to something like `0 */1 * * *` (every hour)

## Deploy elsewhere

Deploy to any devops based deployment by pointing it to the git repo. 
It will pickup the `Dockerfile` and build it.

Deploy to any docker container cloud by building the docker image and pushing it. 
See: `scripts/gcloud-build.sh` for an example