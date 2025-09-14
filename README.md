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

### ⏳ **MÁXIMA SIMPLICIDAD - 2 COMANDOS**

```bash
# 1. Configurar entorno (una sola vez)
cp .env.example .env
# (Opcional: editar .env con tus credenciales de base de datos preferidas)

# 2. Iniciar todo - Laravel se crea automáticamente
docker compose up -d

# ¡Eso es todo! 🎉 Laravel ejecutándose en http://localhost:8000
```

### 🏗️ **Qué Sucede Automáticamente con `docker compose up`:**

1. ✅ **Inicia MariaDB** con verificaciones de salud
2. ✅ **Detecta si src/ está vacía**
3. ✅ **Descarga e instala Laravel 11.x** (solo si es necesario)
4. ✅ **Instala dependencias** con Composer
5. ✅ **Configura la conexión** a la base de datos
6. ✅ **Genera la APP_KEY** de Laravel
7. ✅ **Ejecuta las migraciones** de base de datos
8. ✅ **Inicia el servidor** de desarrollo de Laravel

## 📋 Comandos Adicionales (Opcionales)

```bash
# Detener servicios
docker compose down

# Ver registros
docker compose logs laravel

# Reiniciar completamente
docker compose down -v
docker compose up -d
```

## 🗂️ Estructura del Proyecto

```
infotec/
├── src/                    # Laravel (creado automáticamente con docker compose up)
├── docker-compose.yml     # Configuración principal - TODO EN UNO
├── .env                   # Variables de entorno (copiar de .env.example)
├── .env.example           # Plantilla de configuración
├── .gitignore             # Archivos a ignorar en Git
├── .dockerignore          # Archivos a ignorar en Docker
└── README.md              # Documentación
```

## 🐳 Servicios Docker

| Servicio | Descripción | Puerto |
|----------|-------------|--------|
| **laravel** | Aplicación Laravel con PHP | 8000 |
| **mariadb** | Servidor de base de datos | 3306 |

## 🛠️ Comandos Útiles de Desarrollo

```bash
# Acceder al contenedor Laravel
docker compose exec laravel bash

# Ejecutar comandos artisan
docker compose exec laravel php artisan migrate
docker compose exec laravel php artisan make:controller HomeController
docker compose exec laravel php artisan tinker

# Ver registros en tiempo real
docker compose logs -f laravel
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
# Ver los registros para diagnóstico
docker compose logs laravel

# Reiniciar servicios
docker compose restart laravel
```

### ¿Problemas de conexión a la base de datos?
```bash
# Verificar registros de MariaDB
docker compose logs mariadb

# Verificar variables de entorno
cat .env
```

### ¿Reinicio completo?
```bash
# Eliminar todo y empezar de cero
docker compose down -v
docker compose up -d
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

## 🌐 **GitHub Codespaces (Recomendado)**

### ⏳ **Setup con Codespaces Secrets:**
1. **Configurar secrets** en: `Settings → Secrets and variables → Codespaces`
2. **Agregar variables**:
   ```
   MARIADB_DATABASE = infotec_laravel
   MARIADB_USER = usuario_laravel
   LARAVEL_VERSION = 11.*
   ```
3. **Agregar secrets**:
   ```
   MARIADB_PASSWORD = tu_password_seguro
   MARIADB_ROOT_PASSWORD = root_password
   ```
4. **Abrir Codespace** - ¡Todo se configura automáticamente!
5. **Ejecutar**: `docker compose up -d`

### ✨ **Ventajas de Codespaces:**
- ✅ **Sin configuración manual** de `.env`
- ✅ **Secrets seguros** nunca en código
- ✅ **Colaboración fácil** con el equipo
- ✅ **Entorno consistente** para todos

---

## 🔒 Notas de Seguridad

- ⚠️ **Nunca commitear `.env`** - Contiene credenciales sensibles
- 🔑 **Usar Codespaces Secrets** para credenciales en la nube
- 🏠 **Solo desarrollo** - Este entorno es para desarrollo, no producción


## 🔗 Enlaces Útiles

- [Documentación Laravel](https://laravel.com/docs)
- [Documentación Docker Compose](https://docs.docker.com/compose/)
- [Documentación MariaDB](https://mariadb.org/documentation/)

---

**¡Feliz programación!** 🚀 Si encuentras algún problema, revisa los logs o crea un issue en el repositorio.
