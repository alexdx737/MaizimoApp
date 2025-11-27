"""
Usuario Model - Authentication and user management
"""
from database import get_supabase_client
import bcrypt

class UsuarioModel:
    """Model for usuario table operations"""
    
    @staticmethod
    def validar_credenciales(usuario_id, password):
        """
        Validate user credentials
        Args:
            usuario_id: Username or employee ID
            password: Plain text password (max 50 characters)
        Returns:
            User data if valid, None otherwise
        """
        try:
            supabase = get_supabase_client()
            
            # Query usuario table joined with empleado
            response = supabase.table('usuario')\
                .select('*, empleado(*)')\
                .eq('id_usuario', usuario_id)\
                .eq('activo', True)\
                .execute()
            
            if not response.data or len(response.data) == 0:
                return None
            
            user = response.data[0]
            
            # Simple password comparison (plain text)
            if user['contraseña'] == password:
                return user
            
            return None
            
        except Exception as e:
            print(f"Error validando credenciales: {e}")
            return None
    
    @staticmethod
    def crear_usuario(id_empleado, password, rol='trabajador', activo=True):
        """
        Create a new user
        Args:
            id_empleado: Employee ID
            password: Plain text password (max 50 characters)
            rol: User role (administrador/trabajador)
            activo: Active status
        Returns:
            Created user data or None
        """
        try:
            supabase = get_supabase_client()
            
            # Password stored as plain text (max 50 chars)
            # For production, consider implementing password hashing
            if len(password) > 50:
                print("Error: Contraseña debe tener máximo 50 caracteres")
                return None
            
            data = {
                'id_empleado': id_empleado,
                'contraseña': password,
                'rol': rol,
                'activo': activo
            }
            
            response = supabase.table('usuario').insert(data).execute()
            return response.data[0] if response.data else None
            
        except Exception as e:
            print(f"Error creando usuario: {e}")
            return None
    
    @staticmethod
    def obtener_por_id(id_usuario):
        """Get user by ID"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('usuario')\
                .select('*, empleado(*)')\
                .eq('id_usuario', id_usuario)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error obteniendo usuario: {e}")
            return None
    
    @staticmethod
    def listar_todos():
        """List all users"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('usuario')\
                .select('*, empleado(*)')\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"Error listando usuarios: {e}")
            return []
    
    @staticmethod
    def actualizar(id_usuario, **kwargs):
        """Update user data"""
        try:
            supabase = get_supabase_client()
            response = supabase.table('usuario')\
                .update(kwargs)\
                .eq('id_usuario', id_usuario)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando usuario: {e}")
            return None
    
    @staticmethod
    def desactivar(id_usuario):
        """Deactivate a user"""
        return UsuarioModel.actualizar(id_usuario, activo=False)
