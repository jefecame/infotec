<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\Evento;
use App\Models\Ponente;
use App\Models\Asistente;

class EventoFeatureTest extends TestCase
{
    use RefreshDatabase;

    public function test_can_create_evento_with_ponente_and_asistentes()
    {
        $evento = Evento::create([
            'titulo' => 'Test Evento',
            'descripcion' => 'Descripción de prueba',
            'fecha_inicio' => '2025-10-01',
            'fecha_fin' => '2025-10-02',
            'ubicacion' => 'Auditorio',
        ]);

        $ponente = Ponente::create([
            'nombre' => 'Juan Pérez',
            'biografia' => 'Experto en IA',
            'especialidad' => 'IA',
        ]);

        $evento->ponentes()->attach($ponente->id);

        $asistente = Asistente::create([
            'nombre' => 'Ana López',
            'email' => 'ana@example.com',
            'telefono' => '555-1234',
            'evento_id' => $evento->id,
        ]);

        $this->assertDatabaseHas('eventos', ['titulo' => 'Test Evento']);
        $this->assertDatabaseHas('ponentes', ['nombre' => 'Juan Pérez']);
        $this->assertDatabaseHas('asistentes', ['email' => 'ana@example.com']);
        $this->assertTrue($evento->ponentes->contains($ponente));
        $this->assertEquals($evento->id, $asistente->evento_id);
    }
}
