-- SQL para crear la tabla items en RDS MySQL con campo de fecha

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at)
);

-- Insertar datos de prueba con diferentes fechas (opcional)
INSERT INTO items (name, created_at) VALUES 
    ('Ejemplo 1', NOW()),
    ('Ejemplo 2', DATE_SUB(NOW(), INTERVAL 1 DAY)),
    ('Ejemplo 3', DATE_SUB(NOW(), INTERVAL 7 DAY));
