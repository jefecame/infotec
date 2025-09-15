# Dockerfile.app - imagen ligera basada en la imagen oficial usada anteriormente
FROM bitnami/laravel:latest

# Usar el mismo usuario que usan las imágenes bitnami para evitar problemas de permisos
USER 1001
WORKDIR /app

# Exponer puerto en caso de que la app sirva con `php artisan serve`
EXPOSE 8000

# No ejecutamos composer install aquí porque el volumen monta el código
# y composer se ejecutará en postCreateCommand del devcontainer.
# Mantener el comando por defecto ligero; Codespaces/compose arrancará los servicios.
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
