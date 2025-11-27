-- Maizimo App - PostgreSQL Schema for Supabase
-- Converted from MySQL to PostgreSQL

-- Enable UUID extension (useful for future features)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ========================================
-- Table: cliente
-- ========================================
CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50),
    direccion VARCHAR(200),
    telefono CHAR(20) NOT NULL,
    descuento DECIMAL(7,2) NOT NULL DEFAULT 0,
    descripcion VARCHAR(200)
);

-- ========================================
-- Table: empleado
-- ========================================
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
-- Table: usuario
-- ========================================
CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    id_empleado INTEGER NOT NULL,
    contraseña VARCHAR(255) NOT NULL,  -- Increased for hashed passwords
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('administrador', 'trabajador')),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
);

-- ========================================
-- Table: producto
-- ========================================
CREATE TABLE producto (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    stock DECIMAL(8,2) NOT NULL DEFAULT 0,
    unidad_medida VARCHAR(10) NOT NULL CHECK (unidad_medida IN ('kg', 'l', 'ml', 'pz')),
    costo_unitario DECIMAL(5,2) NOT NULL,
    descripcion VARCHAR(200)
);

-- ========================================
-- Table: venta_completa
-- ========================================
CREATE TABLE venta_completa (
    id_venta_completa SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    monto_total DECIMAL(8,2) NOT NULL,
    id_cliente INTEGER NOT NULL,
    hora TIME NOT NULL,
    descuento_bolsa BOOLEAN NOT NULL DEFAULT FALSE,
    descripcion VARCHAR(200),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

-- ========================================
-- Table: venta
-- ========================================
CREATE TABLE venta (
    id_venta SERIAL PRIMARY KEY,
    id_producto INTEGER NOT NULL,
    cantidad_vendida DECIMAL(4,2) NOT NULL,
    unidad_medida VARCHAR(10) NOT NULL CHECK (unidad_medida IN ('kg', 'l', 'ml', 'pz')),
    subtotal DECIMAL(7,2) NOT NULL,
    id_venta_completa INTEGER NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
    FOREIGN KEY (id_venta_completa) REFERENCES venta_completa(id_venta_completa)
);

-- ========================================
-- Table: donacion
-- ========================================
CREATE TABLE donacion (
    id_donacion SERIAL PRIMARY KEY,
    id_venta_completa INTEGER NOT NULL,
    monto_redondeo DECIMAL(6,2) NOT NULL,
    FOREIGN KEY (id_venta_completa) REFERENCES venta_completa(id_venta_completa)
);

-- ========================================
-- Indexes for better performance
-- ========================================
CREATE INDEX idx_usuario_empleado ON usuario(id_empleado);
CREATE INDEX idx_venta_producto ON venta(id_producto);
CREATE INDEX idx_venta_venta_completa ON venta(id_venta_completa);
CREATE INDEX idx_venta_completa_cliente ON venta_completa(id_cliente);
CREATE INDEX idx_venta_completa_fecha ON venta_completa(fecha);
CREATE INDEX idx_donacion_venta_completa ON donacion(id_venta_completa);

-- ========================================
-- Row Level Security (RLS) Policies
-- ========================================
-- Enable RLS on all tables
ALTER TABLE cliente ENABLE ROW LEVEL SECURITY;
ALTER TABLE empleado ENABLE ROW LEVEL SECURITY;
ALTER TABLE usuario ENABLE ROW LEVEL SECURITY;
ALTER TABLE producto ENABLE ROW LEVEL SECURITY;
ALTER TABLE venta_completa ENABLE ROW LEVEL SECURITY;
ALTER TABLE venta ENABLE ROW LEVEL SECURITY;
ALTER TABLE donacion ENABLE ROW LEVEL SECURITY;

-- Allow service role to bypass RLS (for backend operations)
-- For now, we'll create permissive policies for authenticated users
-- You can customize these based on your security requirements

CREATE POLICY "Allow all operations for authenticated users" ON cliente
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all operations for authenticated users" ON empleado
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all operations for authenticated users" ON usuario
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all operations for authenticated users" ON producto
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all operations for authenticated users" ON venta_completa
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all operations for authenticated users" ON venta
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all operations for authenticated users" ON donacion
    FOR ALL USING (true) WITH CHECK (true);

-- ========================================
-- Sample Data (Optional - for testing)
-- ========================================
-- Insert a test employee
INSERT INTO empleado (nombre, apellido_paterno, apellido_materno, curp, fecha_ingreso, vulnerable, ciclo, descripcion)
VALUES ('Admin', 'Sistema', NULL, 'XXXX000000HDFXXX00', CURRENT_DATE, FALSE, 'finalizado', 'Usuario administrador del sistema');

-- Insert a test user (password: admin123 - you should hash this in production)
INSERT INTO usuario (id_empleado, contraseña, rol, activo)
VALUES (1, 'admin123', 'administrador', TRUE);

-- Insert sample products
INSERT INTO producto (nombre, stock, unidad_medida, costo_unitario, descripcion) VALUES
('Tortillas', 100.00, 'kg', 25.00, 'Tortillas de maíz tradicionales'),
('Tostadas', 50.00, 'pz', 15.00, 'Tostadas crujientes'),
('Chips', 30.00, 'pz', 20.00, 'Chips de tortilla'),
('Tamales', 25.00, 'pz', 12.00, 'Tamales de diversos sabores');

-- Insert a sample client
INSERT INTO cliente (nombre, apellido_paterno, apellido_materno, direccion, telefono, descuento, descripcion)
VALUES ('Cliente', 'General', NULL, 'Sin dirección específica', '0000000000', 0.00, 'Cliente general para ventas sin registro');

COMMENT ON TABLE cliente IS 'Clientes mayoristas y frecuentes';
COMMENT ON TABLE empleado IS 'Empleados de la tortillería';
COMMENT ON TABLE usuario IS 'Usuarios del sistema con credenciales de acceso';
COMMENT ON TABLE producto IS 'Productos disponibles para venta';
COMMENT ON TABLE venta_completa IS 'Registro de ventas completas';
COMMENT ON TABLE venta IS 'Detalles de productos vendidos en cada venta';
COMMENT ON TABLE donacion IS 'Donaciones generadas por redondeo de ventas';
