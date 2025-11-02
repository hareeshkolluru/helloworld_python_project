#!/bin/bash
# Development startup script for full-stack application

echo "🚀 Starting HelloWorld FastAPI Full-Stack Application"
echo "======================================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed!"
    echo "📖 Please see DOCKER_SETUP.md for installation instructions"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Error: Docker is not running!"
    echo "💡 Please start Docker Desktop and try again"
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
fi

# Create uploads directory
mkdir -p uploads

# Start PostgreSQL with Docker Compose
echo "🐘 Starting PostgreSQL database..."
docker compose up -d

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Check if PostgreSQL is healthy
if docker compose ps | grep -q "healthy"; then
    echo "✅ PostgreSQL is ready!"
else
    echo "⚠️  PostgreSQL may still be initializing..."
fi

# Start backend in background
echo "🔧 Starting FastAPI backend on http://localhost:8000..."
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start frontend
echo "⚛️  Starting React frontend on http://localhost:3000..."
cd frontend && npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Application started successfully!"
echo "======================================================"
echo "📱 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🐘 PostgreSQL: localhost:5432"
echo "======================================================"
echo ""
echo "Press Ctrl+C to stop all services"

# Cleanup function
cleanup() {
    echo ''
    echo '🛑 Shutting down...'
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo '🐘 Stopping PostgreSQL...'
    docker compose stop
    echo '✅ All services stopped'
    exit
}

# Wait for Ctrl+C
trap cleanup INT
wait
