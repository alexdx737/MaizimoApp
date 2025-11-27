"""
Cliente Model - Customer management
"""
from database import get_supabase_client

class ClienteModel:
    """Model for cliente table operations"""
    
    @staticmethod
    def listar_todos():
        """List all clients"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('cliente')\
                .select('*')\
                .order('nombre')\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"Error listando clientes: {e}")
            return []
    
    @staticmethod
    def obtener_por_id(id_cliente):
        """Get client by ID"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('cliente')\
                .select('*')\
                .eq('id_cliente', id_cliente)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error obteniendo cliente: {e}")
            return None
    
    @staticmethod
    def crear(nombre, apellido_paterno, telefono, apellido_materno=None, 
              direccion=None, descuento=0.0, descripcion=None):
        """
        Create a new client
        Args:
            nombre: First name
            apellido_paterno: Last name
            telefono: Phone number
            apellido_materno: Mother's last name (optional)
            direccion: Address (optional)
            descuento: Discount percentage (default 0)
            descripcion: Description (optional)
        Returns: Created client or None
        """
        try:
            supabase = get_supabase_client()
            
            data = {
                'nombre': nombre,
                'apellido_paterno': apellido_paterno,
                'apellido_materno': apellido_materno,
                'direccion': direccion,
                'telefono': telefono,
                'descuento': descuento,
                'descripcion': descripcion
            }
            
            response = supabase.table('cliente').insert(data).execute()
            return response.data[0] if response.data else None
            
        except Exception as e:
            print(f"Error creando cliente: {e}")
            return None
    
    @staticmethod
    def actualizar(id_cliente, **kwargs):
        """Update client data"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('cliente')\
                .update(kwargs)\
                .eq('id_cliente', id_cliente)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando cliente: {e}")
            return None
    
    @staticmethod
    def eliminar(id_cliente):
        """Delete a client"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('cliente')\
                .delete()\
                .eq('id_cliente', id_cliente)\
                .execute()
            
            return True
        except Exception as e:
            print(f"Error eliminando cliente: {e}")
            return False
    
    @staticmethod
    def buscar(termino):
        """
        Search clients by name or phone
        Args:
            termino: Search term
        Returns: List of matching clients
        """
        try:
            supabase = get_supabase_client()
            
            # Search in nombre, apellido_paterno, or telefono
            response = supabase.table('cliente')\
                .select('*')\
                .or_(f'nombre.ilike.%{termino}%,apellido_paterno.ilike.%{termino}%,telefono.ilike.%{termino}%')\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"Error buscando clientes: {e}")
            return []
