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
# https://www.vultr.com/pricing/
S3_BUCKET_NAME=mysql-backups # auto created
S3_ENDPOINT_URL=https://sgp1.vultrobjects.com
S3_ACCESS_KEY=s3-key-xyz
S3_SECRET_KEY=***
S3_REGION=sg

# create this from google cloud console
GOOGLE_APPLICATION_CREDENTIALS=secrets/project-224203-f34812eb7d22.json
GCS_BUCKET_NAME=mysql-backups # auto created

# instead of a file you can use a json string
# make sure it is one line
# use sh scripts/gcloud-json2string.sh secrets/file-name.json create string
# GOOGLE_APPLICATION_CREDENTIALS_JSON={...}

# use https://resend.com/ to send emails
RESEND_API_KEY=your-api-key
MAIL_FROM=email@domain.com
MAIL_TO=email@domain.com
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

The build does not includ the `.env` file and `secrets/` folder for security. 

You have to supply the env variables to your build using the google cloud UI or the yaml file after you create the cloud run job. 

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

To get the `GOOGLE_APPLICATION_CREDENTIALS_JSON` env var use
```sh
sh scripts/gcloud-json2string.sh secrets/file-name.json
```

The other env vars can be added via the YAML tab. 
Add it after the `containers: -image`. 

Generate the yaml structure with: 

```sh
sh scripts/env2yaml.sh 
```

```yaml
 containers:
          - image: gcr.io/x-catwalk-224203/mysql-backup@sha256:8d230341ec262f43ac7e20877a7672d5f6d7da4f4178460d255864ac8f9b7362
            env:
            - name: DATABASE_URL
              value: mysql://root:passB@monorail.proxy.rlwy.net:40790/railway
            - name: S3_BUCKET_NAME
              value: mysql-backup
            - name: S3_ENDPOINT_URL
              value: https://sgp1.vultrobjects.com
            - name: S3_ACCESS_KEY
              value: ***
            - name: S3_SECRET_KEY
              value: ***
            - name: S3_REGION
              value: sg
            - name: GOOGLE_APPLICATION_CREDENTIALS_JSON
              value: ***
            - name: GCS_BUCKET_NAME
              value: treks-db
            - name: RESEND_API_KEY
              value: ***
            - name: MAIL_FROM
              value: gabe@example.com
            - name: MAIL_TO
              value: gabe@example.com
            - name: MAIL_SUBJECT_ERROR
              value: Treks db backup error
            - name: MAIL_BODY_ERROR
              value: Database backup failed for treks production
```

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