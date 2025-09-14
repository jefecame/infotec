.PHONY: help start stop restart logs logs-db shell artisan clean status composer-install composer-update backup check

# =============================================================================
# INFOTEC - Comandos Laravel Docker (Makefile)
# =============================================================================
# Todos los comandos están en español y simplificados
# El comando principal es: make start (equivale a docker compose up -d)
# =============================================================================

# Comando por defecto - muestra ayuda
help:
	@echo "🚀 INFOTEC - Comandos Laravel Docker"
	@echo "========================================"
	@echo "PRINCIPAL:"
	@echo "make start           - Iniciar entorno (crea Laravel automáticamente)"
	@echo "make stop            - Detener servicios"
	@echo "make restart         - Reiniciar servicios"
	@echo "make status          - Mostrar estado de contenedores y recursos"
	@echo ""
	@echo "DESARROLLO:"
	@echo "make shell           - Acceder al contenedor Laravel"
	@echo "make artisan CMD     - Ejecutar comando artisan (ej: make artisan migrate)"
	@echo "make composer-install- Instalar dependencias PHP"
	@echo "make composer-update - Actualizar dependencias PHP"
	@echo ""
	@echo "MONITOREO:"
	@echo "make logs            - Ver registros de Laravel"
	@echo "make logs-db         - Ver registros de MariaDB"
	@echo ""
	@echo "MANTENIMIENTO:"
	@echo "make backup          - Crear backup de base de datos"
	@echo "make check           - Verificar estado completo del entorno"
	@echo "make clean           - Eliminar todo (contenedores y datos)"
	@echo ""
	@echo "🌐 Después de 'make start', abrir: http://localhost:8000"

# Iniciar entorno completo (crea Laravel automáticamente)
start:
	@echo "🚀 Iniciando entorno Laravel Infotec..."
	@echo "💡 Laravel se creará automáticamente si src/ está vacío"
	docker compose up -d
	@echo "✅ Servicios iniciados. Laravel disponible en: http://localhost:8000"

# Detener servicios
stop:
	@echo "🚨 Deteniendo servicios..."
	docker compose down
	@echo "✅ Servicios detenidos"

# Reiniciar servicios
restart: stop start

# Ver registros de Laravel
logs:
	@echo "📝 Mostrando registros de Laravel (Ctrl+C para salir):"
	docker compose logs -f laravel

# Acceder al contenedor Laravel
shell:
	@echo "💻 Accediendo al contenedor Laravel..."
	docker compose exec laravel bash

# Ejecutar comandos artisan
artisan:
	@echo "⚙️ Ejecutando: php artisan $(CMD)"
	docker compose exec laravel php artisan $(CMD)

# Limpiar todo el entorno
clean:
	@echo "🧹 Eliminando todos los contenedores y datos..."
	docker compose down -v --remove-orphans
	@echo "📁 Eliminando carpeta src/..."
	@if [ -d "src" ]; then rm -rf src/*; fi
	@echo "✅ Entorno limpio. Usar 'make start' para reinicializar"

# Mostrar estado detallado
status:
	@echo "📈 Estado de los contenedores INFOTEC:"
	docker compose ps
	@echo ""
	@echo "📊 Uso de recursos:"
	@docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" infotec_laravel infotec_mariadb 2>/dev/null || echo "Contenedores no están ejecutándose"

# Ver logs de base de datos
logs-db:
	@echo "📄 Mostrando registros de MariaDB (Ctrl+C para salir):"
	docker compose logs -f mariadb

# Instalar dependencias con Composer
composer-install:
	@echo "📦 Instalando dependencias PHP..."
	docker compose run --rm composer install
	@echo "✅ Dependencias instaladas"

# Actualizar dependencias con Composer
composer-update:
	@echo "🔄 Actualizando dependencias PHP..."
	docker compose run --rm composer update
	@echo "✅ Dependencias actualizadas"

# Crear backup de base de datos
backup:
	@echo "📦 Creando backup de base de datos..."
	@mkdir -p ./backups
	docker compose exec -T mariadb mysqldump -u $$(grep MARIADB_USER .env | cut -d '=' -f2) -p$$(grep MARIADB_PASSWORD .env | cut -d '=' -f2) $$(grep MARIADB_DATABASE .env | cut -d '=' -f2) > "./backups/backup_$$(date +%Y%m%d_%H%M%S).sql"
	@echo "✅ Backup creado en ./backups/"

# Verificar estado completo del entorno
check:
	@echo "🔍 Verificando entorno INFOTEC..."
	@bash scripts/verificar-entorno.sh || echo "⚠️ Script de verificación no disponible"
