# 🚀 INFOTEC - Laravel Automático con Docker

**Configuración Docker Compose que crea e inicializa automáticamente una instalación fresca de Laravel en una carpeta `src/` vacía.**

## ✨ Lo que hace automáticamente

- 🏗️ **Crea Laravel** si la carpeta `src/` está vacía
- 🗄️ **Configura MariaDB** con conexión automática
- ⚙️ **Genera APP_KEY** y configura el entorno
- 🔄 **Ejecuta migraciones** de base de datos
- 🚀 **Inicia el servidor** de desarrollo

## ⚡ Inicio Rápido

### Requisitos
- Docker Desktop instalado y ejecutándose

### Usar el workspace

```bash
# 1. Configurar variables de entorno (una sola vez)
cp .env.example .env

# 2. Iniciar Laravel automáticamente
docker compose up -d

# ✅ ¡Listo! Laravel en http://localhost:8000
```

**Eso es todo.** Laravel se creará automáticamente la primera vez.

## 📂 Estructura del Proyecto

```
infotec/
├── src/                    # Laravel (se crea automáticamente)
├── docker-compose.yml     # Configuración principal
├── .env.example           # Plantilla de variables
└── README.md              # Esta documentación
```

## 🔧 Comandos Útiles

```bash
# Ver logs de Laravel
docker compose logs -f laravel

# Ver logs de MariaDB
docker compose logs -f mariadb

# Acceder al contenedor Laravel
docker compose exec laravel bash

# Detener servicios
docker compose down

# Limpiar todo y empezar de cero
docker compose down -v
docker compose up -d
```

## ⚙️ Configuración

Las variables en `.env` que puedes personalizar:

```bash
# Base de datos
MARIADB_DATABASE=infotec_laravel
MARIADB_USER=usuario_laravel
MARIADB_PASSWORD=mi_password_seguro_123
MARIADB_ROOT_PASSWORD=root_password_456

# Laravel
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

## 🔄 Proceso Automático

Cuando ejecutas `docker compose up`:

1. ✅ **Inicia MariaDB** con verificación de salud
2. ✅ **Verifica** si existe proyecto Laravel en `src/`
3. ✅ **Crea Laravel** automáticamente si `src/` está vacía
4. ✅ **Instala dependencias** con Composer
5. ✅ **Configura conexión** a MariaDB
6. ✅ **Genera APP_KEY** de Laravel
7. ✅ **Ejecuta migraciones** de base de datos
8. ✅ **Inicia servidor** en http://localhost:8000

## 🛠️ Solución de Problemas

### Laravel no se creó
```bash
# Ver logs para diagnosticar
docker compose logs laravel
```

### Error de conexión a base de datos
```bash
# Verificar estado de MariaDB
docker compose logs mariadb
```

### Reinicio completo
```bash
# Eliminar todo y empezar desde cero
docker compose down -v
docker compose up -d
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
