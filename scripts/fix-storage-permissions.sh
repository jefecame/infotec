#!/bin/bash

# =============================================================================
# INFOTEC - Fix Laravel Storage Directories and Permissions
# =============================================================================
# PURPOSE: Fix "Please provide a valid cache path" error in Codespaces
# USAGE: ./scripts/fix-storage-permissions.sh
# =============================================================================

echo "🔧 INFOTEC - Fixing Laravel Storage Directories"

# Define the Laravel source directory
LARAVEL_DIR="/app"

# Check if we're inside the container or outside
if [ ! -d "$LARAVEL_DIR" ]; then
    LARAVEL_DIR="./src"
fi

if [ ! -d "$LARAVEL_DIR" ]; then
    echo "❌ Laravel directory not found. Expected: $LARAVEL_DIR"
    exit 1
fi

cd "$LARAVEL_DIR" || exit 1

echo "📁 Working directory: $(pwd)"

# =============================================================================
# CREATE REQUIRED STORAGE DIRECTORIES
# =============================================================================

echo "📁 Creating storage directory structure..."

# Create all required storage directories
mkdir -p storage/framework/{cache,sessions,testing,views}
mkdir -p storage/framework/cache/data
mkdir -p storage/logs
mkdir -p storage/app/{private,public}
mkdir -p bootstrap/cache

# Create .gitignore files to preserve directory structure
echo "*" > storage/framework/cache/data/.gitignore
echo "!.gitignore" >> storage/framework/cache/data/.gitignore

echo "*" > storage/framework/sessions/.gitignore
echo "!.gitignore" >> storage/framework/sessions/.gitignore

echo "*" > storage/framework/testing/.gitignore
echo "!.gitignore" >> storage/framework/testing/.gitignore

echo "*" > storage/framework/views/.gitignore
echo "!.gitignore" >> storage/framework/views/.gitignore

echo "*" > storage/logs/.gitignore
echo "!.gitignore" >> storage/logs/.gitignore

echo "*" > storage/app/private/.gitignore
echo "!.gitignore" >> storage/app/private/.gitignore

echo "*" > storage/app/public/.gitignore
echo "!.gitignore" >> storage/app/public/.gitignore

echo "*" > bootstrap/cache/.gitignore
echo "!.gitignore" >> bootstrap/cache/.gitignore

echo "✅ Storage directories created successfully"

# =============================================================================
# SET PROPER PERMISSIONS
# =============================================================================

echo "🔐 Setting proper permissions..."

# Set proper permissions for Laravel storage and cache
find storage -type d -exec chmod 775 {} \; 2>/dev/null || true
find storage -type f -exec chmod 664 {} \; 2>/dev/null || true
find bootstrap/cache -type d -exec chmod 775 {} \; 2>/dev/null || true
find bootstrap/cache -type f -exec chmod 664 {} \; 2>/dev/null || true

# Alternative method for environments where find might not work
chmod -R 775 storage 2>/dev/null || true
chmod -R 775 bootstrap/cache 2>/dev/null || true

echo "✅ Permissions set successfully"

# =============================================================================
# VERIFY STRUCTURE
# =============================================================================

echo "🔍 Verifying directory structure..."

REQUIRED_DIRS=(
    "storage/framework/cache"
    "storage/framework/cache/data"
    "storage/framework/sessions"
    "storage/framework/testing"
    "storage/framework/views"
    "storage/logs"
    "storage/app/private"
    "storage/app/public"
    "bootstrap/cache"
)

MISSING_DIRS=()

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        MISSING_DIRS+=("$dir")
    fi
done

if [ ${#MISSING_DIRS[@]} -eq 0 ]; then
    echo "✅ All required directories exist"
else
    echo "❌ Missing directories:"
    for dir in "${MISSING_DIRS[@]}"; do
        echo "   - $dir"
    done
    exit 1
fi

# =============================================================================
# TEST CACHE FUNCTIONALITY
# =============================================================================

echo "🧪 Testing cache functionality..."

# Test if we can write to cache directory
TEST_FILE="storage/framework/cache/data/test_write_permission"
if echo "test" > "$TEST_FILE" 2>/dev/null; then
    rm -f "$TEST_FILE"
    echo "✅ Cache directory is writable"
else
    echo "❌ Cache directory is not writable"
    exit 1
fi

# Test views directory
TEST_FILE="storage/framework/views/test_write_permission"
if echo "test" > "$TEST_FILE" 2>/dev/null; then
    rm -f "$TEST_FILE"
    echo "✅ Views directory is writable"
else
    echo "❌ Views directory is not writable"
    exit 1
fi

echo "🎉 Storage directories fixed successfully!"
echo "💡 Laravel cache should now work properly"

# Clear any existing cache if artisan is available
if [ -f "artisan" ]; then
    echo "🧹 Clearing existing cache..."
    php artisan config:clear 2>/dev/null || true
    php artisan cache:clear 2>/dev/null || true
    php artisan view:clear 2>/dev/null || true
    echo "✅ Cache cleared"
fi

echo "✨ Fix completed successfully!"