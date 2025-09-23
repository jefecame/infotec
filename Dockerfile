# Dockerfile personalizado para Laravel
FROM bitnami/laravel:11

# Copia el script de inicio personalizado
COPY /src/scripts/laravel-startup.sh /app/scripts/laravel-startup.sh

# Da permisos de ejecución al script
RUN chmod +x /app/scripts/laravel-startup.sh

# Puedes instalar dependencias adicionales aquí si lo necesitas
RUN npm install -g npm@latest

RUN apt-get update && apt-get install -y unzip

#RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=

# Comando de inicio
CMD ["/bin/bash", "/app/scripts/laravel-startup.sh"]
