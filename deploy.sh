#!/bin/bash

echo "Starting deployment process..."

# Install or update Python dependencies
pip install -r requirements.txt
echo "All requirements have been set"

# Restart the FastAPI application using uvicorn
uvicorn main:app --host 0.0.0.0 --port 1717 --reload

echo "Deployment process completed successfully."