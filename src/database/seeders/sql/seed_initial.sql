USE infotec_laravel;

-- Eventos (solo si no existen con mismo título y fecha de inicio)
INSERT INTO eventos (titulo, descripcion, fecha_inicio, fecha_fin, ubicacion, created_at, updated_at)
SELECT 'Conferencia de IA', 'Evento sobre avances en Inteligencia Artificial', '2025-10-01', '2025-10-02', 'Auditorio Central', NOW(), NOW()
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM eventos WHERE titulo='Conferencia de IA' AND fecha_inicio='2025-10-01' LIMIT 1);
SET @e1 := (SELECT id FROM eventos WHERE titulo='Conferencia de IA' AND fecha_inicio='2025-10-01' LIMIT 1);

INSERT INTO eventos (titulo, descripcion, fecha_inicio, fecha_fin, ubicacion, created_at, updated_at)
SELECT 'Jornada DevOps', 'Prácticas y herramientas de DevOps', '2025-11-05', '2025-11-05', 'Sala de Conferencias B', NOW(), NOW()
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM eventos WHERE titulo='Jornada DevOps' AND fecha_inicio='2025-11-05' LIMIT 1);
SET @e2 := (SELECT id FROM eventos WHERE titulo='Jornada DevOps' AND fecha_inicio='2025-11-05' LIMIT 1);

INSERT INTO eventos (titulo, descripcion, fecha_inicio, fecha_fin, ubicacion, created_at, updated_at)
SELECT 'Seminario Data Science', 'Talleres y casos de uso en Data Science', '2025-12-10', '2025-12-11', 'Centro de Convenciones', NOW(), NOW()
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM eventos WHERE titulo='Seminario Data Science' AND fecha_inicio='2025-12-10' LIMIT 1);
SET @e3 := (SELECT id FROM eventos WHERE titulo='Seminario Data Science' AND fecha_inicio='2025-12-10' LIMIT 1);

-- Ponentes (solo si no existen por nombre y especialidad)
INSERT INTO ponentes (nombre, biografia, especialidad, created_at, updated_at)
SELECT 'Ana Pérez', 'Ingeniera en IA con 10 años de experiencia', 'Inteligencia Artificial', NOW(), NOW()
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM ponentes WHERE nombre='Ana Pérez' AND especialidad='Inteligencia Artificial' LIMIT 1);
SET @p1 := (SELECT id FROM ponentes WHERE nombre='Ana Pérez' LIMIT 1);

INSERT INTO ponentes (nombre, biografia, especialidad, created_at, updated_at)
SELECT 'Carlos Gómez', 'Ingeniero DevOps y líder de equipos', 'DevOps', NOW(), NOW()
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM ponentes WHERE nombre='Carlos Gómez' AND especialidad='DevOps' LIMIT 1);
SET @p2 := (SELECT id FROM ponentes WHERE nombre='Carlos Gómez' LIMIT 1);

INSERT INTO ponentes (nombre, biografia, especialidad, created_at, updated_at)
SELECT 'Lucía Martínez', 'Científica de datos especializada en ML', 'Data Science', NOW(), NOW()
FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM ponentes WHERE nombre='Lucía Martínez' AND especialidad='Data Science' LIMIT 1);
SET @p3 := (SELECT id FROM ponentes WHERE nombre='Lucía Martínez' LIMIT 1);

-- Asociar ponentes a eventos (evita duplicados con INSERT IGNORE)
INSERT IGNORE INTO evento_ponente (evento_id, ponente_id, created_at, updated_at) VALUES
(@e1, @p1, NOW(), NOW()),
(@e2, @p2, NOW(), NOW()),
(@e3, @p3, NOW(), NOW());

-- Asistentes (INSERT IGNORE para evitar duplicados por unique(email, evento_id))
-- Evento 1
INSERT IGNORE INTO asistentes (nombre, email, telefono, evento_id, created_at, updated_at) VALUES
('María López', 'maria.lopez@example.com', '555-0101', @e1, NOW(), NOW()),
('Pedro Ruiz', 'pedro.ruiz@example.com', '555-0102', @e1, NOW(), NOW()),
('Sofía Torres', 'sofia.torres@example.com', '555-0103', @e1, NOW(), NOW());

-- Evento 2
INSERT IGNORE INTO asistentes (nombre, email, telefono, evento_id, created_at, updated_at) VALUES
('Diego Fernández', 'diego.fernandez@example.com', '555-0201', @e2, NOW(), NOW()),
('Laura Ramos', 'laura.ramos@example.com', '555-0202', @e2, NOW(), NOW()),
('Andrés Peña', 'andres.pena@example.com', '555-0203', @e2, NOW(), NOW());

-- Evento 3
INSERT IGNORE INTO asistentes (nombre, email, telefono, evento_id, created_at, updated_at) VALUES
('Valeria Cruz', 'valeria.cruz@example.com', '555-0301', @e3, NOW(), NOW()),
('Óscar Medina', 'oscar.medina@example.com', '555-0302', @e3, NOW(), NOW()),
('Nora Villegas', 'nora.villegas@example.com', '555-0303', @e3, NOW(), NOW());
