#!/bin/bash

# User Microservice Setup Script
# This script sets up and runs the user microservice

echo "======================================"
echo "User Microservice Setup"
echo "======================================"

# Navigate to app directory
cd "$(dirname "$0")"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy .env.example to .env if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please update .env file with your settings"
fi

# Run the microservice
echo "======================================"
echo "Starting User Microservice..."
echo "======================================"
python -m uvicorn user.main:app --host 0.0.0.0 --port 8001 --reload

