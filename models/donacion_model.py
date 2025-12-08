"""
Donacion Model - Donation management
"""
from core.database import get_supabase_client

class DonacionModel:
    """Model for donacion table operations"""
    
    @staticmethod
    def crear(id_venta_completa, monto_redondeo):
        """
        Create a donation record
        Args:
            id_venta_completa: Complete sale ID
            monto_redondeo: Rounding amount donated
        Returns: Created donation or None
        """
        try:
            supabase = get_supabase_client()
            
            data = {
                'id_venta_completa': id_venta_completa,
                'monto_redondeo': monto_redondeo
            }
            
            response = supabase.table('donacion').insert(data).execute()
            return response.data[0] if response.data else None
            
        except Exception as e:
            print(f"Error creando donación: {e}")
            return None
    
    @staticmethod
    def listar_todas():
        """List all donations"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('donacion')\
                .select('*, venta_completa(fecha, hora)')\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"Error listando donaciones: {e}")
            return []
    
    @staticmethod
    def obtener_total():
        """Get total donation amount"""
        try:
            donaciones = DonacionModel.listar_todas()
            total = sum(float(d['monto_redondeo']) for d in donaciones)
            return total
        except Exception as e:
            print(f"Error calculando total de donaciones: {e}")
            return 0.0
    
    @staticmethod
    def obtener_por_fecha(fecha_inicio, fecha_fin):
        """Get donations within date range"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('donacion')\
                .select('*, venta_completa!inner(fecha, hora)')\
                .gte('venta_completa.fecha', fecha_inicio)\
                .lte('venta_completa.fecha', fecha_fin)\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"Error obteniendo donaciones por fecha: {e}")
            return []
