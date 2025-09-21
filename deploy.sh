#!/bin/bash

# Exit on error
set -e

# Default region
REGION="asia-northeast3"

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Strabismus Detector Cloud Run Deployment Script${NC}"
echo "================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "gcloud could not be found. Please install the Google Cloud SDK."
    exit 1
fi

# Check if logged in to gcloud
ACCOUNT=$(gcloud config get-value account 2>/dev/null)
if [ -z "$ACCOUNT" ]; then
    echo "You are not logged in to gcloud. Please run 'gcloud auth login'."
    exit 1
fi

# Get current project
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
echo "Current project: $PROJECT_ID"
read -p "Continue with this project? (y/n): " CONFIRM_PROJECT
if [ "$CONFIRM_PROJECT" != "y" ]; then
    read -p "Enter project ID: " PROJECT_ID
    gcloud config set project $PROJECT_ID
fi

# Ask for region
read -p "Enter region (default: $REGION): " INPUT_REGION
if [ ! -z "$INPUT_REGION" ]; then
    REGION=$INPUT_REGION
fi

# Enable required APIs
echo -e "${YELLOW}Enabling required APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy
echo -e "${YELLOW}Starting Cloud Build...${NC}"
gcloud builds submit --config=cloudbuild.yaml --substitutions=_REGION=$REGION

echo -e "${GREEN}Deployment completed!${NC}"
echo "Your API is being deployed to Cloud Run."
echo "You can check the status in the GCP Console: https://console.cloud.google.com/run"