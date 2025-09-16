<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Evento extends Model
{
    protected $table = 'eventos';
    protected $fillable = [
        'titulo',
        'descripcion',
        'fecha_inicio',
        'fecha_fin',
        'ubicacion'
    ];
}
