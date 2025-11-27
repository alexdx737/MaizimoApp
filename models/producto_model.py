"""
Producto Model - Product management and inventory
"""
from database import get_supabase_client

class ProductoModel:
    """Model for producto table operations"""
    
    @staticmethod
    def listar_todos():
        """
        List all products
        Returns: List of all products
        """
        try:
            supabase = get_supabase_client()
            response = supabase.table('producto')\
                .select('*')\
                .order('nombre')\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"Error listando productos: {e}")
            return []
    
    @staticmethod
    def obtener_por_id(id_producto):
        """Get product by ID"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('producto')\
                .select('*')\
                .eq('id_producto', id_producto)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error obteniendo producto: {e}")
            return None
    
    @staticmethod
    def crear(nombre, stock, unidad_medida, costo_unitario, descripcion=None):
        """
        Create a new product
        Args:
            nombre: Product name
            stock: Initial stock
            unidad_medida: Unit of measure (kg, l, ml, pz)
            costo_unitario: Unit cost
            descripcion: Optional description
        Returns: Created product or None
        """
        try:
            supabase = get_supabase_client()
            
            data = {
                'nombre': nombre,
                'stock': stock,
                'unidad_medida': unidad_medida,
                'costo_unitario': costo_unitario,
                'descripcion': descripcion
            }
            
            response = supabase.table('producto').insert(data).execute()
            return response.data[0] if response.data else None
            
        except Exception as e:
            print(f"Error creando producto: {e}")
            return None
    
    @staticmethod
    def actualizar(id_producto, **kwargs):
        """Update product data"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('producto')\
                .update(kwargs)\
                .eq('id_producto', id_producto)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando producto: {e}")
            return None
    
    @staticmethod
    def actualizar_stock(id_producto, cantidad_cambio):
        """
        Update product stock
        Args:
            id_producto: Product ID
            cantidad_cambio: Amount to add (positive) or subtract (negative)
        Returns: Updated product or None
        """
        try:
            # Get current product
            producto = ProductoModel.obtener_por_id(id_producto)
            if not producto:
                return None
            
            nuevo_stock = float(producto['stock']) + cantidad_cambio
            
            if nuevo_stock < 0:
                print(f"Error: Stock insuficiente para producto {id_producto}")
                return None
            
            return ProductoModel.actualizar(id_producto, stock=nuevo_stock)
            
        except Exception as e:
            print(f"Error actualizando stock: {e}")
            return None
    
    @staticmethod
    def eliminar(id_producto):
        """Delete a product"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('producto')\
                .delete()\
                .eq('id_producto', id_producto)\
                .execute()
            
            return True
        except Exception as e:
            print(f"Error eliminando producto: {e}")
            return False
    
    @staticmethod
    def buscar_por_nombre(nombre):
        """Search products by name"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('producto')\
                .select('*')\
                .ilike('nombre', f'%{nombre}%')\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"Error buscando productos: {e}")
            return []
