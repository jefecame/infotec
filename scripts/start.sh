#!/bin/bash
set -e

echo "🚀 Infotec Laravel Docker Setup - Automated Initialization"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running!"
    echo "💡 Please start Docker Desktop and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "💡 Please copy .env.example to .env and configure your settings:"
    echo "   cp .env.example .env"
    echo "   # Edit .env with your database credentials"
    exit 1
fi

echo "✅ Docker is running"
echo "✅ Environment file found"

# Step 1: Initialize Laravel project if needed
echo ""
echo "🏗️  Step 1: Initializing Laravel project..."
echo "=================================================="

if [ ! -f "src/composer.json" ] || [ ! -f "src/artisan" ]; then
    echo "📁 Laravel project not found. Creating new project..."
    docker compose --profile init up --build laravel-init
    
    if [ $? -eq 0 ]; then
        echo "✅ Laravel project initialized successfully!"
    else
        echo "❌ Laravel initialization failed!"
        exit 1
    fi
else
    echo "✅ Laravel project already exists"
fi

# Step 2: Start all services
echo ""
echo "🐳 Step 2: Starting Docker services..."
echo "=================================================="
docker compose up -d --build

if [ $? -eq 0 ]; then
    echo "✅ All services started successfully!"
else
    echo "❌ Failed to start services!"
    exit 1
fi

# Wait a bit for services to be fully ready
echo ""
echo "⏳ Waiting for services to be fully ready..."
sleep 5

# Check if application is accessible
echo ""
echo "🔍 Checking application status..."
echo "=================================================="

# Wait for application to respond
timeout=30
while [ $timeout -gt 0 ]; do
    if curl -s http://localhost:8000 > /dev/null 2>&1; then
        echo "✅ Application is responding!"
        break
    fi
    echo "⏳ Waiting for application... ($timeout seconds remaining)"
    sleep 2
    timeout=$((timeout-2))
done

if [ $timeout -le 0 ]; then
    echo "⚠️  Application might still be starting up..."
    echo "💡 Check logs with: docker compose logs application"
fi

# Success message
echo ""
echo "🎉 SETUP COMPLETED SUCCESSFULLY!"
echo "=================================================="
echo "🌐 Laravel application is running at: http://localhost:8000"
echo "🗄️  MariaDB is available on localhost:3306"
echo ""
echo "📋 Useful commands:"
echo "   docker compose logs              # View all logs"
echo "   docker compose logs application  # View Laravel logs"
echo "   docker compose exec application bash  # Access Laravel container"
echo "   docker compose down              # Stop all services"
echo "   docker compose down -v          # Stop and remove all data"
echo ""
echo "Happy coding! 🚀"