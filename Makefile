.PHONY: up down composer migrate key

up:
    docker compose up -d

down:
    docker compose down -v

composer:
    docker compose run --rm composer

key:
    docker compose exec application php artisan key:generate

migrate:
    docker compose exec application php artisan migrate --force --seed