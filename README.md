# Infotec - Desarrollo con Docker

Pasos rápidos (carpeta limpia):

1. Copiar `.env.example` -> `.env` y rellenar valores sensibles.
2. Crear carpeta src/ con tu proyecto Laravel o clonar el repo allí.
3. Levantar servicios:
   docker compose up -d
4. Instalar dependencias (popula volumen vendor_data):
   docker compose run --rm composer
5. Generar APP_KEY y migrar:
   docker compose exec application php artisan key:generate
   docker compose exec application php artisan migrate --force --seed
6. En el host abrir: http://localhost:8000

Notas:
- No commitees `.env`.
- Si `src/` monta tu app, asegúrate de que `src/vendor` no exista o esté en el volumen nombrado.