<?php

namespace Tests\Unit;

use App\Models\Evento;
use PHPUnit\Framework\TestCase;

class EventoUnitTest extends TestCase
{
    public function test_evento_has_titulo()
    {
        $evento = new Evento(['titulo' => 'Conferencia de IA']);
        $this->assertEquals('Conferencia de IA', $evento->titulo);
    }
}
