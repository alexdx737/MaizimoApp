# Instrucciones para Aplicar la Corrección del Redondeo

## Problema Solucionado
El sistema ahora guardará correctamente si marcaste el checkbox de "Redondear para donación" en el historial de ventas.

## Pasos para Aplicar la Corrección

### 1. Ejecutar la Migración en Supabase

1. Abre tu proyecto en [Supabase](https://supabase.com)
2. Ve a **SQL Editor** en el menú lateral
3. Crea una nueva query
4. Copia y pega el contenido del archivo `migration_add_redondeo_aplicado.sql`
5. Haz clic en **Run** para ejecutar la migración

**Contenido del script:**
```sql
-- Add the new column
ALTER TABLE venta_completa 
ADD COLUMN redondeo_aplicado BOOLEAN NOT NULL DEFAULT FALSE;

-- Add comment to document the field
COMMENT ON COLUMN venta_completa.redondeo_aplicado IS 'Indica si el usuario marcó la opción de redondeo para donación';

-- Optional: Update existing records based on whether they have donations
UPDATE venta_completa vc
SET redondeo_aplicado = TRUE
WHERE EXISTS (
    SELECT 1 FROM donacion d 
    WHERE d.id_venta_completa = vc.id_venta_completa
);
```

### 2. Verificar que la Migración Funcionó

En el SQL Editor de Supabase, ejecuta:
```sql
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'venta_completa' AND column_name = 'redondeo_aplicado';
```

Deberías ver una fila que confirma que la columna existe.

### 3. Probar la Aplicación

1. **Reinicia la aplicación** si está corriendo
2. **Realiza una venta CON redondeo:**
   - Agrega productos al carrito
   - ✅ Marca el checkbox "Redondear para donación de tortillas"
   - Completa la venta
   - Verifica en el historial que muestre **"Sí"** en la columna Redondeo

3. **Realiza una venta SIN redondeo:**
   - Agrega productos al carrito
   - ❌ NO marques el checkbox de redondeo
   - Completa la venta
   - Verifica en el historial que muestre **"No"** en la columna Redondeo

## Archivos Modificados

- ✅ `migration_add_redondeo_aplicado.sql` - Script de migración SQL
- ✅ `models/venta_model.py` - Actualizado para guardar `redondeo_aplicado`
- ✅ `controllers/punto_venta_controller.py` - Actualizado para leer `redondeo_aplicado`

## Notas Importantes

- ⚠️ **Debes ejecutar la migración SQL antes de usar la aplicación**, de lo contrario obtendrás un error al intentar crear una venta.
- 📊 Las ventas existentes se actualizarán automáticamente: si tienen donación, se marcará `redondeo_aplicado = TRUE`
- 🔄 No necesitas modificar ningún otro archivo, los cambios son retrocompatibles

## ¿Problemas?

Si encuentras algún error al ejecutar la migración:
1. Verifica que estés conectado a la base de datos correcta
2. Asegúrate de tener permisos de administrador
3. Si la columna ya existe, puedes omitir el `ALTER TABLE` y solo ejecutar el `UPDATE`
