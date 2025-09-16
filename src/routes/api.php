<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
// Agregar el controlador EventoController
use App\Http\Controllers\EventoController;
use App\Http\Controllers\PonenteController;
use App\Http\Controllers\AsistenteController;

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

/**
* Rutas para el recurso Ponente.
*/

Route::get('/ponentes', [PonenteController::class, 'index']);
Route::post('/ponentes', [PonenteController::class, 'store']);
Route::get('/ponentes/{id}', [PonenteController::class, 'show']);
Route::put('/ponentes/{ponente}', [PonenteController::class, 'update']);
Route::delete('/ponentes/{id}', [Ponenteontroller::class, 'destroy']);

/**
* Rutas para el recurso Asistente.
*/

Route::get('/asistentes', [Asistenteontroller::class, 'index']);
Route::post('/asistentes', [AsistenteController::class, 'store']);
Route::get('/asistentes/{id}', [AsistenteController::class, 'show']);
Route::put('/asistentes/{asistente}', [AsistenteController::class, 'update']);
Route::delete('/asistentes/{id}', [AsistenteController::class, 'destroy']);