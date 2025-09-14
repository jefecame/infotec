#!/bin/bash
set -e

echo "🚀 Application Startup Script Starting..."

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
timeout=60
while [ $timeout -gt 0 ]; do
    if mysqladmin ping -h mariadb -u ${LARAVEL_DATABASE_USER} -p${LARAVEL_DATABASE_PASSWORD} --silent; then
        echo "✅ Database is ready!"
        break
    fi
    echo "⏳ Waiting for database... ($timeout seconds remaining)"
    sleep 2
    timeout=$((timeout-2))
done

if [ $timeout -le 0 ]; then
    echo "❌ Database connection timeout!"
    exit 1
fi

# Check if Laravel project exists
if [ ! -f "/app/composer.json" ] || [ ! -f "/app/artisan" ]; then
    echo "❌ Laravel project not found in /app!"
    echo "💡 Please run the initialization first:"
    echo "   docker compose --profile init up laravel-init"
    echo "   docker compose up"
    exit 1
fi

cd /app

# Generate application key if not exists
if [ ! -f ".env" ] || ! grep -q "APP_KEY=" .env || [ "$(grep APP_KEY= .env | cut -d'=' -f2)" = "" ]; then
    echo "🔑 Generating application key..."
    php artisan key:generate --force
fi

# Configure database in Laravel .env if not configured
echo "⚙️  Configuring Laravel environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
fi

# Update database configuration in Laravel .env
sed -i "s/DB_CONNECTION=.*/DB_CONNECTION=mysql/" .env
sed -i "s/DB_HOST=.*/DB_HOST=mariadb/" .env
sed -i "s/DB_PORT=.*/DB_PORT=3306/" .env
sed -i "s/DB_DATABASE=.*/DB_DATABASE=${LARAVEL_DATABASE_NAME}/" .env
sed -i "s/DB_USERNAME=.*/DB_USERNAME=${LARAVEL_DATABASE_USER}/" .env
sed -i "s/DB_PASSWORD=.*/DB_PASSWORD=${LARAVEL_DATABASE_PASSWORD}/" .env

# Run database migrations
echo "🗄️  Running database migrations..."
php artisan migrate --force

# Run database seeders (if any)
echo "🌱 Running database seeders..."
php artisan db:seed --force || echo "ℹ️  No seeders to run"

# Clear and cache config
echo "🧹 Optimizing Laravel..."
php artisan config:clear
php artisan cache:clear
php artisan config:cache

# Start the application
echo "🎉 Starting Laravel development server..."
echo "🌐 Application will be available at: http://localhost:8000"
exec php artisan serve --host=0.0.0.0 --port=8000