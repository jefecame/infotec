# 🚀 INFOTEC - Configuración Automática de Laravel con Docker

Este setup de Docker Compose **crea e inicializa automáticamente** una instalación fresca de Laravel en una carpeta `src/` vacía con **UN SOLO COMANDO**: `docker compose up`

## ✨ Características

- 🏗️ **Configuración Automática Real**: Crea el proyecto Laravel si `src/` está vacío
- ⚡ **Un Solo Comando**: `docker compose up` hace todo
- 🐳 **Desarrollo con Docker**: Completamente containerizado
- 🗄️ **Base de Datos Lista**: MariaDB con migraciones automáticas
- 🔑 **Configuración Automática**: Base de datos, claves y optimización
- 🛠️ **Optimizado para Rendimiento**: Volumen vendor persistente

## 🏃‍♂️ Inicio Rápido

### Requisitos Previos
- Docker Desktop instalado y en ejecución
- Git (opcional, para control de versiones)

### ⚡ **MÁXIMA SIMPLICIDAD - 2 COMANDOS**

```bash
# 1. Configurar entorno (una sola vez)
cp .env.example .env
# (Opcional: editar .env con tus credenciales de base de datos preferidas)

# 2. Iniciar todo (crea Laravel automáticamente si es necesario)
docker compose up -d

# ¡Eso es todo! 🎉 Laravel ejecutándose en http://localhost:8000
```

### 🏗️ **Qué Sucede Automáticamente:**
1. ✅ **Detecta la carpeta src/ vacía**
2. ✅ **Descarga e instala Laravel 11.x**
3. ✅ **Inicia MariaDB con verificaciones de salud**
4. ✅ **Configura la conexión a la base de datos**
5. ✅ **Genera la APP_KEY**
6. ✅ **Ejecuta las migraciones de base de datos** 
7. ✅ **Inicia el servidor de desarrollo de Laravel**

## 🟃‍♂️ Inicio Rápido

### Requisitos Previos
- Docker Desktop instalado y en ejecución
- Git (opcional, para control de versiones)

### 📝 Pasos Alternativos

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
├── scripts/                # Scripts de utilidad
│   └── verificar-entorno.sh   # Script de verificación completa
├── storage/                # Datos persistentes
│   └── mariadb/               # Datos MariaDB (generado automáticamente)
├── backups/                # Backups de base de datos
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
# COMANDOS PRINCIPALES
make help              # Mostrar todos los comandos disponibles
make start             # Iniciar entorno (crea Laravel automáticamente)
make stop              # Detener servicios
make restart           # Reiniciar servicios
make status            # Estado detallado con uso de recursos

# DESARROLLO
make shell             # Acceder al contenedor Laravel
make artisan CMD       # Ejecutar comando artisan (ej: make artisan migrate)
make composer-install  # Instalar dependencias PHP
make composer-update   # Actualizar dependencias PHP

# MONITOREO
make logs              # Ver registros de Laravel
make logs-db           # Ver registros de MariaDB

# MANTENIMIENTO
make backup            # Crear backup de base de datos
make check             # Verificar estado completo del entorno
make clean             # Eliminar todo (contenedores y datos)
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
# Verificar todo el entorno con un comando
make check

# Verificar registros de MariaDB
make logs-db
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
