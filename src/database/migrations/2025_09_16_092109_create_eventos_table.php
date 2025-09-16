<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('eventos', function (Blueprint $table) {
            $table->id();
            $table->string('titulo');
            $table->text('descripcion'); // Changed to text for longer content
            $table->date('fecha_inicio');
            $table->date('fecha_fin');
            $table->string('ubicacion');
            
            // Performance indexes
            $table->index('titulo');
            $table->index('fecha_inicio');
            $table->index('fecha_fin');
            $table->index(['fecha_inicio', 'fecha_fin']); // Composite index for date ranges
            
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('eventos');
    }
};
