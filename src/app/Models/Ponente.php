<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Ponente extends Model
{
    protected $table = 'ponentes';
    protected $fillable = [
        'nombre',
        'biografia',
        'especialidad'
    ];

    /**
     * Relación con Eventos
     * Un ponente puede participar en muchos eventos (many-to-many)
     */
    public function eventos()
    {
        return $this->belongsToMany(Evento::class, 'evento_ponente')
                    ->withTimestamps();
    }
}
