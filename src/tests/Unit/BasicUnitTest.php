<?php

namespace Tests\Unit;

use Tests\TestCase;

class BasicUnitTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_that_true_is_true(): void
    {
        $this->assertTrue(true);
    }

    public function test_sum_is_correct(): void
    {
        $this->assertEquals(4, 2 + 2);
    }

    public function test_string_contains(): void
    {
        $this->assertStringContainsString('laravel', 'bienvenido a laravel');
    }
}
