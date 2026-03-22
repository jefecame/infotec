# Copilot Instructions for INFOTEC

INFOTEC is a **Laravel 11 event management system** running on Docker with MariaDB. All development happens in containers using Docker Compose.

## Quick Start

```bash
# Copy environment file (first time only)
cp .env.example .env

# Start all services
docker compose up -d

# System will auto-initialize: migrations, seeders, server on :8000
```

## Build, Test & Lint Commands

### Running Tests

```bash
# All tests (Unit + Feature)
docker compose exec laravel php artisan test

# Unit tests only
docker compose exec laravel php artisan test --testsuite=Unit

# Feature tests only
docker compose exec laravel php artisan test --testsuite=Feature

# Single test file
docker compose exec laravel php artisan test tests/Feature/EventoFeatureTest.php

# Single test method (add --filter)
docker compose exec laravel php artisan test --filter=test_can_list_eventos
```

### Linting & Code Quality

```bash
# Format code with Pint (Laravel's opinionated code formatter)
docker compose exec laravel php artisan pint

# Check formatting without changes
docker compose exec laravel php artisan pint --test
```

### Database & Development

```bash
# Access Laravel CLI
docker compose exec laravel bash

# Run migrations fresh
docker compose exec laravel php artisan migrate:fresh

# Run migrations with seeders
docker compose exec laravel php artisan migrate:fresh --seed

# Access Tinker REPL
docker compose exec laravel php artisan tinker

# View Laravel logs
docker compose logs -f laravel

# View database logs
docker compose logs -f mariadb
```

## Architecture

### System Overview

- **Framework**: Laravel 11 (API-focused, no Blade templates)
- **Database**: MariaDB 11.4
- **Frontend Build**: Vite with Tailwind CSS (configured but minimal in API)
- **Authentication**: Laravel Passport (OAuth 2.0)
- **Deployment**: Docker Compose with persistent volumes

### Core Entities

Three main models drive the system:

1. **Evento** (Event) - `app/Models/Evento.php`
   - Fields: `titulo`, `descripcion`, `fecha_inicio`, `fecha_fin`, `ubicacion`
   - Relations: Many asistentes (1:N), many ponentes (M:N via `evento_ponente` table)

2. **Ponente** (Speaker) - `app/Models/Ponente.php`
   - Fields: `nombre`, `apellido`, `especialidad`, `biografia`, `email`
   - Relations: Many eventos (M:N via `evento_ponente` table)

3. **Asistente** (Attendee) - `app/Models/Asistente.php`
   - Fields: `nombre`, `apellido`, `email`, `evento_id`
   - Relations: Belongs to evento (N:1)

### API Routes Structure

All routes in `routes/api.php`:

**Public endpoints** (no auth required):
- `GET /api/eventos` - List all events
- `GET /api/eventos/{id}` - Get event details
- `GET /api/ponentes` - List all speakers
- `GET /api/ponentes/{id}` - Get speaker details

**Protected endpoints** (require `auth:api` middleware):
- `POST /api/eventos` - Create event
- `PUT /api/eventos/{evento}` - Update event
- `DELETE /api/eventos/{id}` - Delete event
- `POST /api/ponentes` - Create speaker
- `PUT /api/ponentes/{ponente}` - Update speaker
- `DELETE /api/ponentes/{id}` - Delete speaker
- `GET /api/asistentes` - List attendees (auth required)
- `POST /api/asistentes` - Register attendee (auth required)
- `GET /api/asistentes/{id}` - Get attendee (auth required)
- `PUT /api/asistentes/{asistente}` - Update attendee (auth required)
- `DELETE /api/asistentes/{id}` - Delete attendee (auth required)

### Controllers Location

All controllers are in `app/Http/Controllers/`:
- `EventoController` - Handles event CRUD operations
- `PonenteController` - Handles speaker CRUD operations
- `AsistenteController` - Handles attendee operations

Controllers follow **REST conventions** with standard methods: `index`, `store`, `show`, `update`, `destroy`.

### Database Migrations

