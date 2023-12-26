#!/bin/bash

echo "Starting deployment process..."
#cd visitmarthapura

# Pull the latest changes from the GitHub
git pull origin master

# Install or update Python dependencies
pip install -r requirements.txt

# Restart the FastAPI application using uvicorn
uvicorn main:app --reload

echo "Deployment process completed successfully."