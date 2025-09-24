# Dockerfile personalizado para Laravel
FROM bitnami/laravel:latest

# Copia el script de inicio personalizado
COPY /src/scripts/laravel-startup.sh /app/scripts/laravel-startup.sh

# Da permisos de ejecución al script
RUN chmod +x /app/scripts/laravel-startup.sh

# Puedes instalar dependencias adicionales aquí si lo necesitas
RUN apt-get update && apt-get install -y unzip

# Actualiza Composer a su última versión
RUN composer self-update

# Actualiza npm a su última versión
RUN npm install -g npm@latest

# Instala las dependencias de Composer
RUN composer update

# Instala las dependencias de npm
RUN npm install

# Actualiza las dependencias de npm
RUN npm update

# Comando de inicio
CMD ["/bin/bash", "/app/scripts/laravel-startup.sh"]
