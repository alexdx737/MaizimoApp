-- Migration: Add redondeo_aplicado field to venta_completa table
-- Date: 2025-12-01
-- Purpose: Track whether the user selected the rounding option for donations

-- Add the new column
ALTER TABLE venta_completa 
ADD COLUMN redondeo_aplicado BOOLEAN NOT NULL DEFAULT FALSE;

-- Add comment to document the field
COMMENT ON COLUMN venta_completa.redondeo_aplicado IS 'Indica si el usuario marcó la opción de redondeo para donación';

-- Optional: Update existing records based on whether they have donations
-- This is optional - you can skip this if you want all existing records to show "No"
UPDATE venta_completa vc
SET redondeo_aplicado = TRUE
WHERE EXISTS (
    SELECT 1 FROM donacion d 
    WHERE d.id_venta_completa = vc.id_venta_completa
);
