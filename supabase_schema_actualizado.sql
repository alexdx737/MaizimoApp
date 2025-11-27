-- Maizimo App - PostgreSQL Schema for Supabase (ACTUALIZADO)
-- Basado en especificaciones exactas del usuario

-- Enable UUID extension (útil para futuras funcionalidades)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ========================================
-- Tabla: cliente
-- ========================================
-- CAMBIOS JUSTIFICADOS:
-- - VARCHAR en lugar de TEXTO para compatibilidad estándar SQL
-- - DECIMAL(7,2) mantiene 2 decimales para el descuento (ej: 99999.99)
CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,  -- SERIAL = autoincrement en PostgreSQL
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50),
    direccion VARCHAR(200),
    telefono CHAR(20) NOT NULL,
    descuento DECIMAL(7,2) NOT NULL DEFAULT 0,
    descripcion VARCHAR(200)
);

-- ========================================
-- Tabla: empleado
-- ========================================
-- CAMBIOS JUSTIFICADOS:
-- - VARCHAR en lugar de TEXT para campos con límite de caracteres
-- - CURP es UNIQUE para evitar duplicados
-- - CHECK constraint para validar valores de ciclo
CREATE TABLE empleado (
    id_empleado SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50),
    curp VARCHAR(22) NOT NULL UNIQUE,
    fecha_ingreso DATE NOT NULL,
    vulnerable BOOLEAN NOT NULL DEFAULT FALSE,
    ciclo VARCHAR(20) NOT NULL CHECK (ciclo IN ('espera', 'proceso', 'finalizado')),
    descripcion VARCHAR(200)
);

-- ========================================
-- Tabla: usuario
-- ========================================
-- CAMBIOS JUSTIFICADOS:
-- - VARCHAR(50) para contraseña según especificación del usuario
-- - CHECK constraint para validar rol
CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    id_empleado INTEGER NOT NULL,
    contraseña VARCHAR(50) NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('administrador', 'trabajador')),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado) ON DELETE CASCADE
);

-- ========================================
-- Tabla: producto
-- ========================================
-- CAMBIOS JUSTIFICADOS:
-- - DECIMAL(8,2) para stock permite valores como 999999.99
-- - DECIMAL(5,2) para costo_unitario permite valores como 999.99
-- - CHECK constraint para validar unidad_medida
CREATE TABLE producto (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    stock DECIMAL(8,2) NOT NULL DEFAULT 0,
    unidad_medida VARCHAR(10) NOT NULL CHECK (unidad_medida IN ('kg', 'l', 'ml', 'pz')),
    costo_unitario DECIMAL(5,2) NOT NULL,
    descripcion VARCHAR(200)
);

-- ========================================
-- Tabla: venta_completa
-- ========================================
-- CAMBIOS JUSTIFICADOS:
-- - DECIMAL(8,2) para monto_total permite valores hasta 999999.99
-- - TIME para hora (formato HH:MM:SS)
-- - ON DELETE RESTRICT para evitar eliminar clientes con ventas
CREATE TABLE venta_completa (
    id_venta_completa SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    monto_total DECIMAL(8,2) NOT NULL,
    id_cliente INTEGER NOT NULL,
    hora TIME NOT NULL,
    descuento_bolsa BOOLEAN NOT NULL DEFAULT FALSE,
    descripcion VARCHAR(200),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE RESTRICT
);

-- ========================================
-- Tabla: venta
-- ========================================
-- CAMBIOS JUSTIFICADOS:
-- - DECIMAL(4,2) para cantidad_vendida permite valores como 99.99
-- - DECIMAL(7,2) para subtotal permite valores como 99999.99
-- - CHECK constraint para validar unidad_medida
-- - ON DELETE CASCADE para eliminar items si se elimina la venta completa
CREATE TABLE venta (
    id_venta SERIAL PRIMARY KEY,
    id_producto INTEGER NOT NULL,
    cantidad_vendida DECIMAL(4,2) NOT NULL,
    unidad_medida VARCHAR(10) NOT NULL CHECK (unidad_medida IN ('kg', 'l', 'ml', 'pz')),
    subtotal DECIMAL(7,2) NOT NULL,
    id_venta_completa INTEGER NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto) ON DELETE RESTRICT,
    FOREIGN KEY (id_venta_completa) REFERENCES venta_completa(id_venta_completa) ON DELETE CASCADE
);

