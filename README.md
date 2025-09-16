# 🚀 INFOTEC - Laravel Automático con Docker

**Configuración Docker Compose completamente funcional que crea e inicializa automáticamente una instalación fresca de Laravel 11 con MariaDB en una carpeta `src/` vacía.**

✅ **Estado actual**: Sistema funcionando al 100% - Laravel 11 con MariaDB se crea automáticamente y responde en http://localhost:8000

🗄️ **Base de datos**: Configurado para usar **MariaDB** (no SQLite) con conexión automática y migraciones ejecutándose correctamente.

## ✨ Lo que hace automáticamente

- 🏗️ **Crea Laravel 11** completo si la carpeta `src/` está vacía
- 🗄️ **Configura MariaDB** con conexión automática (no SQLite)
- ⚙️ **Genera APP_KEY** único y configura el entorno
- 🔄 **Ejecuta migraciones** de base de datos automáticamente
- 📦 **Instala dependencias** Composer con optimización
- 🚀 **Inicia el servidor** de desarrollo en puerto 8000
- 🔧 **Configura permisos** de storage y cache

## ⚡ Inicio Rápido

### Requisitos
- Docker Desktop instalado y ejecutándose

### Usar el workspace

```bash
# 1. Configurar variables de entorno (una sola vez)
cp .env.example .env

# 2. Iniciar Laravel automáticamente
docker compose up -d

# 3. Verificar que todo funciona
docker compose ps
curl http://localhost:8000

# ✅ ¡Listo! Laravel en http://localhost:8000
```

**Eso es todo.** Laravel se creará automáticamente la primera vez con todas las dependencias instaladas.

## 📂 Estructura del Proyecto

```
infotec/
├── src/                    # Laravel 11 (se crea automáticamente)
│   ├── app/               # Lógica de la aplicación
│   ├── database/          # Migraciones y seeders
│   ├── resources/         # Vistas y assets
│   ├── routes/            # Definición de rutas
│   ├── artisan            # CLI de Laravel
│   └── composer.json      # Dependencias PHP
├── .devcontainer/         # Configuración para Codespaces
├── docker-compose.yml     # Configuración principal
├── .env.example           # Plantilla de variables
└── README.md              # Esta documentación
```

## 🔧 Comandos Útiles

### Monitoreo y Logs
```bash
# Ver logs de Laravel
docker compose logs -f laravel

# Ver logs de MariaDB
docker compose logs -f mariadb

# Ver estado de los servicios
docker compose ps
```

### Desarrollo Laravel
```bash
# Acceder al contenedor Laravel
docker compose exec laravel bash

# Ejecutar comandos Artisan
docker compose exec laravel php artisan migrate
docker compose exec laravel php artisan make:controller HomeController
docker compose exec laravel php artisan make:model User

# Instalar dependencias Composer
docker compose exec laravel composer install
```

### Control de Servicios
```bash
# Detener servicios
docker compose down

# Reiniciar solo Laravel
docker compose restart laravel

# Limpiar todo y empezar de cero
docker compose down -v
docker compose up -d
```

## ⚙️ Configuración

Las variables en `.env` que puedes personalizar:

```bash
# Base de datos MariaDB
MARIADB_DATABASE=infotec_laravel
MARIADB_USER=usuario_laravel
MARIADB_PASSWORD=mi_password_seguro_123
MARIADB_ROOT_PASSWORD=root_password_456

# Laravel - Configuración de base de datos
DB_CONNECTION=mysql
DB_HOST=mariadb
DB_PORT=3306
DB_DATABASE=infotec_laravel
DB_USERNAME=usuario_laravel
DB_PASSWORD=mi_password_seguro_123

# Laravel - General
LARAVEL_VERSION=11.*
```

## 🌐 GitHub Codespaces

Este workspace está optimizado para Codespaces. Simplemente:

