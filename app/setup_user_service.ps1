# User Microservice Setup Script (PowerShell)
# This script sets up and runs the user microservice

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "User Microservice Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Navigate to app directory
Set-Location $PSScriptRoot

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

# Copy .env.example to .env if .env doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "Please update .env file with your settings" -ForegroundColor Green
}

# Run the microservice
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Starting User Microservice..." -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Service will be available at: http://localhost:8001" -ForegroundColor Green
Write-Host "API Documentation: http://localhost:8001/docs" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan

python -m uvicorn user.main:app --host 0.0.0.0 --port 8001 --reload

