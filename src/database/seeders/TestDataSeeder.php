<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\Evento;
use App\Models\Ponente;
use App\Models\Asistente;

class TestDataSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // Eliminar datos existentes para evitar duplicados
        // No podemos usar truncate debido a las restricciones de clave foránea
        
        // Primero eliminamos asistentes (tienen FK a eventos)
        Asistente::query()->delete();
        $this->command->info('🧹 Asistentes existentes eliminados');
        
        // Luego eliminamos las relaciones pivot
        \DB::table('evento_ponente')->delete();
        $this->command->info('🧹 Relaciones evento-ponente eliminadas');
        
        // Después eliminamos eventos y ponentes
        Evento::query()->delete();
        Ponente::query()->delete();
        $this->command->info('🧹 Eventos y ponentes existentes eliminados\n');
        
        $this->command->info('📅 Creando eventos...');
        
        // Crear 3 eventos
        $evento1 = Evento::create([
            'titulo' => 'Conferencia de Inteligencia Artificial 2024',
            'descripcion' => 'Una conferencia completa sobre los últimos avances en inteligencia artificial, machine learning y sus aplicaciones en la industria moderna. Incluye talleres prácticos, conferencias magistrales y networking.',
            'fecha_inicio' => '2024-12-15',
            'fecha_fin' => '2024-12-17',
            'ubicacion' => 'Centro de Convenciones INFOTEC, Ciudad de México'
        ]);
        $this->command->info("✅ Evento creado: {$evento1->titulo}");

        $evento2 = Evento::create([
            'titulo' => 'Taller de Desarrollo Web Full Stack',
            'descripcion' => 'Taller práctico intensivo sobre desarrollo web moderno utilizando tecnologías como Laravel, Vue.js, React y bases de datos relacionales. Dirigido a desarrolladores intermedios y avanzados.',
            'fecha_inicio' => '2024-12-20',
            'fecha_fin' => '2024-12-22',
            'ubicacion' => 'Laboratorio de Cómputo INFOTEC, Planta Baja'
        ]);
        $this->command->info("✅ Evento creado: {$evento2->titulo}");

        $evento3 = Evento::create([
            'titulo' => 'Seminario de Ciberseguridad Empresarial',
            'descripcion' => 'Seminario especializado en ciberseguridad para empresas, cubriendo amenazas actuales, protocolos de seguridad, auditorías y mejores prácticas para proteger activos digitales.',
            'fecha_inicio' => '2024-12-25',
            'fecha_fin' => '2024-12-26',
            'ubicacion' => 'Auditorio Principal INFOTEC'
        ]);
        $this->command->info("✅ Evento creado: {$evento3->titulo}");

        $this->command->info('👥 Creando ponentes...');
        
        // Crear 3 ponentes
        $ponente1 = Ponente::create([
            'nombre' => 'Dr. Ana García Rodríguez',
            'biografia' => 'Doctora en Ciencias de la Computación con especialización en Inteligencia Artificial. Ha trabajado en empresas tecnológicas líderes como Google y Microsoft. Actualmente es profesora investigadora en el Instituto Tecnológico de Monterrey y ha publicado más de 50 artículos en revistas internacionales sobre ML y AI.',
            'especialidad' => 'Inteligencia Artificial y Machine Learning'
        ]);
        $this->command->info("✅ Ponente creado: {$ponente1->nombre} - {$ponente1->especialidad}");

        $ponente2 = Ponente::create([
            'nombre' => 'Ing. Carlos Mendoza Silva',
            'biografia' => 'Ingeniero en Sistemas con más de 12 años de experiencia en desarrollo web full stack. Ha liderado equipos de desarrollo en startups y empresas Fortune 500. Especialista en Laravel, Vue.js, React y arquitecturas de microservicios. Fundador de la comunidad DevMexico.',
            'especialidad' => 'Desarrollo Web Full Stack y DevOps'
        ]);
        $this->command->info("✅ Ponente creado: {$ponente2->nombre} - {$ponente2->especialidad}");

        $ponente3 = Ponente::create([
            'nombre' => 'M.C. Laura Jiménez Torres',
            'biografia' => 'Maestra en Ciberseguridad con certificaciones CISSP, CEH y CISM. Ha trabajado como consultora de seguridad para bancos y empresas gubernamentales. Especialista en auditorías de seguridad, análisis forense digital y gestión de riesgos cibernéticos.',
            'especialidad' => 'Ciberseguridad y Análisis Forense Digital'
        ]);
        $this->command->info("✅ Ponente creado: {$ponente3->nombre} - {$ponente3->especialidad}");

        $this->command->info('🎫 Creando asistentes...');
        
        // Crear 3 asistentes (uno para cada evento)
        $asistente1 = Asistente::create([
            'nombre' => 'María Elena Vásquez López',
            'email' => 'maria.vasquez@techcorp.com',
            'telefono' => '+52 55 1234-5678',
            'evento_id' => $evento1->id
        ]);
        $this->command->info("✅ Asistente creado: {$asistente1->nombre} para '{$evento1->titulo}'");

        $asistente2 = Asistente::create([
            'nombre' => 'Roberto Sánchez Martínez',
            'email' => 'roberto.sanchez@devstudio.mx',
            'telefono' => '+52 55 9876-5432',
            'evento_id' => $evento2->id
        ]);
        $this->command->info("✅ Asistente creado: {$asistente2->nombre} para '{$evento2->titulo}'");

        $asistente3 = Asistente::create([
            'nombre' => 'Carmen Patricia Ruiz Hernández',
            'email' => 'carmen.ruiz@securebank.com',
            'telefono' => '+52 55 5555-1111',
            'evento_id' => $evento3->id
        ]);
        $this->command->info("✅ Asistente creado: {$asistente3->nombre} para '{$evento3->titulo}'");

        $this->command->info('🔗 Creando relaciones ponente-evento...');
        
        // Crear relaciones ponente-evento (muchos a muchos)
        $evento1->ponentes()->attach($ponente1->id);
        $this->command->info("✅ {$ponente1->nombre} asignado a '{$evento1->titulo}'");
        
        $evento2->ponentes()->attach($ponente2->id);
        $this->command->info("✅ {$ponente2->nombre} asignado a '{$evento2->titulo}'");
        
        $evento3->ponentes()->attach($ponente3->id);
        $this->command->info("✅ {$ponente3->nombre} asignado a '{$evento3->titulo}'");
        
        // Asignar algunos ponentes a múltiples eventos para demostrar relación muchos-a-muchos
        $evento1->ponentes()->attach($ponente2->id);
        $this->command->info("✅ {$ponente2->nombre} también asignado a '{$evento1->titulo}'");

        $this->command->info('');
        $this->command->info('=== ¡Datos de prueba creados exitosamente! ===');
        $this->command->info('📊 Resumen:');
        $this->command->info('   • 3 eventos creados');
        $this->command->info('   • 3 ponentes creados');
        $this->command->info('   • 3 asistentes creados');
        $this->command->info('   • 4 relaciones ponente-evento creadas');
        $this->command->info('');
        $this->command->info('🔍 Para verificar los datos:');
        $this->command->info('   • GET /api/eventos');
        $this->command->info('   • GET /api/ponentes');
        $this->command->info('   • GET /api/asistentes');
    }
}