<?php

namespace Tests\Unit;

use App\Models\Asistente;
use PHPUnit\Framework\TestCase;

class AsistenteUnitTest extends TestCase
{
    public function test_asistente_has_email()
    {
        $asistente = new Asistente(['email' => 'test@example.com']);
        $this->assertEquals('test@example.com', $asistente->email);
    }
}
