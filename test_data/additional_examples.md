# Ejemplos JSON Adicionales para INFOTEC API

Este archivo contiene ejemplos JSON adicionales para diferentes casos de uso y validaciones.

## 🎯 Eventos - Ejemplos Adicionales

### Evento con fechas de un solo día
```json
{
  "titulo": "Masterclass: Introducción a Blockchain",
  "descripcion": "Masterclass intensiva sobre tecnología blockchain, criptomonedas y contratos inteligentes. Aprende los fundamentos de esta tecnología disruptiva en una sola sesión.",
  "fecha_inicio": "2025-11-20",
  "fecha_fin": "2025-11-20",
  "ubicacion": "Auditorio Virtual INFOTEC"
}
```

### Evento con descripción corta
```json
{
  "titulo": "Networking Tech Meetup",
  "descripcion": "Evento de networking para profesionales de tecnología.",
  "fecha_inicio": "2025-12-05",
  "fecha_fin": "2025-12-05",
  "ubicacion": "Lobby Principal INFOTEC"
}
```

## 👥 Ponentes - Ejemplos Adicionales

### Ponente con biografía corta
```json
{
  "nombre": "Ing. Sofia Ramírez Castro",
  "biografia": "Desarrolladora Full Stack con 8 años de experiencia en startups tecnológicas. Especialista en React, Node.js y arquitecturas modernas.",
  "especialidad": "Desarrollo Frontend y UX/UI"
}
```

### Ponente internacional
```json
{
  "nombre": "Dr. Michael Johnson",
  "biografia": "Senior Software Engineer at Google with over 20 years of experience in large-scale distributed systems. PhD in Computer Science from MIT. Has led the development of several open-source projects with millions of users worldwide. Expert in microservices architecture, Kubernetes, and cloud-native applications.",
  "especialidad": "Distributed Systems and Cloud Architecture"
}
```

## 🎫 Asistentes - Ejemplos Adicionales

### Asistente para evento diferente
```json
{
  "nombre": "Lic. Carlos Eduardo Vega",
  "email": "carlos.vega@innovatech.com.mx",
  "telefono": "+52 55 4455-6677",
  "evento_id": 3
}
```

### Asistente universitario
```json
{
  "nombre": "Ana Lucía Herrera Mendoza",
  "email": "ana.herrera@estudiante.unam.mx",
  "telefono": "+52 55 9988-7766",
  "evento_id": 4
}
```

### Asistente empresarial
```json
{
  "nombre": "Mtro. Roberto Carlos Jiménez",
  "email": "roberto.jimenez@techcorp.global",
  "telefono": "+52 55 1122-3344",
  "evento_id": 5
}
```

## ❌ Ejemplos de Validación de Errores

### Evento con fecha en el pasado (ERROR)
```json
{
  "titulo": "Evento con fecha inválida",
  "descripcion": "Este evento generará un error de validación",
  "fecha_inicio": "2024-01-01",
  "fecha_fin": "2024-01-02", 
  "ubicacion": "Lugar cualquiera"
}
```

### Evento con fecha_fin anterior a fecha_inicio (ERROR)
```json
{
  "titulo": "Evento con fechas invertidas",
  "descripcion": "Este evento generará un error de validación",
  "fecha_inicio": "2025-12-31",
  "fecha_fin": "2025-12-01",
  "ubicacion": "Lugar cualquiera"
}
```

### Asistente con evento_id inválido (ERROR)
```json
{
  "nombre": "Usuario Test",
  "email": "test@error.com",
  "telefono": "+52 55 0000-0000",
  "evento_id": 999
}
```

### Asistente con email duplicado para el mismo evento (ERROR)
```json
{
  "nombre": "Usuario Duplicado",
  "email": "maria.vasquez@techcorp.com",
  "telefono": "+52 55 9999-9999",
  "evento_id": 2
}
```

## 🧪 Scripts de Prueba Automatizada

### PowerShell - Crear múltiples registros
```powershell
# Crear varios eventos de prueba
$eventos = @(
    "test_data/create_evento.json",
    "additional_evento_1.json",
    "additional_evento_2.json"
)

foreach ($evento in $eventos) {
    Write-Host "Creando evento desde $evento"
    $response = curl -X POST http://localhost:8000/api/eventos -H "Content-Type: application/json" -H "Accept: application/json" -d (Get-Content $evento -Raw)
    Write-Host "Respuesta: $response"
    Write-Host "---"
}
```

### Bash - Verificar todos los endpoints
```bash
#!/bin/bash
echo "=== Verificando todos los endpoints ==="

echo "📅 Eventos:"
curl -s http://localhost:8000/api/eventos | jq '.eventos | length'

echo "👥 Ponentes:"
curl -s http://localhost:8000/api/ponentes | jq '.ponentes | length'

echo "🎫 Asistentes:"
curl -s http://localhost:8000/api/asistentes | jq '.asistentes | length'
```

## 💡 Tips de Uso

1. **Fechas**: Siempre usar formato YYYY-MM-DD
2. **Email**: Debe ser único por evento, no globalmente
3. **Biografías**: Pueden ser muy extensas (campo TEXT)
4. **Teléfonos**: Se recomienda formato internacional (+52...)
5. **IDs**: Los evento_id deben existir antes de crear asistentes

## 🔧 Troubleshooting

### Error "evento_id no existe"
- Verificar que el evento existe: `curl http://localhost:8000/api/eventos/{id}`
- Usar un ID válido de la lista de eventos

### Error "Email ya registrado"
- El email ya está registrado para ese evento específico
- Usar un email diferente o registrar en otro evento

### Error "Fecha en el pasado"
- Las fechas deben ser futuras (después del día actual)
- Actualizar las fechas en el JSON