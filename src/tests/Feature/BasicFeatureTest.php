<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class BasicFeatureTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_the_application_returns_a_successful_response(): void
    {
        $response = $this->get('/');
        $response->assertStatus(200);
        $response->assertSee('Laravel'); // Verifica que la palabra Laravel aparece en la página principal
    }

    public function test_not_found_page_returns_404(): void
    {
        $response = $this->get('/no-existe-url');
        $response->assertStatus(404);
    }
}
