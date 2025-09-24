<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
// Agregar el controlador EventoController
use App\Http\Controllers\EventoController;
// Agregar el controlador PonenteController
use App\Http\Controllers\PonenteController;
// Agregar el controlador AsistenteController
use App\Http\Controllers\AsistenteController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
| Aquí es donde puedes registrar las rutas de la API para tu aplicación.
| Estas rutas son cargadas por el RouteServiceProvider.
*/

/*
|--------------------------------------------------------------------------
| Rutas públicas (no requieren autenticación)
|--------------------------------------------------------------------------
*/
// Evento: listar, ver
Route::get('/eventos', [EventoController::class, 'index']);
Route::get('/eventos/{id}', [EventoController::class, 'show']);

// Ponente: listar, ver
Route::get('/ponentes', [PonenteController::class, 'index']);
Route::get('/ponentes/{id}', [PonenteController::class, 'show']);

/*
|--------------------------------------------------------------------------
| Rutas privadas (requieren autenticación)
|--------------------------------------------------------------------------
*/
Route::middleware('auth:api')->group(function () {
    // Evento: crear, actualizar, eliminar
    Route::post('/eventos', [EventoController::class, 'store']);
    Route::put('/eventos/{evento}', [EventoController::class, 'update']);
    Route::delete('/eventos/{id}', [EventoController::class, 'destroy']);

    // Ponente: crear, actualizar, eliminar
    Route::post('/ponentes', [PonenteController::class, 'store']);
    Route::put('/ponentes/{ponente}', [PonenteController::class, 'update']);
    Route::delete('/ponentes/{id}', [PonenteController::class, 'destroy']);

    // Asistentes: listar, crear, ver, actualizar, eliminar
    Route::get('/asistentes', [AsistenteController::class, 'index']);
    Route::post('/asistentes', [AsistenteController::class, 'store']);
    Route::get('/asistentes/{id}', [AsistenteController::class, 'show']);
    Route::put('/asistentes/{asistente}', [AsistenteController::class, 'update']);
    Route::delete('/asistentes/{id}', [AsistenteController::class, 'destroy']);

    // Usuario autenticado
    Route::get('/user', function (Request $request) {
        return $request->user();
    });
});