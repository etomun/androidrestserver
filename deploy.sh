#!/bin/bash

echo "Starting deployment process..."
#cd visitmarthapura

# Pull the latest changes from the GitHub
git pull origin master

# Install or update Python dependencies
pip install -r requirements.txt
echo "All requirements is set"

# Restart the FastAPI application using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8008--reload

echo "Deployment process completed successfully."