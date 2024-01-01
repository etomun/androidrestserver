#!/bin/bash

echo "Starting deployment process..."

# Pull the latest changes from the GitHub
git pull origin master

# Install or update Python dependencies
pip install -r requirements.txt
echo "All requirements have been set"

# Load environment variables from .env using python-decouple
eval "$(python -c "from decouple import config; print('\n'.join([f'export {key}={value}' for key, value in config.items()]))")"

# Run Alembic migrations
alembic upgrade head

# I skipped the test in production

echo "Deployment process completed successfully."
echo "Starting the application..."

# Restart the FastAPI application using uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8888 --reload