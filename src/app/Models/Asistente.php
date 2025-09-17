<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Asistente extends Model
{
    protected $table = 'asistentes';
    protected $fillable = [
        'nombre',
        'email',
        'telefono',
        'evento_id'
    ];

    /**
     * Relación con Evento
     * Un asistente pertenece a un evento
     */
    public function evento()
    {
        return $this->belongsTo(Evento::class);
    }
}
