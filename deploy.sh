#!/bin/bash

echo "Starting deployment process..."

# Pull the latest changes from the GitHub
git pull origin master

# Install or update Python dependencies
pip install -r requirements.txt
echo "All requirements have been set"

# Set domain name using dnsmasq, restart the existing process
# pkill dnsmasq && dnsmasq -C ~/visitmarthapura/.local-dns.conf

# Restart the FastAPI application using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8888 --reload

echo "Deployment process completed successfully."