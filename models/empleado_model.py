"""
Empleado Model - Employee management
"""
from core.database import get_supabase_client

class EmpleadoModel:
    """Model for empleado table operations"""
    
    @staticmethod
    def listar_todos():
        """List all employees"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('empleado')\
                .select('*')\
                .order('nombre')\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"Error listando empleados: {e}")
            return []
    
    @staticmethod
    def obtener_por_id(id_empleado):
        """Get employee by ID"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('empleado')\
                .select('*')\
                .eq('id_empleado', id_empleado)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error obteniendo empleado: {e}")
            return None
    
    @staticmethod
    def crear(nombre, apellido_paterno, curp, fecha_ingreso, vulnerable=False,
              ciclo='espera', apellido_materno=None, descripcion=None):
        """
        Create a new employee
        Args:
            nombre: First name
            apellido_paterno: Last name
            curp: CURP (unique identifier)
            fecha_ingreso: Hire date
            vulnerable: Vulnerable status
            ciclo: Cycle status (espera, proceso, finalizado)
            apellido_materno: Mother's last name (optional)
            descripcion: Description (optional)
        Returns: Created employee or None
        """
        try:
            supabase = get_supabase_client()
            
            data = {
                'nombre': nombre,
                'apellido_paterno': apellido_paterno,
                'apellido_materno': apellido_materno,
                'curp': curp,
                'fecha_ingreso': fecha_ingreso,
                'vulnerable': vulnerable,
                'ciclo': ciclo,
                'descripcion': descripcion
            }
            
            response = supabase.table('empleado').insert(data).execute()
            return response.data[0] if response.data else None
            
        except Exception as e:
            print(f"Error creando empleado: {e}")
            return None
    
    @staticmethod
    def actualizar(id_empleado, **kwargs):
        """Update employee data"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('empleado')\
                .update(kwargs)\
                .eq('id_empleado', id_empleado)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando empleado: {e}")
            return None
    
    @staticmethod
    def eliminar(id_empleado):
        """Delete an employee"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('empleado')\
                .delete()\
                .eq('id_empleado', id_empleado)\
                .execute()
            
            return True
        except Exception as e:
            print(f"Error eliminando empleado: {e}")
            return False
    
    @staticmethod
    def listar_vulnerables():
        """List vulnerable employees"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('empleado')\
                .select('*')\
                .eq('vulnerable', True)\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"Error listando empleados vulnerables: {e}")
            return []
    
    @staticmethod
    def listar_por_ciclo(ciclo):
        """List employees by cycle status"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('empleado')\
                .select('*')\
                .eq('ciclo', ciclo)\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"Error listando empleados por ciclo: {e}")
            return []
