# =============================================================================
# INFOTEC - Comandos Automatizados con Makefile
# =============================================================================
# Facilita el uso del workspace para desarrollo local y GitHub Codespaces
# =============================================================================

.PHONY: help start stop restart logs clean setup dev backup restore artisan composer test

# Configuración por defecto
COMPOSE_FILE = docker-compose.yml
COMPOSE_PROJECT = infotec

# =============================================================================
# COMANDOS PRINCIPALES
# =============================================================================

help: ## 📖 Mostrar ayuda
	@echo ""
	@echo "🚀 INFOTEC - Comandos Disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "   \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

setup: ## 🔧 Configuración inicial (desarrollo)
	@echo "🔧 Configurando entorno de desarrollo..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "✅ .env creado desde .env.example"; fi
	@echo "📋 Verifica las credenciales en .env antes de ejecutar 'make start'"

start: setup ## ▶️ Iniciar entorno de desarrollo
	@echo "🚀 Iniciando INFOTEC (desarrollo)..."
	docker compose --env-file .env up -d
	@echo "✅ Laravel disponible en: http://localhost:8000"

dev: start ## 🔧 Alias para desarrollo (igual que start)

stop: ## ⏹️ Detener servicios
	@echo "⏹️ Deteniendo servicios..."
	docker compose down

restart: stop start ## 🔄 Reiniciar servicios

clean: ## 🧹 Limpiar completamente (CUIDADO: borra datos)
	@echo "🧹 Limpiando todo (incluyendo volúmenes)..."
	@read -p "¿Estás seguro? (s/N): " confirm && [ "$$confirm" = "s" ] || exit 1
	docker compose down -v --remove-orphans
	docker system prune -f

# =============================================================================
# COMANDOS DE MONITOREO
# =============================================================================

logs: ## 📄 Ver logs de Laravel
	docker compose logs -f laravel

logs-db: ## 📄 Ver logs de MariaDB
	docker compose logs -f mariadb

status: ## 📊 Estado de contenedores
	docker compose ps

# =============================================================================
# COMANDOS DE DESARROLLO
# =============================================================================

shell: ## 💻 Acceder al contenedor Laravel
	docker compose exec laravel bash

artisan: ## 🎨 Ejecutar comando artisan (uso: make artisan cmd="migrate")
	docker compose exec laravel php artisan $(cmd)

composer: ## 📦 Ejecutar composer (uso: make composer cmd="install")
	docker compose exec laravel composer $(cmd)

migrate: ## 🗄️ Ejecutar migraciones
	docker compose exec laravel php artisan migrate

fresh: ## 🆕 Migración fresca con seed
	docker compose exec laravel php artisan migrate:fresh --seed

test: ## 🧪 Ejecutar tests
	docker compose exec laravel php artisan test

# =============================================================================
# COMANDOS DE BACKUP Y RESTORE
# =============================================================================

backup: ## 💾 Hacer backup de la base de datos
	@echo "💾 Creando backup..."
	@mkdir -p backups
	docker compose exec mariadb mysqldump -u root -p$(shell grep MARIADB_ROOT_PASSWORD .env | cut -d '=' -f2) --all-databases > backups/backup-$(shell date +%Y%m%d-%H%M%S).sql
	@echo "✅ Backup creado en backups/"

restore: ## 📥 Restaurar backup (uso: make restore file="backup.sql")
	@if [ -z "$(file)" ]; then echo "❌ Especifica el archivo: make restore file=backup.sql"; exit 1; fi
	@echo "📥 Restaurando backup: $(file)"
	docker compose exec -T mariadb mysql -u root -p$(shell grep MARIADB_ROOT_PASSWORD .env | cut -d '=' -f2) < backups/$(file)
	@echo "✅ Backup restaurado"

# =============================================================================
# INFORMACIÓN DEL SISTEMA
# =============================================================================

info: ## ℹ️ Información del sistema
	@echo ""
	@echo "🖥️  INFORMACIÓN DEL SISTEMA"
	@echo "=========================="
	@echo "Docker:" 
	@docker --version 2>/dev/null || echo "❌ Docker no encontrado"
	@echo "Docker Compose:" 
	@docker compose version 2>/dev/null || echo "❌ Docker Compose no encontrado"
	@echo ""
	@echo "📁 ESTADO DEL PROYECTO"
	@echo "===================="
	@if [ -f .env ]; then echo "✅ .env configurado"; else echo "❌ .env no encontrado - ejecuta: make setup"; fi
	@if [ -d src ] && [ "$(shell ls -A src 2>/dev/null)" ]; then echo "✅ Proyecto Laravel presente"; else echo "📁 Carpeta src/ vacía - Laravel se creará automáticamente"; fi
	@echo ""

# =============================================================================
# COMANDO POR DEFECTO
# =============================================================================

# Si ejecutan solo "make", mostrar ayuda
.DEFAULT_GOAL := help