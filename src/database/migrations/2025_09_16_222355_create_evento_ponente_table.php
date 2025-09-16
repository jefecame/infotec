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
        Schema::create('evento_ponente', function (Blueprint $table) {
            $table->id();
            
            // Foreign keys
            $table->unsignedBigInteger('evento_id');
            $table->unsignedBigInteger('ponente_id');
            
            // Foreign key constraints with cascade delete
            $table->foreign('evento_id')
                  ->references('id')
                  ->on('eventos')
                  ->onDelete('cascade');
                  
            $table->foreign('ponente_id')
                  ->references('id')
                  ->on('ponentes')
                  ->onDelete('cascade');
            
            // Unique constraint to prevent duplicate assignments
            $table->unique(['evento_id', 'ponente_id']);
            
            // Indexes for performance
            $table->index('evento_id');
            $table->index('ponente_id');
            
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('evento_ponente');
    }
};
