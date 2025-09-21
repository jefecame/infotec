USE infotec_laravel;

-- Insertar 3 eventos
INSERT INTO eventos (titulo, descripcion, fecha_inicio, fecha_fin, ubicacion, created_at, updated_at) VALUES
('Conferencia de IA', 'Evento sobre avances en Inteligencia Artificial', '2025-10-01', '2025-10-02', 'Auditorio Central', NOW(), NOW()),
('Jornada DevOps', 'Prácticas y herramientas de DevOps', '2025-11-05', '2025-11-05', 'Sala de Conferencias B', NOW(), NOW()),
('Seminario Data Science', 'Talleres y casos de uso en Data Science', '2025-12-10', '2025-12-11', 'Centro de Convenciones', NOW(), NOW());

-- Insertar 3 ponentes (uno por evento)
INSERT INTO ponentes (nombre, biografia, especialidad, created_at, updated_at) VALUES
('Ana Pérez', 'Ingeniera en IA con 10 años de experiencia', 'Inteligencia Artificial', NOW(), NOW()),
('Carlos Gómez', 'Ingeniero DevOps y líder de equipos', 'DevOps', NOW(), NOW()),
('Lucía Martínez', 'Científica de datos especializada en ML', 'Data Science', NOW(), NOW());

-- Asociar ponentes a eventos (evento_ponente)
-- Asumo que los IDs se asignan en el orden insertado: eventos 1..3, ponentes 1..3
INSERT INTO evento_ponente (evento_id, ponente_id, created_at, updated_at) VALUES
(1, 1, NOW(), NOW()),
(2, 2, NOW(), NOW()),
(3, 3, NOW(), NOW());

-- Insertar 3 asistentes por cada evento
INSERT INTO asistentes (nombre, email, telefono, evento_id, created_at, updated_at) VALUES
-- Evento 1
('María López', 'maria.lopez@example.com', '555-0101', 1, NOW(), NOW()),
('Pedro Ruiz', 'pedro.ruiz@example.com', '555-0102', 1, NOW(), NOW()),
('Sofía Torres', 'sofia.torres@example.com', '555-0103', 1, NOW(), NOW()),
-- Evento 2
('Diego Fernández', 'diego.fernandez@example.com', '555-0201', 2, NOW(), NOW()),
('Laura Ramos', 'laura.ramos@example.com', '555-0202', 2, NOW(), NOW()),
('Andrés Peña', 'andres.pena@example.com', '555-0203', 2, NOW(), NOW()),
-- Evento 3
('Valeria Cruz', 'valeria.cruz@example.com', '555-0301', 3, NOW(), NOW()),
('Óscar Medina', 'oscar.medina@example.com', '555-0302', 3, NOW(), NOW()),
('Nora Villegas', 'nora.villegas@example.com', '555-0303', 3, NOW(), NOW());

