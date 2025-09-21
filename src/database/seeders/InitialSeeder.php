<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class SqlSeedSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $path = database_path('seeders/sql/seed_idempotent.sql');

        if (!file_exists($path)) {
            $this->command->error("SQL seed file not found: {$path}");
            return;
        }

        $sql = file_get_contents($path);

        // Ejecutar en bloque; es idempotente y usa INSERT IGNORE
        DB::unprepared($sql);
        $this->command->info('✅ SQL seed ejecutado desde: ' . $path);
    }
}
