#!/bin/bash

# =============================================================================
# INFOTEC - Laravel Container Startup Script
# =============================================================================
# PURPOSE: Initialize Laravel application in Docker container
# USAGE: Called automatically by docker-compose.yml
# LOCATION: /app/scripts/laravel-startup.sh (inside container)
# =============================================================================

set -e  # Exit on any error

echo "🚀 INFOTEC - Configuración automática de Laravel"

# =============================================================================
# WAIT FOR MARIADB
# =============================================================================

echo "⏳ Esperando MariaDB..."
for i in {1..30}; do
    # Preferimos /dev/tcp porque la imagen puede no tener 'nc'
    if bash -c ">/dev/tcp/mariadb/3306" >/dev/null 2>&1; then
        echo "✅ MariaDB disponible en puerto 3306"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Error: MariaDB no disponible después de 60 segundos"
        exit 1
    fi
    sleep 2
done

# =============================================================================
# NAVIGATE TO APP DIRECTORY
# =============================================================================

cd /app || { echo "❌ Error: No se puede acceder al directorio /app"; exit 1; }
echo "📁 Directorio de trabajo: $(pwd)"

# =============================================================================
# CREATE LARAVEL PROJECT IF NOT EXISTS
# =============================================================================

if [ ! -f artisan ] && [ ! -f composer.json ]; then
    echo "📁 Creando nuevo proyecto Laravel..."
    
    # Preserve custom .gitignore
    [ -f .gitignore ] && cp .gitignore /tmp/custom-gitignore
    
    # Create Laravel project
    echo "📦 Descargando Laravel $LARAVEL_VERSION..."
    composer create-project laravel/laravel:$LARAVEL_VERSION /tmp/laravel --prefer-dist --no-interaction
    
    echo "📋 Copiando archivos del proyecto..."
    cp -r /tmp/laravel/. . && rm -rf /tmp/laravel
    
    # Restore custom .gitignore
    [ -f /tmp/custom-gitignore ] && cp /tmp/custom-gitignore .gitignore
    
    echo "✅ Laravel creado exitosamente"
else
    echo "✅ Laravel ya existe, continuando con configuración..."
fi

# =============================================================================
# INSTALL DEPENDENCIES
# =============================================================================

echo "📦 Verificando dependencias de Composer..."
if [ ! -d vendor ] || [ ! -f vendor/autoload.php ]; then
    echo "📥 Instalando dependencias..."
    composer install --no-interaction --optimize-autoloader --no-dev
    echo "✅ Dependencias instaladas"
else
    echo "✅ Dependencias ya instaladas"
fi

# =============================================================================
# CONFIGURE LARAVEL ENVIRONMENT
# =============================================================================

echo "⚙️ Configurando entorno Laravel..."

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "📄 Creando archivo .env..."
    cp .env.example .env
fi

# Configure database using environment variables
echo "🗄️ Configurando conexión de base de datos..."

# Helper: replace a key even if it's commented or add it if missing
replace_or_add_env() {
    local key="$1" value="$2"
    # If a line for the key exists (commented or not), replace it. Allow leading spaces and optional '#'
    if grep -q -E "^[[:space:]]*#?[[:space:]]*${key}=" .env; then
        sed -i -E "s/^[[:space:]]*#?[[:space:]]*(${key})=.*/\1=${value}/" .env
    else
        echo "${key}=${value}" >> .env
    fi
}

replace_or_add_env "DB_CONNECTION" "$DB_CONNECTION"
replace_or_add_env "DB_HOST" "$DB_HOST"
replace_or_add_env "DB_PORT" "$DB_PORT"
replace_or_add_env "DB_DATABASE" "$DB_DATABASE"
replace_or_add_env "DB_USERNAME" "$DB_USERNAME"
replace_or_add_env "DB_PASSWORD" "$DB_PASSWORD"

echo "✅ Configuración de BD: MariaDB ($DB_HOST:$DB_PORT/$DB_DATABASE)"

# Generate APP_KEY if not exists
if ! grep -q 'APP_KEY=base64:' .env; then
    echo "🔑 Generando APP_KEY..."
    php artisan key:generate --force
    echo "✅ APP_KEY generada"
else
    echo "✅ APP_KEY ya existe"
fi

# =============================================================================
# CREATE AND CONFIGURE STORAGE DIRECTORIES (FIX FOR CODESPACES)
# =============================================================================

