-- Script para MIGRAR de schema antiguo a schema actualizado
-- Ejecuta esto SOLO si ya tienes datos que quieres conservar

-- PASO 1: Respaldar datos existentes (opcional pero recomendado)
-- Puedes exportar desde Supabase Dashboard → Table Editor → Export

-- PASO 2: Eliminar tablas en orden correcto (respetando foreign keys)
DROP TABLE IF EXISTS donacion CASCADE;
DROP TABLE IF EXISTS venta CASCADE;
DROP TABLE IF EXISTS venta_completa CASCADE;
DROP TABLE IF EXISTS usuario CASCADE;
DROP TABLE IF EXISTS producto CASCADE;
DROP TABLE IF EXISTS empleado CASCADE;
DROP TABLE IF EXISTS cliente CASCADE;

-- PASO 3: Ahora ejecuta el contenido completo de supabase_schema_actualizado.sql

-- NOTA: Este script eliminará TODOS los datos
-- Si necesitas conservar datos, exporta primero desde Supabase
