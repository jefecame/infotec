.PHONY: help init up down restart logs shell composer artisan clean status

# Default target
help:
	@echo "🚀 Infotec Laravel Docker Commands"
	@echo "====================================="
	@echo "make init        - Initialize Laravel project and start services"
	@echo "make up          - Start all services"
	@echo "make down        - Stop all services"
	@echo "make restart     - Restart all services"
	@echo "make logs        - View application logs"
	@echo "make shell       - Access Laravel container shell"
	@echo "make composer    - Run composer install"
	@echo "make artisan CMD - Run artisan command (e.g., make artisan migrate)"
	@echo "make clean       - Stop services and remove all data"
	@echo "make status      - Show running containers"

# Initialize project (create Laravel if needed, then start services)
init:
	@echo "🏗️  Initializing Laravel project..."
	@if [ ! -f "src/composer.json" ]; then \
		echo "📁 Creating new Laravel project..."; \
		docker compose --profile init up --build laravel-init; \
	fi
	@echo "🐳 Starting services..."
	@docker compose up -d --build
	@echo "✅ Setup completed! Application available at: http://localhost:8000"

# Start services
up:
	docker compose up -d

# Stop services
down:
	docker compose down

# Restart services
restart: down up

# View logs
logs:
	docker compose logs -f application

# Access container shell
shell:
	docker compose exec application bash

# Run composer install
composer:
	docker compose --profile tools run --rm composer

# Run artisan commands
artisan:
	docker compose exec application php artisan $(CMD)

# Clean up everything
clean:
	docker compose down -v --remove-orphans
	docker system prune -f

# Show status
status:
	docker compose ps
