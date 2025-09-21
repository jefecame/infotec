<?php

namespace Tests\Unit;

use App\Models\Ponente;
use PHPUnit\Framework\TestCase;

class PonenteUnitTest extends TestCase
{
    public function test_ponente_has_especialidad()
    {
        $ponente = new Ponente(['especialidad' => 'DevOps']);
        $this->assertEquals('DevOps', $ponente->especialidad);
    }
}
