# Development Workflow & Best Practices

This guide covers common development workflows, IDE setup, and best practices for this Laravel project.

## IDE/Editor Setup

### VS Code / Cursor / GitHub Copilot

Recommended extensions for PHP/Laravel development:

```json
{
  "extensions": {
    "PHP Intelephense": "bmewburn.vscode-intelephense-client",
    "Laravel Artisan": "ryannaddy.laravel-artisan",
    "Laravel Blade Snippets": "onecentlin.laravel-blade",
    "Database Clients": "cweijan.vscode-database-client2",
    "Docker": "ms-azuretools.vscode-docker"
  }
}
```

### PHPStan (Static Analysis)

Not currently configured, but recommended for larger codebases. To add:

```bash
docker compose exec laravel composer require --dev phpstan/phpstan
docker compose exec laravel vendor/bin/phpstan analyse app --level=5
```

## Git Workflow

### Branch Strategy

- `main` - Production-ready code
- `develop` - Integration branch
- `feature/name` - Feature branches
- `bugfix/name` - Bug fix branches

### Commit Messages

Use clear, descriptive messages:

```
feature: add speaker rating system

- Add star_rating column to ponentes table
- Add endpoint PUT /api/ponentes/{id}/rate
- Add validation for rating values 1-5
```

### Pre-commit Checks

Before pushing:

```bash
# Format code
docker compose exec laravel php artisan pint

# Run tests
docker compose exec laravel php artisan test

# Check for laravel-specific issues
docker compose exec laravel php artisan tinker --execute="echo 'Ready to commit';"
```

## Making Changes to Core Components

### Adding a New Field to Evento

1. **Create migration**:
   ```bash
   docker compose exec laravel php artisan make:migration add_capacity_to_eventos
   ```

2. **Edit migration** (`database/migrations/YYYY_MM_DD_HHMMSS_add_capacity_to_eventos.php`):
   ```php
   Schema::table('eventos', function (Blueprint $table) {
       $table->integer('capacity')->nullable()->index();
       $table->integer('registered')->default(0);
   });
   ```

3. **Update model** (`app/Models/Evento.php`):
   ```php
   protected $fillable = [
       'titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'ubicacion',
       'capacity', 'registered'  // Add new fields
   ];
   ```

4. **Update controller validation** (if input field):
   ```php
   $validator = Validator::make($request->all(), [
       // ... existing validations
       'capacity' => 'integer|min:1|max:10000',
   ]);
   ```

5. **Run migration**:
   ```bash
   docker compose exec laravel php artisan migrate
   ```

6. **Update tests**:
   ```bash
   docker compose exec laravel php artisan test
   ```

### Adding a New Controller/Model Pair

```bash
# Create model with migration, controller, factory
docker compose exec laravel php artisan make:model YourModel -mcr --api

# This creates:
# - app/Models/YourModel.php
# - app/Http/Controllers/YourModelController.php
# - database/factories/YourModelFactory.php
# - database/migrations/YYYY_MM_DD_create_your_models_table.php
```

Then:

1. Define relationships in model
2. Add validation rules in controller
3. Implement CRUD methods in controller
4. Add routes in `routes/api.php`
5. Write tests in `tests/Feature/`

### Creating Seeder Data

```bash
docker compose exec laravel php artisan make:seeder YourModelSeeder
```

Example (`database/seeders/YourModelSeeder.php`):

```php
<?php

namespace Database\Seeders;

use App\Models\Evento;
use Illuminate\Database\Seeder;

class EventoSeeder extends Seeder
{
    public function run(): void
    {
        Evento::create([
            'titulo' => 'Tech Conference 2025',
            'descripcion' => 'Annual tech gathering',
            'fecha_inicio' => '2025-06-15',
            'fecha_fin' => '2025-06-17',
            'ubicacion' => 'Convention Center',
        ]);
    }
}
```

Call from `DatabaseSeeder.php`:

```php
public function run(): void
{
    $this->call([
        EventoSeeder::class,
        PonenteSeeder::class,
    ]);
}
```

Then run: `docker compose exec laravel php artisan migrate:fresh --seed`

## Debugging Workflows

### Debugging a Failed Test

```bash
# 1. Run the specific test with verbose output
docker compose exec laravel php artisan test --filter=test_name -v

# 2. Add dd() (dump and die) to see intermediate values
// In test or controller:
dd($evento);  // Stops execution, outputs variable

# 3. Or use dumpIt to continue:
dump($evento);
// ... code continues

# 4. View output in logs
docker compose logs -f laravel
```

### Debugging API Requests

```bash
# Option 1: Use curl with verbose output
curl -v http://localhost:8000/api/eventos

# Option 2: Use Postman/Insomnia for GUI
# Set method, headers, body

# Option 3: Test in Tinker
docker compose exec laravel php artisan tinker
> $response = app('Laravel\Lumen\Routing\Router')->dispatch(
    app('Illuminate\Http\Request')->create('GET', '/api/eventos')
);
> $response->getContent();
```

