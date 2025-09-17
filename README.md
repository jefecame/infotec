# 🚀 INFOTEC - Sistema de Eventos Laravel

**Sistema automatizado de gestión de eventos desarrollado con Laravel 11 y MariaDB usando Docker Compose. Configuración completa lista para desarrollo con un solo comando.**

✅ **Estado**: Funcionando completamente - Laravel 11 + MariaDB + API REST en http://localhost:8000

## 📊 Arquitectura del Sistema

### 🏗️ Diagrama de Base de Datos

![Diagrama de Modelos INFOTEC](https://www.plantuml.com/plantuml/svg/ZP9DRjim48NtFeMNMrWfUhOXGrjqh39AXcjqwJccKaRZ8dNgQlQO7xywdyQeEoAK7sEURxTpNl_3nM6pYHKA0KrQdQ9LGhq3CqwdY1bfXmK5mYjBm9zOZoY9f6cZ_4Q9e5PgjgZZP4nCbEQHXIc8PjUbGX2oNK8nGM5a7nv9iIa49Jgr6qNE8N8fO9W9cJKQ9Gs5QOo)

> **Diagrama en vivo**: [Ver diagrama completo en PlantUML](docs/models-diagram-basic.puml) 📁

### 🎯 Funcionalidad Principal
- **Gestión de Eventos**: Crear, editar y eliminar eventos con fechas y ubicaciones
- **Registro de Ponentes**: Administrar ponentes con biografías y especialidades
- **Control de Asistentes**: Registro único por evento con validación de email
- **API REST**: Endpoints completos para todas las entidades
- **Base de datos**: MariaDB con relaciones optimizadas y restricciones de integridad

## ✨ Configuración Automática

- 🏗️ **Laravel 11** completamente configurado
- 🗄️ **MariaDB** con conexión automática y optimizada
- 🔄 **Migraciones** ejecutadas automáticamente
- 📦 **Dependencias** instaladas con Composer
- 🚀 **Servidor** listo en puerto 8000
- ⚙️ **Entorno** configurado con variables seguras

## ⚡ Inicio Rápido

### Requisitos
- Docker Desktop instalado

### Iniciar el Sistema

```bash
# 1. Configurar entorno
cp .env.example .env

# 2. Iniciar servicios
docker compose up -d

# 3. Verificar
docker compose ps
```

**¡Listo!** Accede a http://localhost:8000 - Laravel se configura automáticamente.

## 📂 Estructura del Proyecto

```
infotec/
├── 📁 src/                # Aplicación Laravel 11
│   ├── app/Models/        # Modelos: Evento, Ponente, Asistente
│   ├── app/Http/Controllers/Api/  # Controladores API REST
│   ├── database/migrations/       # Estructura de base de datos
│   ├── routes/api.php     # Rutas API (/api/eventos, /api/ponentes)
│   └── artisan            # CLI de Laravel
├── 📁 docs/               # Documentación y diagramas
│   └── models-diagram-basic.puml  # Diagrama PlantUML
├── 📁 database/           # Scripts SQL y datos de prueba
├── 🐳 docker-compose.yml  # Orquestación de servicios
└── 📄 README.md           # Esta documentación
```

## 🔧 Comandos Útiles

### Desarrollo
```bash
# Acceder al contenedor
docker compose exec laravel bash

# Comandos Artisan frecuentes
docker compose exec laravel php artisan migrate
docker compose exec laravel php artisan make:model Evento
docker compose exec laravel php artisan make:controller Api/EventoController

# Instalar dependencias
docker compose exec laravel composer install
```

### Monitoreo
```bash
# Ver logs
docker compose logs -f laravel
docker compose logs -f mariadb

# Estado de servicios
docker compose ps
```

### Control
```bash
# Detener
docker compose down

# Reiniciar completo
docker compose down -v && docker compose up -d
```

## 🌐 API REST Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/eventos` | Listar todos los eventos |
| POST | `/api/eventos` | Crear nuevo evento |
| GET | `/api/eventos/{id}` | Obtener evento específico |
| PUT | `/api/eventos/{id}` | Actualizar evento |
| DELETE | `/api/eventos/{id}` | Eliminar evento |
| GET | `/api/ponentes` | Listar ponentes |
| POST | `/api/ponentes` | Crear ponente |
| GET | `/api/asistentes` | Listar asistentes |
| POST | `/api/asistentes` | Registrar asistente |

### Ejemplo de uso:
```bash
# Crear evento
curl -X POST http://localhost:8000/api/eventos \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Conferencia Tech","fecha_inicio":"2024-01-15","ubicacion":"Auditorio Central"}'

# Listar eventos
curl http://localhost:8000/api/eventos
```

## ⚙️ Variables de Entorno

```bash
# Base de datos
MARIADB_DATABASE=infotec_laravel
MARIADB_USER=usuario_laravel
MARIADB_PASSWORD=mi_password_seguro_123

# Laravel
DB_CONNECTION=mysql
DB_HOST=mariadb
DB_PORT=3306
```

## 🌐 GitHub Codespaces

**Uso en Codespaces:**
1. Abre el repositorio en Codespaces
2. Ejecuta: `docker compose up -d`
3. Codespaces detectará automáticamente el puerto 8000

### Secrets (Opcional)
En `Settings → Secrets and variables → Codespaces`:
```
MARIADB_PASSWORD = tu_password_seguro
MARIADB_ROOT_PASSWORD = tu_root_password
```

## 🐳 Servicios Docker

| Servicio | Descripción | Puerto | Estado |
|----------|-------------|--------|--------|
| **laravel** | API Laravel + PHP 8.3 | 8000 | 🟢 Activo |
| **mariadb** | Base de datos MariaDB 11.4 | 3306 | 🟢 Activo |

## 🔄 Proceso de Inicialización

Al ejecutar `docker compose up`, el sistema:

1. ✅ Inicia **MariaDB** con verificación de salud
2. ✅ **Crea Laravel 11** si es necesario
3. ✅ **Instala dependencias** automáticamente
4. ✅ **Configura entorno** (.env con credenciales DB)
5. ✅ **Ejecuta migraciones** de base de datos
6. ✅ **Inicia servidor** en puerto 8000

## 🛠️ Solución de Problemas

### Verificación Rápida
```bash
# Estado de servicios
docker compose ps

# Probar API
curl http://localhost:8000/api/eventos

# Ver logs si hay problemas
docker compose logs -f laravel
```

### Reinicio Completo
```bash
# Reiniciar todo (mantiene datos)
docker compose restart

# Reinicio limpio (borra todo)
docker compose down -v && docker compose up -d
```

## 📚 Recursos Adicionales

- 📖 [Documentación Laravel](https://laravel.com/docs)
- 🐳 [Docker Compose](https://docs.docker.com/compose/)
- 🎨 [PlantUML](https://plantuml.com/) - Diagramas como código
- 🌐 [GitHub Codespaces](https://github.com/features/codespaces)

## 🔒 Seguridad

- ⚠️ Nunca subir archivos `.env` al repositorio
- 🏠 Este entorno es solo para desarrollo
- 🔑 Usar Codespaces Secrets para credenciales

---

**🚀 Un comando, sistema completo:** `docker compose up -d`