Migrations in `database/migrations/`:
- `2025_09_16_092109` - Create `eventos` table
- `2025_09_16_191846` - Create `ponentes` table
- `2025_09_16_191858` - Create `asistentes` table
- `2025_09_16_222355` - Create `evento_ponente` junction table (for M:N relationship)

Apply migrations with:
```bash
docker compose exec laravel php artisan migrate
```

### Seeders

`database/seeders/InitialSeeder.php` runs automatically on container startup. Create seeders with:
```bash
docker compose exec laravel php artisan make:seeder YourSeederName
```

## Key Conventions

### Model Fillable Arrays

All models use explicit `$fillable` arrays defining which attributes can be mass-assigned. When adding new columns, always add them to the model's fillable list:

```php
protected $fillable = ['campo1', 'campo2', 'campo3'];
```

### Relationships & Comments

Model relationships have inline documentation comments explaining the relationship type (1:N, M:N). Example:

```php
/**
 * Relación con Asistentes
 * Un evento tiene muchos asistentes
 */
public function asistentes()
{
    return $this->hasMany(Asistente::class);
}
```

### Controller Structure

Controllers use action-based naming with consistent patterns:
- `index()` - GET all records with optional filtering/pagination
- `show(id)` - GET single record
- `store()` - POST to create
- `update(model)` - PUT to update
- `destroy(id)` - DELETE

### File Organization

```
src/
├── app/
│   ├── Models/              # Data models with relationships
│   └── Http/Controllers/    # REST controllers (no subdirectories currently)
├── database/
│   ├── migrations/          # Database schema changes
│   └── seeders/            # Data fixtures
├── routes/
│   └── api.php             # All API routes (grouped by auth)
├── tests/
│   ├── Feature/            # Test complete features (e.g., API endpoints)
│   └── Unit/               # Test individual components (e.g., models)
└── config/                 # Laravel configuration files
```

### Testing Conventions

- **Feature tests**: Test HTTP endpoints, authentication, full request-response cycle
- **Unit tests**: Test model methods, business logic, relationships
- Test files follow model names: `EventoFeatureTest`, `EventoUnitTest`
- Use existing test files as templates for consistent patterns

### Environment Configuration

Laravel configuration files in `src/config/`. Key environment variables (in `.env`):

- `DB_CONNECTION=mysql` (MariaDB uses mysql driver)
- `DB_HOST=mariadb` (Docker Compose service name)
- `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD` - Set via `.env.example`
- `APP_KEY` - Generated automatically on first startup
- `CACHE_STORE=database` - Uses database for caching
- `QUEUE_CONNECTION=database` - Uses database for queues
- `SESSION_DRIVER=database` - Uses database for sessions

## Docker Compose Details

### Services

**laravel** container:
- Image: `bitnami/laravel:latest` (PHP 8.3)
- Volumes: `./src:/app` (live code editing)
- Ports: `8000:8000`
- Startup: Runs `scripts/laravel-startup.sh`
- Health check: HTTP GET to `/` every 30s

**mariadb** container:
- Image: `bitnami/mariadb:latest` (v11.4)
- Ports: `3306:3306`
- Volume: `mariadb_data` (persistent)
- Health check: `mysqladmin ping` every 10s

### Startup Script

`src/scripts/laravel-startup.sh` handles:
1. Wait for MariaDB health check
2. Create Laravel project if needed
3. Install Composer/npm dependencies
4. Configure `.env` from Docker environment variables
5. Generate `APP_KEY`
6. Create storage directories (Codespaces workaround)
7. Run migrations with `--force` flag
8. Run `InitialSeeder` for test data
9. Start development server on port 8000

The script is idempotent - it safely re-runs if container restarts.

### Persistent Data

- `mariadb_data` - Database files (survives `docker compose down`)
- `vendor_data` - Composer dependencies (optimization for Windows)
- `composer_cache` - Composer cache (faster install on rebuilds)

### Networking

Services communicate via `laravel-network` (bridge network). Use `mariadb` hostname from Laravel container.

