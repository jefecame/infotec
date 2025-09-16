<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
// Agregar el controlador EventoController
use App\Http\Controllers\EventoController;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:api');

/**
* Rutas para el recurso Evento.
*/

// Recuperar todos los eventos
Route::get('/eventos', [EventoController::class, 'index']);
// Almacenar un evento nuevo
Route::post('/eventos', [EventoController::class, 'store']);
// Recuperar un evento específico
Route::get('/eventos/{id}', [EventoController::class, 'show']);
// Actualizar un evento específico
Route::put('/eventos/{evento}', [EventoController::class, 'update']);
// Eliminar un evento específico
Route::delete('/eventos/{id}', [EventoController::class, 'destroy']);