### Database Debugging

```bash
# Access MySQL CLI directly
docker compose exec mariadb mysql -u infotec_user -p infotec_db
MariaDB> SELECT * FROM eventos;

# Or use Tinker
docker compose exec laravel php artisan tinker
> DB::table('eventos')->get();
> DB::table('eventos')->where('id', 1)->first();
```

### Checking Container Logs for Errors

```bash
# Last 50 lines of logs
docker compose logs --tail=50 laravel

# Follow live logs
docker compose logs -f laravel

# Filter by timestamp
docker compose logs laravel --since 5m  # Last 5 minutes

# View specific service
docker compose logs mariadb
```

## Performance Debugging

### Identifying Slow Queries

Enable query logging in `config/database.php`:

```php
'mysql' => [
    'driver' => 'mysql',
    'host' => env('DB_HOST'),
    // ...
    'modes' => [
        'STRICT_TRANS_TABLES',
        'NO_ZERO_IN_DATE',
        'NO_ZERO_DATE',
        'ERROR_FOR_DIVISION_BY_ZERO',
        'NO_ENGINE_SUBSTITUTION',
    ],
    'logging' => true,  // Enable query logging
],
```

Then in Tinker:

```php
DB::enableQueryLog();
// ... your queries
dd(DB::getQueryLog());
```

### N+1 Detection

Look for patterns like:

```php
// ❌ N+1 problem
foreach (Evento::all() as $evento) {
    echo $evento->ponentes->count();  // Query per event
}

// ✅ Solution
foreach (Evento::with('ponentes')->get() as $evento) {
    echo $evento->ponentes->count();  // 2 queries total
}
```

## Deployment Considerations

### Building for Production

Currently API runs only in Docker development environment. For deployment:

```bash
# Build optimized image
docker build --target production -t infotec:latest .

# Run production container (would need reverse proxy, HTTPS, etc)
docker run -d -e APP_ENV=production infotec:latest
```

### Environment Variable Management

For production use GitHub Secrets or Kubernetes ConfigMaps:

```bash
# In CI/CD pipeline
export DB_PASSWORD=${SECRET_DB_PASSWORD}
export APP_KEY=${SECRET_APP_KEY}
docker compose up -d
```

### Database Backups

```bash
# Backup MariaDB
docker compose exec mariadb mysqldump -u root -p${MARIADB_ROOT_PASSWORD} ${MARIADB_DATABASE} > backup.sql

# Restore
docker compose exec mariadb mysql -u root -p${MARIADB_ROOT_PASSWORD} ${MARIADB_DATABASE} < backup.sql
```

## Troubleshooting Common Issues

### "Target class does not exist" Error

Problem: Controller method not found when accessing route.

Solution:
1. Check controller name matches route: `EventoController` not `Eventocontroller`
2. Verify namespace: `App\Http\Controllers\EventoController`
3. Reload autoloader: `php artisan dump-autoload`

### "Integrity constraint violation" on Insert

Problem: Foreign key constraint failed (e.g., evento_id references non-existent evento).

Solution:
1. Verify referenced record exists: `Evento::find($id)`
2. Check column names match in migration
3. Ensure migration ran: `php artisan migrate:status`

### "SQLSTATE[HY000]: General error: 1030"

Problem: Storage or temp space issue.

Solution:
```bash
# Check disk space
docker compose exec laravel df -h

# Clear cache and temp
docker compose exec laravel php artisan cache:clear
docker compose exec laravel rm -rf storage/framework/cache/*
```

### Tests Randomly Failing

Problem: Database state pollution between tests.

Solution:
1. All test classes should use `RefreshDatabase` trait
2. Don't manually seed in tests - use factories
3. Use `setUp()` and `tearDown()` for cleanup

```php
use RefreshDatabase;  // ✅ Ensures clean DB per test

public function test_something()
{
    $evento = Evento::factory()->create();  // ✅ Use factories
    // test...
}
```

## Code Quality Standards

### What Gets Checked

- PHP syntax (via Pint)
- Type hints (encouraged but not enforced)
- Variable names (should be descriptive)
- Comments (only on complex logic)

### Running Pint

```bash
# Format code
docker compose exec laravel php artisan pint

# Check without modifying
docker compose exec laravel php artisan pint --test

# Format specific file
docker compose exec laravel php artisan pint app/Models/Evento.php
```

### What to Avoid

- Hardcoded values (use env/config)
- Comments for obvious code (good naming is better)
- Deep nesting (refactor to methods)
- Global state (use dependency injection)

## Resources

- **Laravel Best Practices**: https://laravel.best/
- **PHP Standards**: https://www.php-fig.org/psr/
- **12 Factor App**: https://12factor.net/
- **Git Workflow**: https://www.atlassian.com/git/tutorials/comparing-workflows
