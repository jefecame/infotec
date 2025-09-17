# 🧪 Test Data - INFOTEC API

Este directorio contiene archivos JSON de prueba y documentación para probar los endpoints de la API INFOTEC.

## 📁 Estructura de Archivos

```
test_data/
├── README.md                   # Este archivo
├── create_evento.json         # JSON para crear eventos
├── create_ponente.json        # JSON para crear ponentes  
├── create_asistente.json      # JSON para crear asistentes
├── test_commands.md           # Comandos cURL de ejemplo
└── additional_examples.md     # Ejemplos adicionales y casos edge
```

## 🎯 Archivos JSON Principales

### `create_evento.json`
- **Propósito**: Crear un nuevo evento
- **Endpoint**: `POST /api/eventos`
- **Contenido**: Workshop de Cloud Computing y AWS
- **Fechas**: 15-17 octubre 2025 (fechas futuras válidas)

### `create_ponente.json`
- **Propósito**: Crear un nuevo ponente  
- **Endpoint**: `POST /api/ponentes`
- **Contenido**: Dr. Fernando Medina González, especialista en Cloud Computing
- **Biografía**: Extensa biografía con experiencia detallada

### `create_asistente.json`
- **Propósito**: Crear un nuevo asistente
- **Endpoint**: `POST /api/asistentes`
- **Contenido**: Ing. Patricia Morales Herrera
- **Evento**: Se registra al evento ID 2 (Conferencia IA 2024)

## 🚀 Uso Rápido

### Prerequisitos
```bash
# Asegurar que Docker esté corriendo
docker-compose up -d

# Verificar que la API esté disponible
curl http://localhost:8000/api/eventos
```

### Crear Registros
```powershell
# Crear evento
curl -X POST http://localhost:8000/api/eventos -H "Content-Type: application/json" -d (Get-Content test_data/create_evento.json -Raw)

# Crear ponente
curl -X POST http://localhost:8000/api/ponentes -H "Content-Type: application/json" -d (Get-Content test_data/create_ponente.json -Raw)

# Crear asistente
curl -X POST http://localhost:8000/api/asistentes -H "Content-Type: application/json" -d (Get-Content test_data/create_asistente.json -Raw)
```

## 📚 Documentación Adicional

- **`test_commands.md`**: Comandos cURL completos con ejemplos de respuestas
- **`additional_examples.md`**: Más ejemplos JSON y casos de validación de errores

## ✅ Pruebas Realizadas

Los siguientes archivos han sido probados exitosamente:

- ✅ **create_evento.json** - Evento creado con ID 5
- ✅ **create_ponente.json** - Ponente creado con ID 5  
- ✅ **create_asistente.json** - Asistente creado con ID 6

## 🔍 Validaciones Implementadas

### Eventos
- ✅ Fechas futuras obligatorias
- ✅ fecha_fin >= fecha_inicio
- ✅ Todos los campos obligatorios
- ✅ Descripción hasta 10,000 caracteres

### Ponentes  
- ✅ Todos los campos obligatorios
- ✅ Biografía tipo TEXT (sin límite práctico)
- ✅ Especialidad requerida

### Asistentes
- ✅ Email único por evento
- ✅ evento_id debe existir
- ✅ Todos los campos obligatorios
- ✅ Eager loading del evento

## 🧪 Casos de Prueba

### Casos Exitosos
- [x] Crear evento con fechas válidas
- [x] Crear ponente con biografía extensa
- [x] Crear asistente para evento existente
- [x] Verificar relaciones y eager loading

### Casos de Error (documentados)
- [x] Evento con fechas pasadas
- [x] Evento con fechas invertidas  
- [x] Asistente con evento_id inválido
- [x] Email duplicado en el mismo evento

## 💡 Tips para Desarrolladores

1. **Fechas**: Usar siempre formato YYYY-MM-DD con fechas futuras
2. **IDs**: Verificar existencia de eventos antes de crear asistentes
3. **Emails**: Son únicos por evento, no globalmente
4. **Testing**: Usar los archivos JSON como base para pruebas automatizadas

## 🔄 Mantenimiento

Para actualizar las fechas cuando se vuelvan pasadas:
```bash
# Editar create_evento.json y actualizar fecha_inicio y fecha_fin
# Asegurar que fecha_inicio >= fecha_actual
# Asegurar que fecha_fin >= fecha_inicio
```

---
**Última actualización**: 16 de septiembre de 2025  
**Versión API**: Laravel 11 con validación mejorada