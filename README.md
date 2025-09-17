# 🚀 INFOTEC - Sistema de Eventos Laravel

**Sistema automatizado de gestión de eventos desarrollado con Laravel 11 y MariaDB usando Docker Compose.**

✅ **Estado**: Funcionando completamente - Laravel 11 + MariaDB + API REST en http://localhost:8000

## 📊 Arquitectura del Sistema

### 🏗️ Diagrama de Base de Datos

![Diagrama de Modelos INFOTEC](https://www.plantuml.com/plantuml/svg/pLRDRkCs4BxhAQP6WRNHA2aMs4kG6gjQp4Ae8xcsijW01G9QcdY9ogHAqkukaW3jfRTUYfvwQ-yzzH7o9liabMH6fBrnwXG6sW21GNxVS3ZV_50lbQPIB-O5HF5faf81d8aS2w5WI2LTOk5zakCLumWaJgFq0hA2AjLkZiRHMJ2-kFoANC39j7-IYKB8OubvlwMS9cCIlOetADDYWPPp7aTVdnC7dab4Rl4e3iaR1nQIyfbZdv8tAHYiNCYog31FCrrW6vQ_6HYy1wA-M-2SGexm9LLO_uPK2-Lvp-2BFVvvpnhrmY0a4pY2ioGamsIoRoUUoH1P8jS2hZq0M4iGo-4Ofcp6kEu-_xm7Yl7gVyP5pJGQLw8j2b7nbbHcRwdiFd_nejVWZSOvgaooCcE2LnoDxxHhV8MLoINZhC8hk5b-15S9MyCMKvPHS-17Jds_-SaaKetv9TMrLpP7fUcyN9cN-JR8zs6jdCOL9bbM-q9rV7BKOFrx7nz--CD4NqMGuxjsqudAG00EQ6BQCEgwLWUMrhlCnBnSeDB2tj5sn1WBkkL-dm5LJ6da6bMtrmIB75zJoOGoX59m2vSeAp9c61ZERLiXenNloIN2nNmgSMjnJ9cOINh5w5ffe2enOxHWESttcU8douTDN_oZE85HUP_ocFc6SygAXt2D1Lu9BXx0tFbfGhZSUet_ecVkVekZGGBT9hW3UyLUonYSEXV_yDClPgKEg-KWc0o2CB2d_Ho7qO1OWt-Pveqic_pQyNZV0YSdAPqM54PiAJJs-qzD-jFJungOXlr_9hIDvi3UqytgC7XDwcZkVen9i7E6D-pQeusXMJwXDbp47bObVF-F-9WCWq6Kn6J_R_SpEEV2f_vg71sRAgqbiGD9UMRtviRtnRK5u1Wwpclm3Uykk57f09RDdlDuz3grknNr8O-_clTXqv_JESPdcuYEjuxT2j-_kG67QZFJU1_U_ScHAiWHseAy-ulNwq51bmYdGjxzNb4y6wGvrDp9TLy5J0esPvokJa4E6LKPpMaLw_xBO934wJWP1c7LoHEu01A7eoIAqma4esZlbL7Ix5iwG-WC1DTI53GN4bNjgcE6LVD9RdGnf0Ab0LT3iVauQMRYAvB24ItPaMbHXwIqaDYGHibaE-kj-BxxASiVEkpeckMtbclcqZrxTFuuEwyhGRo_fuTaI5AonUBMiw7RHjWzUjiEZmjWYOzhu39tbS4QxAw4DTecXccwtQKe1Tz524lRBeFXxIw2eUyimHQJs-Pztso0myE-Corcg3GJd7RiIDdWjllhT5TGIpQxwrJl9V9yCI_-1W00)

### 🎯 Funcionalidad 

- **Gestión de Eventos**: Crear, editar y eliminar eventos con fechas y ubicaciones
- **Registro de Ponentes**: Administrar ponentes con biografías y especialidades
- **Control de Asistentes**: Registro único por evento con validación de email
- **API REST**: Endpoints completos para todas las entidades
- **Base de datos**: MariaDB con relaciones y restricciones de integridad

## ✨ Configuración Automática

- 🏗️ **Laravel 11** completamente configurado
- 🗄️ **MariaDB** con conexión automática y optimizada
- 🔄 **Migraciones** ejecutadas automáticamente
- 📦 **Dependencias** instaladas con Composer
- 🚀 **Servidor** listo en puerto 8000
- ⚙️ **Entorno** configurado con variables seguras

## ⚡ Inicio Rápido

### Requisitos
- Docker Desktop instalado en local o uso de GitHub Codespaces

### Iniciar el Sistema en local

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
docker compose exec laravel php artisan make:model Evento -mcr --api
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
# Iniciar
docker compose up -d

# Detener
docker compose -v

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
MARIADB_DATABASE
MARIADB_PASSWORD
MARIADB_ROOT_PASSWORD
MARIADB_USER

# Laravel
DB_CONNECTION
DB_HOST
DB_PASSWOR
DB_PORT
DB_USERNAME

# Otras
COMPOSE_PROJECT_NAME
LARAVEL_VERSION
```

## 🌐 GitHub Codespaces

**Uso en Codespaces:**

1. Abre el repositorio en Codespaces (se configura automáticamente con devcontainer.json)
2. Ejecuta: `docker compose up -d`
3. Codespaces detectará automáticamente el puerto 8000

### Secrets (Opcional)

En `Settings → Secrets and variables → Codespaces`: Variables de entorno.

## 🐳 Servicios Docker

| Servicio    | Descripción | Puerto       | Estado            |
|-------------|-------------|--------------|----- -------------|
| **laravel** | API Laravel + PHP 8.3      | 8000 | 🟢 Activo |
| **mariadb** | Base de datos MariaDB 11.4 | 3306 | 🟢 Activo |

## 🔄 Proceso de Inicialización

Al ejecutar `docker compose -d`, el sistema:

1. ✅ Inicia **MariaDB** con verificación de salud
2. ✅ **Crea Laravel 11** si es necesario
3. ✅ **Isntala dependencias** automáticamente
4. ✅ **Configura entorno** (.env con credenciales DB o secrets de Codespaces)
5. ✅ **Ejecuta migraciones** de base de datos
6. ✅ **Inicia servidor** en puerto 8000

## 🛠️ Solución de Problemas

### Verificación 

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
