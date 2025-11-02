#!/bin/bash
# Quick start script for the FastAPI application

# Check if .env exists, if not copy from .env.example
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

# Run the application with uv
echo "Starting FastAPI application..."
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
