#!/bin/bash

echo "Starting deployment process..."
#cd visitmarthapura

# Pull the latest changes from the GitHub
git pull origin master

# Set domain name using dnsmasq
dnsmasq -C ~/visitmarthapura/.local-dns.conf

# Install or update Python dependencies
pip install -r requirements.txt
echo "All requirements have been set"

# Restart the FastAPI application using uvicorn
uvicorn main:app --host 0.0.0.0 --port 1717 --reload

echo "Deployment process completed successfully."