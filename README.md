# 🚀 INFOTEC - Entorno de Desarrollo Laravel con Docker

Este entorno Docker Compose crea automáticamente una instalación fresca de Laravel en la carpeta `src/` vacía y configura un entorno completo de desarrollo con MariaDB.

## ✨ Características

- 🏗️ **Creación Automática de Laravel**: Crea un proyecto Laravel nuevo si `src/` está vacío
- 🐳 **Desarrollo con Docker**: Entorno completamente containerizado
- 🗄️ **Integración de Base de Datos**: MariaDB preconfigurado con migraciones automáticas
- 🔑 **Gestión de Variables**: Manejo seguro de credenciales
- 🛠️ **Herramientas Integradas**: Composer, Artisan, y más

## 🏃‍♂️ Inicio Rápido

### Requisitos Previos
- Docker Desktop instalado y en ejecución
- Git (opcional, para control de versiones)

### 🚀 Configuración en Un Comando

```bash
# 1. Copiar y configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de base de datos preferidas

# 2. Iniciar todo (crea Laravel + inicia servicios)
make start

# ¡Listo! Abrir http://localhost:8000
```

### 📝 Pasos Manuales Alternativos

```bash
# Opción 1: Usando Make (recomendado)
make start

# Opción 2: Usando Docker Compose directamente
docker compose up -d
```

**¡Es así de simple!** El sistema detecta automáticamente si necesita crear Laravel.

## 🗂️ Estructura del Proyecto

```
infotec/
├── src/                    # Aplicación Laravel (creada automáticamente)
├── docker-compose.yml     # Definición de servicios
├── .env                   # Variables de entorno (crear desde .env.example)
├── .env.example           # Plantilla de variables de entorno
├── Makefile               # Comandos simplificados
├── .gitignore             # Archivos a ignorar en Git
├── .dockerignore          # Archivos a ignorar en Docker
└── README.md              # Este archivo
```

## 🐳 Servicios Docker

| Servicio | Descripción | Puerto |
|----------|-------------|--------|
| **laravel** | Aplicación Laravel con PHP | 8000 |
| **mariadb** | Servidor de base de datos | 3306 |

## 🛠️ Comandos de Desarrollo

### Usando Make (Recomendado)
```bash
make help           # Mostrar todos los comandos disponibles
make start          # Iniciar entorno (crea Laravel automáticamente)
make stop           # Detener servicios
make restart        # Reiniciar servicios
make logs           # Ver registros de Laravel
make shell          # Acceder al contenedor Laravel
make artisan CMD    # Ejecutar comando artisan
make clean          # Eliminar todo (contenedores y datos)
make status         # Mostrar estado de contenedores
```

### Usando Docker Compose Directamente
```bash
# Ver registros
docker compose logs laravel

# Acceder al contenedor
docker compose exec laravel bash

# Ejecutar comandos artisan
docker compose exec laravel php artisan migrate
docker compose exec laravel php artisan make:controller HomeController
```

## 🤖 Funciones Automáticas

El entorno maneja automáticamente:

- ✅ **Instalación Laravel**: Crea Laravel 11.x si src/ está vacío
- ✅ **Configuración de BD**: Configura Laravel para usar MariaDB
- ✅ **Configuración del Entorno**: Genera APP_KEY y configura .env
- ✅ **Migraciones**: Ejecuta migraciones iniciales de base de datos
- ✅ **Dependencias**: Instala paquetes de Composer
- ✅ **Permisos**: Establece permisos correctos de archivos
- ✅ **Optimización**: Limpia y optimiza Laravel

## 🐛 Solución de Problemas

### ¿Laravel no se creó?
```bash
# Reiniciar servicios
make restart

# Ver registros para diagnosticar
make logs
```

### ¿¿Problemas de conexión a la base de datos?
```bash
# Verificar registros de MariaDB
docker compose logs mariadb

# Verificar variables de entorno
cat .env
```

### ¿Reinicio completo?
```bash
# Eliminar todo y empezar de cero
make clean
make start  # Reinicializar
```

## 📁 Variables de Entorno (.env)

```bash
# Variables de MariaDB
MARIADB_DATABASE=infotec_db
MARIADB_USER=usuario_laravel
MARIADB_PASSWORD=tu_password_seguro
MARIADB_ROOT_PASSWORD=root_password_seguro

# Configuración adicional
LARAVEL_VERSION=11.*
COMPOSE_PROJECT_NAME=infotec
```

## 🔒 Notas de Seguridad

- ⚠️ **Nunca commitear `.env`** - Contiene credenciales sensibles
- 🔑 **Cambiar passwords por defecto** en `.env` antes de producción
- 🏠 **Solo desarrollo** - Este entorno es para desarrollo, no producción

## 🔗 Enlaces Útiles

- [Documentación Laravel](https://laravel.com/docs)
- [Documentación Docker Compose](https://docs.docker.com/compose/)
- [Documentación MariaDB](https://mariadb.org/documentation/)

---

**¡Feliz programación!** 🚀 Si encuentras algún problema, revisa los logs o crea un issue en el repositorio.
