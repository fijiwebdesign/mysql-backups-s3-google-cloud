#!/bin/bash

# Script to build Docker image and push to Google Container Registry

# Step 1: Build Docker image

docker build -t mysql-backup .

# Step 2: Push Docker image to Google Container Registry (GCR)

# Authenticate Docker to GCR
gcloud auth configure-docker

# get gcloud projectId
PROJECT_ID=$(gcloud config get-value project)

# Tag the Docker image with the GCR repository path
docker tag mysql-backup gcr.io/$PROJECT_ID/mysql-backup

# Push the Docker image to GCR
docker push gcr.io/$PROJECT_ID/mysql-backup

# deploy
gcloud run deploy --image gcr.io/$PROJECT_ID/mysql-backup --platform managed --allow-unauthenticated

