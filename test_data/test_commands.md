# Comandos de Prueba para la API INFOTEC

Este archivo contiene ejemplos de comandos cURL para probar los endpoints de la API usando los archivos JSON creados.

## 📋 Prerrequisitos

Asegúrate de que:
- Los servicios de Docker estén corriendo: `docker-compose up -d`
- La aplicación esté disponible en: http://localhost:8000
- Los archivos JSON estén en el directorio `test_data/`

## 🎯 Crear Evento

```bash
# POST /api/eventos
curl -X POST http://localhost:8000/api/eventos \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d @test_data/create_evento.json
```

**PowerShell equivalente:**
```powershell
curl -X POST http://localhost:8000/api/eventos -H "Content-Type: application/json" -H "Accept: application/json" -d (Get-Content test_data/create_evento.json -Raw)
```

## 👥 Crear Ponente

```bash
# POST /api/ponentes
curl -X POST http://localhost:8000/api/ponentes \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d @test_data/create_ponente.json
```

**PowerShell equivalente:**
```powershell
curl -X POST http://localhost:8000/api/ponentes -H "Content-Type: application/json" -H "Accept: application/json" -d (Get-Content test_data/create_ponente.json -Raw)
```

## 🎫 Crear Asistente

```bash
# POST /api/asistentes
curl -X POST http://localhost:8000/api/asistentes \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d @test_data/create_asistente.json
```

**PowerShell equivalente:**
```powershell
curl -X POST http://localhost:8000/api/asistentes -H "Content-Type: application/json" -H "Accept: application/json" -d (Get-Content test_data/create_asistente.json -Raw)
```

## 🔍 Verificar Creación

Después de crear los registros, puedes verificarlos:

```bash
# Ver todos los eventos
curl http://localhost:8000/api/eventos

# Ver todos los ponentes  
curl http://localhost:8000/api/ponentes

# Ver todos los asistentes
curl http://localhost:8000/api/asistentes

# Ver evento específico (reemplaza {id} con el ID del evento creado)
curl http://localhost:8000/api/eventos/{id}
```

## ⚠️ Notas Importantes

### Para Asistentes:
- El `evento_id` debe ser un ID válido de un evento existente
- El email debe ser único por evento (no puede haber dos asistentes con el mismo email en el mismo evento)
- Todos los campos son obligatorios

### Para Eventos:
- `fecha_inicio` y `fecha_fin` deben ser fechas futuras (no se permiten eventos en el pasado)
- `fecha_fin` debe ser igual o posterior a `fecha_inicio`
- El título debe ser único
- La descripción puede ser muy larga (hasta 10,000 caracteres)

### Para Ponentes:
- Todos los campos son obligatorios
- La biografía puede ser muy extensa (campo TEXT)
- No hay restricciones únicas (pueden existir ponentes con el mismo nombre)

## 🧪 Ejemplos de Respuestas Exitosas

### Evento creado:
```json
{
  "evento": {
    "id": 5,
    "titulo": "Workshop de Cloud Computing y AWS",
    "descripcion": "Workshop intensivo sobre computación...",
    "fecha_inicio": "2025-01-15",
    "fecha_fin": "2025-01-17",
    "ubicacion": "Sala de Conferencias Principal INFOTEC, Edificio A",
    "created_at": "2025-09-16T23:30:00Z",
    "updated_at": "2025-09-16T23:30:00Z"
  },
  "message": "Evento creado exitosamente",
  "status": 201
}
```

### Ponente creado:
```json
{
  "ponente": {
    "id": 5,
    "nombre": "Dr. Fernando Medina González",
    "biografia": "Doctor en Ingeniería en Sistemas...",
    "especialidad": "Cloud Computing, AWS, Arquitecturas Serverless y DevOps",
    "created_at": "2025-09-16T23:30:00Z",
    "updated_at": "2025-09-16T23:30:00Z"
  },
  "message": "Ponente creado exitosamente",
  "status": 201
}
```

### Asistente creado:
```json
{
  "asistente": {
    "id": 6,
    "nombre": "Ing. Patricia Morales Herrera",
    "email": "patricia.morales@cloudtech.mx",
    "telefono": "+52 55 7788-9900",
    "evento_id": 2,
    "created_at": "2025-09-16T23:30:00Z",
    "updated_at": "2025-09-16T23:30:00Z",
    "evento": {
      "id": 2,
      "titulo": "Conferencia de Inteligencia Artificial 2024",
      "fecha_inicio": "2024-12-15",
      "fecha_fin": "2024-12-17"
    }
  },
  "message": "Asistente registrado exitosamente",
  "status": 201
}
```