1. **Abre el repositorio en Codespaces**
2. **Ejecuta:** `docker compose up -d`
3. **¡Listo!** Codespaces detectará el puerto 8000 automáticamente

### Configuración con Secrets (Opcional)

En `Settings → Secrets and variables → Codespaces`:

```
MARIADB_DATABASE = tu_base_datos
MARIADB_USER = tu_usuario
MARIADB_PASSWORD = tu_password_seguro
MARIADB_ROOT_PASSWORD = tu_root_password
```

```

## 🐳 Servicios Docker

| Servicio | Descripción | Puerto |
|----------|-------------|---------|
| **laravel** | Aplicación Laravel + PHP | 8000 |
| **mariadb** | Base de datos MariaDB | 3306 |

## 🔄 Proceso Automático Mejorado

Cuando ejecutas `docker compose up`, el sistema automáticamente:

1. ✅ **Inicia MariaDB** con verificación de salud
2. ✅ **Verifica conectividad** de red con netcat (nc)
3. ✅ **Detecta estado** del directorio `src/` (vacío o parcial)
4. ✅ **Crea Laravel 11** si es necesario usando Composer
5. ✅ **Instala dependencias** con optimización
6. ✅ **Configura entorno** (.env con credenciales de DB)
7. ✅ **Genera APP_KEY** único de Laravel
8. ✅ **Ejecuta migraciones** (con manejo de errores)
9. ✅ **Configura permisos** de storage y cache
10. ✅ **Inicia servidor** de desarrollo en puerto 8000

🔧 **Mejoras recientes**: 
- Configuración automática de **MariaDB** (reemplaza SQLite por defecto)
- Detección de conectividad con **netcat** más confiable
- Variables de entorno de Laravel configuradas automáticamente
- Limpieza automática de instalaciones parciales
- Mejor manejo de errores en migraciones

## 🛠️ Solución de Problemas

### ❌ Laravel no se creó o no responde
```bash
# Verificar estado de contenedores
docker compose ps

# Ver logs detallados de Laravel
docker compose logs laravel

# Probar respuesta HTTP
curl http://localhost:8000

# Reinicio completo (solución más común)
docker compose down -v && docker compose up -d
```

### 🔌 Problemas de conectividad de base de datos
```bash
# Verificar estado de MariaDB
docker compose logs mariadb

# Probar conectividad de red
docker compose exec laravel nc -z mariadb 3306

# Verificar configuración de BD en Laravel
docker compose exec laravel bash -c "cat .env | grep -E 'DB_|APP_KEY'"

# Verificar estado de migraciones
docker compose exec laravel php artisan migrate:status

# Probar conexión desde Laravel
docker compose exec laravel php artisan tinker --execute="echo 'DB: ' . DB::connection()->getPdo()->getAttribute(PDO::ATTR_CONNECTION_STATUS);"
```

### 🔄 Limpieza y reinicio
```bash
# Reinicio suave (mantiene datos)
docker compose restart

# Reinicio completo (elimina todo)
docker compose down -v && docker compose up -d

# Limpiar cachés de Laravel
docker compose exec laravel php artisan cache:clear
docker compose exec laravel php artisan config:clear
```

### ⚡ Verificación rápida
```bash
# Todo en uno: verificar que funciona
docker compose ps && curl -s -o /dev/null -w "%{http_code}" http://localhost:8000
# Debe mostrar contenedores "Up (healthy)" y código "200"
```

## 🔒 Notas de Seguridad

- ⚠️ **Nunca subir `.env`** al repositorio
- 🔑 **Usar Codespaces Secrets** para credenciales sensibles
- 🏠 **Solo desarrollo** - Este entorno es para desarrollo local y Codespaces

## 🔗 Enlaces Útiles

- [Documentación Laravel](https://laravel.com/docs)
- [Docker Compose](https://docs.docker.com/compose/)
- [GitHub Codespaces](https://github.com/features/codespaces)

---

**¡Un solo comando, Laravel listo!** 🚀 `docker compose up -d`