## Common Tasks

### Creating New Models

```bash
docker compose exec laravel php artisan make:model YourModel -m
```

This creates:
- `app/Models/YourModel.php`
- `database/migrations/YYYY_MM_DD_HHMMSS_create_your_models_table.php`

Add relationships and `$fillable` immediately.

### Creating Controllers

```bash
docker compose exec laravel php artisan make:controller YourModelController
```

For REST API, implement: `index()`, `store()`, `show()`, `update()`, `destroy()`.

### Adding Database Columns

1. Create migration: `php artisan make:migration add_field_to_table`
2. Edit migration in `database/migrations/`
3. Run: `php artisan migrate`
4. Update model's `$fillable` array

### Testing API Endpoints

```bash
# Using curl (from host machine)
curl http://localhost:8000/api/eventos

# Using Tinker REPL (inside container)
docker compose exec laravel php artisan tinker
> App\Models\Evento::all();
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker compose logs laravel

# Verify database is healthy
docker compose ps

# Full restart with clean state (WARNING: loses data)
docker compose down -v && docker compose up -d
```

### Migrations fail

```bash
# Check database connection from container
docker compose exec laravel php artisan tinker
> DB::connection()->getPdo();  # Should return PDO object

# Manually re-run migrations
docker compose exec laravel php artisan migrate:fresh --seed
```

### Cache/view errors on Codespaces

Storage directories are auto-created by `laravel-startup.sh`. If issues persist:

```bash
docker compose exec laravel php artisan storage:link
docker compose exec laravel php artisan cache:clear
docker compose exec laravel php artisan view:clear
```

### Code changes not reflecting

Docker volume mounts `src/` live, so changes should appear immediately. If not:

```bash
# Clear Laravel cache
docker compose exec laravel php artisan config:clear
docker compose exec laravel php artisan cache:clear

# Or restart container
docker compose restart laravel
```

## API Response Format

All endpoints return JSON with a consistent structure:

### Success Response

```json
{
  "evento": { /* resource data */ },
  "status": 200
}
```

For lists:
```json
{
  "eventos": [{ /* resources */ }],
  "status": 200
}
```

Status codes:
- `200` - OK (GET, PUT, DELETE success)
- `201` - Created (POST success)
- `400` - Validation error
- `404` - Resource not found
- `500` - Server error

### Error Response

```json
{
  "message": "Error de validación",
  "errors": {
    "email": ["The email field is required."],
    "titulo": ["The titulo field is required."]
  },
  "status": 400
}
```

## Validation Rules & Patterns

Controllers use Laravel's `Validator` facade with explicit rule definitions:

### Evento Validation (store/update)
```php
'titulo' => 'required|string|max:255',
'descripcion' => 'required|string|max:10000',
'fecha_inicio' => 'required|date|after_or_equal:today',  // Store only
'fecha_fin' => 'required|date|after_or_equal:fecha_inicio',
'ubicacion' => 'required|string|max:255',
```

### Asistente Validation (store)
```php
'nombre' => 'required|string|max:255',
'email' => 'required|email|max:255|unique:asistentes,email,NULL,id,evento_id,X',  // Unique per evento
'telefono' => 'required|string|max:20',
'evento_id' => 'required|integer|exists:eventos,id',  // Must reference existing event
```

**Pattern**: All validation happens in controllers before model creation. Return `400` status with error details if validation fails.

## Request/Response Flow

Example: Creating an Evento

1. **Request** → `POST /api/eventos`
   ```json
   {
     "titulo": "Tech Conference 2025",
     "descripcion": "Annual technology conference",
     "fecha_inicio": "2025-06-15",
     "fecha_fin": "2025-06-17",
     "ubicacion": "Convention Center"
   }
   ```

2. **Controller** (`EventoController::store()`)
   - Validate input with `Validator::make()`
   - Return `400` if validation fails
   - Create model with `Evento::create()`
   - Return `201` with created resource

