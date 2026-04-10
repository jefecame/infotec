# INFOTEC Copilot Instructions

This directory contains documentation for AI assistants working on the INFOTEC Laravel project. These guides help ensure consistency and efficiency across sessions.

## Quick Navigation

### 📖 Core Documentation

- **[copilot-instructions.md](./copilot-instructions.md)** — START HERE
  - Quick start & Docker setup
  - Build, test, lint commands
  - System architecture & entity relationships
  - API routes and controller patterns
  - Key conventions and gotchas
  - Database structure and migrations

### 🚀 Advanced Topics

- **[development-workflow.md](./development-workflow.md)**
  - IDE setup recommendations
  - Git workflow & best practices
  - Step-by-step guides for common tasks
  - Debugging workflows and techniques
  - Performance optimization
  - Troubleshooting guide
  - Code quality standards

### 🔌 Configuration

- **[mcp-config.md](./mcp-config.md)**
  - Setting up MCP servers (Database)
  - Direct database access methods
  - Query examples

## For New Sessions

1. Read the **Quick Start** section in [copilot-instructions.md](./copilot-instructions.md)
2. Familiarize yourself with the **Architecture** section
3. Check **Key Conventions** for codebase-specific patterns
4. Use [development-workflow.md](./development-workflow.md) when:
   - Adding new models/controllers
   - Debugging issues
   - Setting up your environment
   - Looking for best practices

## TL;DR

**This is a Laravel 11 API** (no frontend templates) with:
- **Database**: MariaDB in Docker Compose
- **Main entities**: Evento (Event), Ponente (Speaker), Asistente (Attendee)
- **Key relationship**: Many-to-many between Evento and Ponente
- **Authentication**: Protected write operations with Passport
- **Testing**: PHPUnit with Feature & Unit test suites

All development happens in Docker containers. No local PHP setup required.

```bash
cp .env.example .env
docker compose up -d
# Visit http://localhost:8000/api/eventos
```

## Key File Locations

```
src/
├── app/Models/              # Evento, Ponente, Asistente
├── app/Http/Controllers/    # REST API controllers
├── routes/api.php           # API route definitions
├── database/migrations/     # Schema changes
├── tests/Feature/           # HTTP endpoint tests
├── tests/Unit/              # Model & logic tests
└── config/                  # Laravel configuration

Dockerfile                   # Docker image definition
docker-compose.yml          # Service orchestration
.github/                    # This documentation
```

## Most Common Tasks

### Running Tests
```bash
docker compose exec laravel php artisan test
```

### Creating New Model
```bash
docker compose exec laravel php artisan make:model YourModel -mcr --api
```

### Formatting Code
```bash
docker compose exec laravel php artisan pint
```

### Accessing Database
```bash
docker compose exec laravel php artisan tinker
```

### Checking Service Status
```bash
docker compose ps
```

## Important Notes

- **Never commit `.env`** — Use `.env.example` as template
- **Docker volumes mount `src/` live** — Changes reflect immediately
- **Tests use SQLite by default** — MariaDB isn't needed for testing
- **Migrations run automatically** — On container startup
- **Seeders run automatically** — InitialSeeder runs with migrations

## Extending These Docs

When you discover:
- **Codebase patterns** not documented here
- **Common errors** and their solutions
- **Best practices** specific to this project
- **Performance tips**

Please add them to the appropriate guide so future sessions benefit.

---

**Last updated**: 2026-03-22
**Project**: INFOTEC - Event Management System
**Framework**: Laravel 11
**Database**: MariaDB 11.4
**Deployment**: Docker Compose
