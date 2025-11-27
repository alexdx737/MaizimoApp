-- SCRIPT ADICIONAL: Deshabilitar RLS temporalmente para pruebas
-- Ejecuta esto en Supabase SQL Editor si tienes problemas de acceso

-- Opción 1: Deshabilitar RLS completamente (solo para desarrollo/pruebas)
ALTER TABLE cliente DISABLE ROW LEVEL SECURITY;
ALTER TABLE empleado DISABLE ROW LEVEL SECURITY;
ALTER TABLE usuario DISABLE ROW LEVEL SECURITY;
ALTER TABLE producto DISABLE ROW LEVEL SECURITY;
ALTER TABLE venta_completa DISABLE ROW LEVEL SECURITY;
ALTER TABLE venta DISABLE ROW LEVEL SECURITY;
ALTER TABLE donacion DISABLE ROW LEVEL SECURITY;

-- Opción 2: Mantener RLS pero permitir acceso público (más seguro)
-- Descomenta las siguientes líneas si prefieres esta opción:

/*
-- Eliminar políticas existentes
DROP POLICY IF EXISTS "Allow all operations for authenticated users" ON cliente;
DROP POLICY IF EXISTS "Allow all operations for authenticated users" ON empleado;
DROP POLICY IF EXISTS "Allow all operations for authenticated users" ON usuario;
DROP POLICY IF EXISTS "Allow all operations for authenticated users" ON producto;
DROP POLICY IF EXISTS "Allow all operations for authenticated users" ON venta_completa;
DROP POLICY IF EXISTS "Allow all operations for authenticated users" ON venta;
DROP POLICY IF EXISTS "Allow all operations for authenticated users" ON donacion;

-- Crear políticas permisivas para todos
CREATE POLICY "Allow all for anon" ON cliente FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon" ON empleado FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon" ON usuario FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon" ON producto FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon" ON venta_completa FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon" ON venta FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon" ON donacion FOR ALL USING (true) WITH CHECK (true);
*/
