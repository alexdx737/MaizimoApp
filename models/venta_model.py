"""
Venta Model - Sales management
"""
from core.database import get_supabase_client
from datetime import datetime, date, time
from models.producto_model import ProductoModel

class VentaModel:
    """Model for venta and venta_completa tables"""
    
    @staticmethod
    def crear_venta_completa(id_cliente, monto_total, descripcion=None, fecha=None, hora=None):
        """
        Create a complete sale record
        Args:
            id_cliente: Client ID
            monto_total: Total amount (already includes all discounts applied)
            descripcion: Optional description
            fecha: Sale date (default: today)
            hora: Sale time (default: now)
        Returns: Created venta_completa or None
        """
        try:
            supabase = get_supabase_client()
            
            if fecha is None:
                fecha = date.today().isoformat()
            if hora is None:
                hora = datetime.now().time().isoformat()
            
            data = {
                'fecha': fecha,
                'monto_total': monto_total,
                'id_cliente': id_cliente,
                'hora': hora,
                'descripcion': descripcion
            }
            
            response = supabase.table('venta_completa').insert(data).execute()
            return response.data[0] if response.data else None
            
        except Exception as e:
            print(f"Error creando venta completa: {e}")
            return None
    
    @staticmethod
    def agregar_item_venta(id_venta_completa, id_producto, cantidad_vendida, 
                          unidad_medida, subtotal):
        """
        Add an item to a sale
        Args:
            id_venta_completa: Complete sale ID
            id_producto: Product ID
            cantidad_vendida: Quantity sold
            unidad_medida: Unit of measure
            subtotal: Item subtotal
        Returns: Created venta item or None
        """
        try:
            supabase = get_supabase_client()
            
            data = {
                'id_producto': id_producto,
                'cantidad_vendida': cantidad_vendida,
                'unidad_medida': unidad_medida,
                'subtotal': subtotal,
                'id_venta_completa': id_venta_completa
            }
            
            response = supabase.table('venta').insert(data).execute()
            
            # Update product stock
            if response.data:
                ProductoModel.actualizar_stock(id_producto, -cantidad_vendida)
            
            return response.data[0] if response.data else None
            
        except Exception as e:
            print(f"Error agregando item a venta: {e}")
            return None
    
    @staticmethod
    def procesar_venta(carrito, id_cliente, descuento_bolsa=False, redondeo=False, monto_pago=0):
        """
        Process a complete sale with multiple items
        Args:
            carrito: List of cart items [{id_producto, cantidad, precio, nombre}]
            id_cliente: Client ID
            descuento_bolsa: Apply bag discount
            redondeo: Donate the change
            monto_pago: Amount paid by customer
        Returns: venta_completa ID or None
        """
        try:
            from models.cliente_model import ClienteModel
            
            # Calculate subtotal
            subtotal = sum(item['precio'] * item['cantidad'] for item in carrito)
            
            # Get client discount percentage
            cliente = ClienteModel.obtener_por_id(id_cliente)
            descuento_porcentaje = cliente.get('descuento', 0) if cliente else 0
            
            # Calculate client discount amount
            descuento_cliente_monto = (subtotal * descuento_porcentaje / 100.0) if descuento_porcentaje > 0 else 0.0
            
            # Apply bag discount (fixed $2.00)
            descuento_bolsa_monto = 2.0 if descuento_bolsa and subtotal >= 2.0 else 0.0
            
            # Calculate total
            total = max(subtotal - descuento_cliente_monto - descuento_bolsa_monto, 0.0)
            
            # Calculate donation from change (if redondeo is enabled and customer paid more than total)
            if redondeo and monto_pago > total:
                monto_donacion = monto_pago - total
            else:
                monto_donacion = 0.0
            
            # Create venta_completa (total already includes all discounts)
            venta_completa = VentaModel.crear_venta_completa(
                id_cliente=id_cliente,
                monto_total=total,
                descripcion=f"Venta con {len(carrito)} productos"
            )
            
            if not venta_completa:
                return None
            
            id_venta_completa = venta_completa['id_venta_completa']
            
            # Add each item
            for item in carrito:
                item_subtotal = item['precio'] * item['cantidad']
                VentaModel.agregar_item_venta(
                    id_venta_completa=id_venta_completa,
                    id_producto=item['id_producto'],
                    cantidad_vendida=item['cantidad'],
                    unidad_medida=item.get('unidad_medida', 'pz'),
                    subtotal=item_subtotal
                )
            
            # Create donation if customer donated their change
            if monto_donacion > 0:
                from models.donacion_model import DonacionModel
                DonacionModel.crear(id_venta_completa, monto_donacion)
            
            return id_venta_completa
            
        except Exception as e:
            print(f"Error procesando venta: {e}")
            return None
    
    @staticmethod
    def obtener_venta_completa(id_venta_completa):
        """Get complete sale with all items and donation info"""
        try:
            supabase = get_supabase_client()
            
            # Get venta_completa with cliente and donacion
            response = supabase.table('venta_completa')\
                .select('*, cliente(*), donacion(*)')\
                .eq('id_venta_completa', id_venta_completa)\
                .execute()
            
            if not response.data:
                return None
            
            venta = response.data[0]
            
            # Get items
            items_response = supabase.table('venta')\
                .select('*, producto(*)')\
                .eq('id_venta_completa', id_venta_completa)\
                .execute()
            
            venta['items'] = items_response.data
            
            return venta
            
        except Exception as e:
            print(f"Error obteniendo venta completa: {e}")
            return None
    
    @staticmethod
    def listar_ventas(fecha_inicio=None, fecha_fin=None, limit=100):
        """List sales with optional date filter"""
        try:
            supabase = get_supabase_client()
            
            query = supabase.table('venta_completa')\
                .select('*, cliente(*), donacion(*)')\
                .order('fecha', desc=True)\
                .order('hora', desc=True)\
                .limit(limit)
            
            if fecha_inicio:
                query = query.gte('fecha', fecha_inicio)
            if fecha_fin:
                query = query.lte('fecha', fecha_fin)
            
            response = query.execute()
            return response.data
            
        except Exception as e:
            print(f"Error listando ventas: {e}")
            return []
