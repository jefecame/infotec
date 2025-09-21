#!/bin/bash

# =============================================================================
# INFOTEC - Quick Fix for Codespaces Storage Issue
# =============================================================================
# PURPOSE: Fix "Please provide a valid cache path" error in Codespaces
# USAGE: ./scripts/fix-codespace-storage.sh
# =============================================================================

echo "🚀 INFOTEC - Quick Fix for Codespaces Storage Issue"

# Check if we're in the correct directory
if [ ! -d "src" ]; then
    echo "❌ src directory not found. Please run this script from the project root."
    echo "📍 Current directory: $(pwd)"
    echo "📁 Expected structure: ./src/"
    exit 1
fi

echo "📁 Working from project root: $(pwd)"
echo "📍 Target Laravel directory: ./src/"

cd src

echo "📁 Creating Laravel storage directories..."

# Create all required storage directories
sudo mkdir -p storage/framework/{cache,sessions,testing,views}
sudo mkdir -p storage/framework/cache/data
sudo mkdir -p storage/logs
sudo mkdir -p storage/app/{private,public}
sudo mkdir -p bootstrap/cache

echo "🔐 Setting proper permissions..."

# Set proper permissions (775 for directories, 664 for files)
sudo chmod -R 775 storage
sudo chmod -R 775 bootstrap/cache

echo "✅ Storage directories created and permissions set!"

# Test if we can access the storage directories
echo "🧪 Testing storage access..."

if [ -w "storage/framework/views" ] && [ -w "storage/framework/cache" ]; then
    echo "✅ Storage directories are writable!"
else
    echo "⚠️ Storage directories may not be properly writable"
    echo "🔧 Running additional permission fix..."
    sudo chown -R $(whoami):$(whoami) storage bootstrap/cache 2>/dev/null || true
fi

echo "🎉 Fix completed!"
echo "💡 You can now run: docker compose up -d"
echo "🌐 Laravel should be accessible at http://localhost:8000"