-- ========================================
-- Tabla: donacion
-- ========================================
-- CAMBIOS JUSTIFICADOS:
-- - DECIMAL(6,2) para monto_redondeo permite valores como 9999.99
-- - ON DELETE CASCADE para eliminar donación si se elimina la venta
CREATE TABLE donacion (
    id_donacion SERIAL PRIMARY KEY,
    id_venta_completa INTEGER NOT NULL,
    monto_redondeo DECIMAL(6,2) NOT NULL,
    FOREIGN KEY (id_venta_completa) REFERENCES venta_completa(id_venta_completa) ON DELETE CASCADE
);

-- ========================================
-- Índices para mejor rendimiento
-- ========================================
CREATE INDEX idx_usuario_empleado ON usuario(id_empleado);
CREATE INDEX idx_venta_producto ON venta(id_producto);
CREATE INDEX idx_venta_venta_completa ON venta(id_venta_completa);
CREATE INDEX idx_venta_completa_cliente ON venta_completa(id_cliente);
CREATE INDEX idx_venta_completa_fecha ON venta_completa(fecha);
CREATE INDEX idx_donacion_venta_completa ON donacion(id_venta_completa);
CREATE INDEX idx_empleado_curp ON empleado(curp);

-- ========================================
-- Row Level Security (RLS) - DESHABILITADO para desarrollo
-- ========================================
-- Para desarrollo, RLS está deshabilitado
-- Para producción, habilita y configura políticas apropiadas

ALTER TABLE cliente DISABLE ROW LEVEL SECURITY;
ALTER TABLE empleado DISABLE ROW LEVEL SECURITY;
ALTER TABLE usuario DISABLE ROW LEVEL SECURITY;
ALTER TABLE producto DISABLE ROW LEVEL SECURITY;
ALTER TABLE venta_completa DISABLE ROW LEVEL SECURITY;
ALTER TABLE venta DISABLE ROW LEVEL SECURITY;
ALTER TABLE donacion DISABLE ROW LEVEL SECURITY;

-- ========================================
-- Datos de prueba
-- ========================================

-- Insertar empleado de prueba
INSERT INTO empleado (nombre, apellido_paterno, apellido_materno, curp, fecha_ingreso, vulnerable, ciclo, descripcion)
VALUES ('Admin', 'Sistema', NULL, 'XXXX000000HDFXXX00', CURRENT_DATE, FALSE, 'finalizado', 'Usuario administrador del sistema');

-- Insertar usuario de prueba (contraseña: admin123)
-- NOTA: En producción, usa bcrypt para hashear la contraseña
INSERT INTO usuario (id_empleado, contraseña, rol, activo)
VALUES (1, 'admin123', 'administrador', TRUE);

-- Insertar productos de prueba
INSERT INTO producto (nombre, stock, unidad_medida, costo_unitario, descripcion) VALUES
('Tortillas', 100.00, 'kg', 25.00, 'Tortillas de maíz tradicionales'),
('Tostadas', 50.00, 'pz', 15.00, 'Tostadas crujientes'),
('Chips', 30.00, 'pz', 20.00, 'Chips de tortilla'),
('Tamales', 25.00, 'pz', 12.00, 'Tamales de diversos sabores');

-- Insertar cliente general
INSERT INTO cliente (nombre, apellido_paterno, apellido_materno, direccion, telefono, descuento, descripcion)
VALUES ('Cliente', 'General', NULL, 'Sin dirección específica', '0000000000', 0.00, 'Cliente general para ventas sin registro');

-- ========================================
-- Comentarios en las tablas
-- ========================================
COMMENT ON TABLE cliente IS 'Clientes mayoristas y frecuentes';
COMMENT ON TABLE empleado IS 'Empleados de la tortillería';
COMMENT ON TABLE usuario IS 'Usuarios del sistema con credenciales de acceso';
COMMENT ON TABLE producto IS 'Productos disponibles para venta';
COMMENT ON TABLE venta_completa IS 'Registro de ventas completas';
COMMENT ON TABLE venta IS 'Detalles de productos vendidos en cada venta';
COMMENT ON TABLE donacion IS 'Donaciones generadas por redondeo de ventas';

-- ========================================
-- RESUMEN DE CAMBIOS JUSTIFICADOS
-- ========================================
-- 1. SERIAL en lugar de INT AUTOINCREMENT (equivalente en PostgreSQL)
-- 2. VARCHAR en lugar de TEXT para campos con límite específico (mejor rendimiento)
-- 3. CHECK constraints en lugar de ENUM (más flexible en PostgreSQL)
-- 4. VARCHAR(50) para contraseña según especificación del usuario
-- 5. ON DELETE CASCADE/RESTRICT para mantener integridad referencial
-- 6. Índices adicionales para optimizar consultas frecuentes
-- 7. UNIQUE en CURP para evitar duplicados de empleados
