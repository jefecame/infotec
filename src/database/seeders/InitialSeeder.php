<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

// Seeder inicial que ejecuta el SQL para poblar eventos, ponentes y asistentes
class InitialSeeder extends Seeder
{
    /**
     * Ejecuta el seed inicial desde el archivo SQL.
     * Crea 3 eventos, 1 ponente por evento y 3 asistentes por evento.
     */
    public function run(): void
    {
        $path = database_path('seeders/sql/seed_initial.sql');

        if (!file_exists($path)) {
            $this->command->error("SQL seed file not found: {$path}");
            return;
        }

        $sql = file_get_contents($path);

        // Ejecuta el SQL en bloque; es idempotente y usa INSERT IGNORE
        DB::unprepared($sql);
        $this->command->info('✅ SQL seed ejecutado desde: ' . $path);
    }
}