3. **Response**
   ```json
   {
     "evento": {
       "id": 1,
       "titulo": "Tech Conference 2025",
       "descripcion": "Annual technology conference",
       "fecha_inicio": "2025-06-15",
       "fecha_fin": "2025-06-17",
       "ubicacion": "Convention Center",
       "created_at": "2025-03-22T00:04:27Z",
       "updated_at": "2025-03-22T00:04:27Z"
     },
     "status": 201
   }
   ```

## Eager Loading & Relationships

Controllers load related data with `with()` to prevent N+1 queries:

```php
// In EventoController::index()
$eventos = Evento::with(['asistentes', 'ponentes'])->get();

// In EventoController::show()
$evento = Evento::with(['asistentes', 'ponentes'])->find($id);

// In AsistenteController::index()
$asistentes = Asistente::with('evento')->get();
```

This loads all relationships in a single query per relation type.

## Testing Patterns

### Feature Tests (`tests/Feature/`)

Test complete HTTP workflows with real database state:

```php
use RefreshDatabase;  // Refresh DB before each test

public function test_can_create_evento_with_ponente_and_asistentes()
{
    // 1. Create test data
    $evento = Evento::create([...]);
    $ponente = Ponente::create([...]);
    
    // 2. Set up relationships
    $evento->ponentes()->attach($ponente->id);
    
    // 3. Assert database state
    $this->assertDatabaseHas('eventos', ['titulo' => '...']);
    $this->assertTrue($evento->ponentes->contains($ponente));
}
```

### Unit Tests (`tests/Unit/`)

Test model methods and business logic in isolation:

```php
public function test_evento_has_many_asistentes()
{
    $evento = Evento::factory()->create();
    $asistente = Asistente::factory()->for($evento)->create();
    
    $this->assertTrue($evento->asistentes->contains($asistente));
}
```

### Key Patterns

- Use `RefreshDatabase` trait to reset DB before each test
- Use `with()` to load relationships in assertions
- Use `assertDatabaseHas()` to verify persisted data
- Use model relationships directly to test Eloquent connections

## Dependency Management

### Composer (PHP)

```bash
# Install dependencies
docker compose exec laravel composer install

# Update dependencies
docker compose exec laravel composer update

# Add a new package
docker compose exec laravel composer require vendor/package

# Remove package
docker compose exec laravel composer remove vendor/package
```

Key packages installed:
- `laravel/framework:^12.0` - Core framework
- `laravel/passport:^13.0` - OAuth 2.0 authentication
- `laravel-keycloak-guard:^1.6` - Keycloak SSO support
- `laravel/tinker:^2.9` - Interactive REPL
- `phpunit/phpunit:^12.0` - Testing framework

### npm (Frontend Build)

```bash
# Install dependencies
docker compose exec laravel npm install

# Update dependencies
docker compose exec laravel npm update

# Add package
docker compose exec laravel npm install package-name --save-dev
```

Key packages:
- `vite:^7.1.7` - Frontend build tool
- `laravel-vite-plugin:^2.0.1` - Laravel integration
- `tailwindcss:^4.1.13` - CSS framework

## Debugging & Introspection

### Using Tinker REPL

Interactive PHP shell for testing code:

```bash
docker compose exec laravel php artisan tinker

# List models
>>> App\Models\Evento::all();
>>> App\Models\Evento::find(1);

# Test relationships
>>> $evento = App\Models\Evento::find(1);
>>> $evento->asistentes;
>>> $evento->ponentes;

# Test validation manually
>>> $validator = Validator::make(['titulo' => ''], ['titulo' => 'required']);
>>> $validator->fails();

# Check database connection
>>> DB::connection()->getPdo();
```

### Reading Logs

```bash
# Tail application logs
docker compose logs -f laravel

# Tail database logs
docker compose logs -f mariadb

# View specific log file
docker compose exec laravel tail -f storage/logs/laravel.log
```

### Checking Container State

```bash
# Container status
docker compose ps

# Shell into container
docker compose exec laravel bash

# View environment variables inside container
docker compose exec laravel printenv | grep DB_
```