echo "📁 Creando directorios de storage requeridos..."
mkdir -p storage/framework/{cache,sessions,testing,views}
mkdir -p storage/framework/cache/data
mkdir -p storage/logs
mkdir -p storage/app/{private,public}
mkdir -p bootstrap/cache

# Create .gitignore files to preserve structure
echo "📄 Creando archivos .gitignore para estructura..."
echo '*' > storage/framework/cache/data/.gitignore
echo '!.gitignore' >> storage/framework/cache/data/.gitignore
echo '*' > storage/framework/sessions/.gitignore
echo '!.gitignore' >> storage/framework/sessions/.gitignore
echo '*' > storage/framework/testing/.gitignore
echo '!.gitignore' >> storage/framework/testing/.gitignore
echo '*' > storage/framework/views/.gitignore
echo '!.gitignore' >> storage/framework/views/.gitignore
echo '*' > storage/logs/.gitignore
echo '!.gitignore' >> storage/logs/.gitignore
echo '*' > bootstrap/cache/.gitignore
echo '!.gitignore' >> bootstrap/cache/.gitignore

# Configure permissions (FIX FOR CODESPACES)
echo "🔐 Configurando permisos de storage..."
find storage -type d -exec chmod 775 {} \; 2>/dev/null || chmod -R 775 storage
find storage -type f -exec chmod 664 {} \; 2>/dev/null || chmod -R 664 storage/*/
find bootstrap/cache -type d -exec chmod 775 {} \; 2>/dev/null || chmod -R 775 bootstrap/cache
find bootstrap/cache -type f -exec chmod 664 {} \; 2>/dev/null || chmod -R 664 bootstrap/cache/

echo "✅ Directorios de storage configurados correctamente"

# =============================================================================
# CLEAR EXISTING CACHE TO PREVENT ISSUES
# =============================================================================

echo "🧹 Limpiando cache existente..."
php artisan config:clear 2>/dev/null || true
php artisan cache:clear 2>/dev/null || true
php artisan view:clear 2>/dev/null || true
echo "✅ Cache limpiado"

# =============================================================================
# RUN DATABASE MIGRATIONS
# =============================================================================

echo "🗄️ Ejecutando migraciones de base de datos..."
if php artisan migrate --force 2>/dev/null; then
    echo "✅ Migraciones ejecutadas exitosamente"
else
    echo "⚠️ Error en migraciones, reintentando en 5 segundos..."
    sleep 5
    if php artisan migrate --force; then
        echo "✅ Migraciones ejecutadas exitosamente (segundo intento)"
    else
        echo "❌ Error: No se pudieron ejecutar las migraciones"
        echo "🔍 Verificando conectividad de base de datos..."
        php artisan tinker --execute="echo 'DB Status: ' . (DB::connection()->getPdo() ? 'Connected' : 'Failed');" 2>/dev/null || echo "❌ No se puede conectar a la base de datos"
    fi
fi

# =============================================================================
# RUN SEEDERS AUTOMATICAMENTE
# =============================================================================

echo "🌱 Ejecutando seeder inicial..."
if php artisan db:seed --class=InitialSeeder --force 2>/dev/null; then
    echo "✅ Seeder inicial ejecutado exitosamente"
else
    echo "⚠️ Error al ejecutar el seeder inicial"
fi

# =============================================================================
# FINAL SETUP AND HEALTH CHECK
# =============================================================================

echo "🔍 Verificación final del sistema..."

# Verify critical directories exist and are writable
REQUIRED_DIRS=(
    "storage/framework/cache"
    "storage/framework/views" 
    "storage/logs"
    "bootstrap/cache"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "❌ Error: Directorio faltante: $dir"
        exit 1
    fi
    
    if [ ! -w "$dir" ]; then
        echo "❌ Error: Directorio sin permisos de escritura: $dir"
        exit 1
    fi
done

echo "✅ Todos los directorios requeridos están disponibles y con permisos correctos"

# Verify database connection
echo "🔍 Verificando conexión de base de datos..."
if php artisan tinker --execute="DB::connection()->getPdo();" >/dev/null 2>&1; then
    echo "✅ Conexión de base de datos verificada"
else
    echo "⚠️ Advertencia: Problemas de conectividad con la base de datos"
fi

# =============================================================================
# START LARAVEL DEVELOPMENT SERVER 
# =============================================================================

echo "✅ Configuración completada exitosamente"
echo "🎉 Laravel listo en http://localhost:8000"
echo "🚀 Iniciando servidor de desarrollo..."

# Start the Laravel development server
exec php artisan serve --host=0.0.0.0 --port=8000