<?php

namespace Database\Seeders;

use App\Models\User;
// use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use Database\Seeders\SqlSeedSeeder;
use Database\Seeders\TestDataSeeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        // User::factory(10)->create();

        // Si necesitas crear un usuario de prueba con factory, activa esta sección
        // Ten en cuenta que las factories usan faker (require-dev) y pueden faltar en
        // entornos donde no estén instaladas dependencias de desarrollo.
        // User::factory()->create([
        //     'name' => 'Test User',
        //     'email' => 'test@example.com',
        // ]);

        // Ejecutar SQL seed idempotente y el seeder de prueba
        $this->call([SqlSeedSeeder::class, TestDataSeeder::class]);
    }
}