## Models Deep Dive

### Evento Model

```php
protected $fillable = ['titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'ubicacion'];

// Relationships
public function asistentes() { return $this->hasMany(Asistente::class); }
public function ponentes() { return $this->belongsToMany(Ponente::class, 'evento_ponente')->withTimestamps(); }
```

To add ponentes to an event:
```php
$evento->ponentes()->attach($ponente_id);  // Add
$evento->ponentes()->detach($ponente_id);  // Remove
$evento->ponentes()->sync([$id1, $id2]);   // Replace all
```

### Ponente Model

Many-to-many with Evento via `evento_ponente` junction table.

### Asistente Model

Belongs to single Evento. Note the `unique` validation constraint is scoped to evento:

```php
'email' => 'unique:asistentes,email,NULL,id,evento_id,' . $request->evento_id
```

This allows same email across different events, but prevents duplicates within an event.

## Key Gotchas & Solutions

### 1. N+1 Query Problem

**Problem**: Looping through events and accessing `$evento->ponentes` in a loop causes separate queries.

**Solution**: Always use `with()` when fetching:
```php
// ❌ Bad: N+1 queries
$eventos = Evento::all();
foreach($eventos as $e) { $e->ponentes; }  // Separate query per event

// ✅ Good: 2 queries total
$eventos = Evento::with('ponentes')->get();
```

### 2. Validation Errors Not Returning

**Problem**: Custom validation rules need explicit error messages.

**Solution**: Pass error messages array to validator:
```php
$validator = Validator::make($data, $rules, [
    'email.unique' => 'This attendee is already registered for this event.'
]);
```

### 3. Mass Assignment Protection

**Problem**: Trying to create a model with columns not in `$fillable` silently fails.

**Solution**: Always add fields to `$fillable` when adding new columns:
```php
protected $fillable = ['field1', 'field2', 'new_field'];
```

### 4. Database Connection Issues in Tests

**Problem**: Tests fail with "connection refused" when MariaDB isn't ready.

**Solution**: Tests are configured for SQLite in-memory via `phpunit.xml`. No MariaDB needed:
```xml
<!-- Commented out by default - uses array cache instead
<env name="DB_CONNECTION" value="sqlite"/>
<env name="DB_DATABASE" value=":memory:"/>
-->
```

## Security Considerations

### Environment Variables

- **Never commit `.env`** - Contains database credentials
- Use `.env.example` as template for new developers
- In Codespaces, use **Secrets** instead of local `.env`

### Authentication

- `auth:api` middleware protects write operations (POST, PUT, DELETE)
- Passport handles token generation and validation
- Keycloak integration available for SSO

### CORS (if needed)

Currently API serves from same host. If adding frontend SPA, configure:
```php
// config/cors.php
'paths' => ['api/*'],
'allowed_origins' => ['http://localhost:3000'],  // Your frontend
```

### Input Validation

- All input is validated before reaching models
- Email uniqueness is enforced at database level
- Date formats are validated (must be `YYYY-MM-DD`)

## Performance Notes

### Database Indexing

Key relationships are indexed by default via migrations. When adding new searchable columns, ensure indexes:

```php
Schema::create('eventos', function (Blueprint $table) {
    $table->id();
    $table->string('titulo')->index();  // Adds index
    $table->timestamps();
});
```

### Caching

```bash
# Cache is configured to use database
# Clear cache after schema changes:
docker compose exec laravel php artisan cache:clear
```

### Pagination (if needed)

Add to controller:
```php
$eventos = Evento::with(['asistentes', 'ponentes'])->paginate(15);
```

## References

- **Laravel Docs**: https://laravel.com/docs
- **Laravel Testing**: https://laravel.com/docs/testing
- **Eloquent Relationships**: https://laravel.com/docs/eloquent-relationships
- **Validation**: https://laravel.com/docs/validation
- **Docker Compose**: https://docs.docker.com/compose/
- **MariaDB**: https://mariadb.com/docs/
- **PlantUML Diagrams**: Check `docs/` directory
