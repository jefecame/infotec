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

    /**
     * Relación con Asistentes
     * Un evento tiene muchos asistentes
     */
    public function asistentes()
    {
        return $this->hasMany(Asistente::class);
    }

    /**
     * Relación con Ponentes
     * Un evento puede tener muchos ponentes (many-to-many)
     */
    public function ponentes()
    {
        return $this->belongsToMany(Ponente::class, 'evento_ponente')
                    ->withTimestamps();
    }
}
