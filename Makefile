.PHONY: help start stop restart logs shell artisan clean status

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
	@echo "make start       - Iniciar entorno (crea Laravel automaticamente)"
	@echo "make stop        - Detener servicios"
	@echo "make restart     - Reiniciar servicios"
	@echo "make logs        - Ver registros de Laravel"
	@echo "make shell       - Acceder al contenedor Laravel"
	@echo "make artisan CMD - Ejecutar comando artisan (ej: make artisan migrate)"
	@echo "make clean       - Eliminar todo (contenedores y datos)"
	@echo "make status      - Mostrar estado de contenedores"
	@echo ""
	@echo "🌐 Después de 'make start', abrir: http://localhost:8000"

# Iniciar entorno completo (crea Laravel si es necesario)
start:
	@echo "🚀 Iniciando entorno Laravel Infotec..."
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

# Mostrar estado
status:
	@echo "📈 Estado de los contenedores:"
	docker compose ps
