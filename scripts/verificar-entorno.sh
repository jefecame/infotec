#!/bin/bash
# =============================================================================
# INFOTEC - Script de Verificación del Entorno
# =============================================================================
# Este script verifica que todo esté funcionando correctamente
# =============================================================================

set -e

echo "🔍 INFOTEC - Verificación del Entorno Docker + Laravel"
echo "=================================================="

# Función para verificar si un comando existe
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "❌ Error: $1 no está instalado"
        return 1
    else
        echo "✅ $1 está disponible"
        return 0
    fi
}

# Función para verificar servicios Docker
check_docker_service() {
    local service_name="$1"
    local container_name="$2"
    
    if docker compose ps --services --filter "status=running" | grep -q "^${service_name}$"; then
        echo "✅ Servicio $service_name está ejecutándose"
        
        # Verificar salud si hay healthcheck
        health=$(docker inspect --format='{{.State.Health.Status}}' "$container_name" 2>/dev/null || echo "no-healthcheck")
        if [ "$health" = "healthy" ]; then
            echo "   💚 Estado: Saludable"
        elif [ "$health" = "unhealthy" ]; then
            echo "   ❤️ Estado: No saludable"
        elif [ "$health" = "starting" ]; then
            echo "   🟡 Estado: Iniciando..."
        fi
    else
        echo "❌ Servicio $service_name no está ejecutándose"
        return 1
    fi
}

# 1. Verificar herramientas necesarias
echo ""
echo "1️⃣ Verificando herramientas necesarias..."
check_command "docker" || exit 1
check_command "docker-compose" || check_command "docker compose" || exit 1
check_command "make" || echo "⚠️  Advertencia: make no disponible (opcional)"

# 2. Verificar archivos de configuración
echo ""
echo "2️⃣ Verificando archivos de configuración..."

if [ -f ".env" ]; then
    echo "✅ Archivo .env encontrado"
    
    # Verificar variables críticas
    if grep -q "MARIADB_DATABASE=" .env && grep -q "MARIADB_USER=" .env; then
        echo "   ✅ Variables de MariaDB configuradas"
    else
        echo "   ❌ Variables de MariaDB faltantes en .env"
    fi
else
    echo "❌ Archivo .env no encontrado"
    if [ -f ".env.example" ]; then
        echo "   💡 Copiar .env.example a .env y configurar"
    fi
fi

if [ -f "docker-compose.yml" ]; then
    echo "✅ docker-compose.yml encontrado"
else
    echo "❌ docker-compose.yml no encontrado"
    exit 1
fi

# 3. Verificar estado de contenedores
echo ""
echo "3️⃣ Verificando estado de contenedores..."

if [ "$(docker compose ps -q)" ]; then
    check_docker_service "mariadb" "infotec_mariadb"
    check_docker_service "laravel" "infotec_laravel"
else
    echo "❌ No hay contenedores ejecutándose"
    echo "   💡 Ejecutar: make start"
fi

# 4. Verificar conectividad
echo ""
echo "4️⃣ Verificando conectividad..."

# Verificar Laravel
if curl -s -f "http://localhost:8000" > /dev/null; then
    echo "✅ Laravel responde en http://localhost:8000"
else
    echo "❌ Laravel no responde en http://localhost:8000"
fi

# Verificar MariaDB
if docker compose exec -T mariadb mysqladmin ping -h localhost --silent 2>/dev/null; then
    echo "✅ MariaDB responde correctamente"
else
    echo "❌ MariaDB no responde"
fi

# 5. Verificar estructura de archivos
echo ""
echo "5️⃣ Verificando estructura Laravel..."

if [ -d "src" ]; then
    if [ -f "src/artisan" ] && [ -f "src/composer.json" ]; then
        echo "✅ Proyecto Laravel encontrado en src/"
        
        if [ -f "src/.env" ]; then
            echo "   ✅ Laravel configurado (.env existe)"
        else
            echo "   ❌ Laravel no configurado (.env faltante)"
        fi
        
        if [ -d "src/vendor" ]; then
            echo "   ✅ Dependencias instaladas"
        else
            echo "   ❌ Dependencias no instaladas"
        fi
    else
        echo "❌ No hay proyecto Laravel en src/"
    fi
else
    echo "❌ Directorio src/ no existe"
fi

# 6. Mostrar resumen de recursos
echo ""
echo "6️⃣ Uso de recursos:"
if docker compose ps -q > /dev/null 2>&1; then
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" infotec_laravel infotec_mariadb 2>/dev/null || echo "   No se pudo obtener información de recursos"
fi

echo ""
echo "🎯 Verificación completada"
echo ""
echo "💡 Comandos útiles:"
echo "   make start  - Iniciar entorno"
echo "   make logs   - Ver registros"
echo "   make shell  - Acceder al contenedor"
echo "   make status - Estado detallado"