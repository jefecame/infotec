#!/bin/bash
set -e

echo "🚀 Laravel Initialization Script Starting..."

# Check if workspace is empty or doesn't have Laravel files
if [ ! -f "/workspace/composer.json" ] || [ ! -f "/workspace/artisan" ]; then
    echo "📁 Workspace is empty or missing Laravel files. Creating new Laravel project..."
    
    # Create Laravel project (preserve existing files if any)
    if [ "$(ls -A /workspace | grep -v .gitignore | wc -l)" -eq 0 ]; then
        echo "🏗️  Creating fresh Laravel project..."
        composer create-project laravel/laravel:${LARAVEL_VERSION:-11.*} /tmp/laravel-temp --prefer-dist --no-interaction
        
        # Move all files from temp to workspace (preserving .gitignore)
        cp -r /tmp/laravel-temp/. /workspace/
        rm -rf /tmp/laravel-temp
    else
        echo "📦 Files exist but no Laravel detected. Installing Laravel in existing directory..."
        cd /workspace
        composer init --no-interaction --name="infotec/laravel-app" --description="Laravel application for Infotec"
        composer require laravel/laravel:${LARAVEL_VERSION:-11.*} --no-interaction
    fi
    
    echo "✅ Laravel project created successfully!"
else
    echo "✅ Laravel project already exists. Installing/updating dependencies..."
fi

# Install/update dependencies
cd /workspace
echo "📦 Installing Composer dependencies..."
composer install --no-interaction --prefer-dist --optimize-autoloader

# Set proper permissions (if needed)
echo "🔐 Setting permissions..."
chmod -R 755 /workspace
chmod -R 775 /workspace/storage /workspace/bootstrap/cache 2>/dev/null || true

echo "🎉 Laravel initialization completed successfully!"
echo "📍 Laravel project is ready in /workspace"