"""
Configuration module for Maizimo App
Loads environment variables and provides configuration settings
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')  # Anon/Public key
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')  # Service role key
    
    # Use service role key for backend operations (bypasses RLS)
    # For production, you should implement proper RLS policies
    SUPABASE_BACKEND_KEY = os.getenv('SUPABASE_SERVICE_KEY', os.getenv('SUPABASE_KEY'))
    
    # Database Configuration (for direct PostgreSQL connection)
    DB_HOST = os.getenv('DB_HOST', 'db.iggylhudyphmzflrjgta.supabase.co')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'postgres')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        if not cls.SUPABASE_URL:
            raise ValueError("SUPABASE_URL no está configurada en .env")
        if not cls.SUPABASE_BACKEND_KEY:
            raise ValueError("SUPABASE_KEY o SUPABASE_SERVICE_KEY deben estar configuradas en .env")
        return True

# Validate configuration on import
try:
    Config.validate()
    print("✓ Configuración cargada correctamente")
except ValueError as e:
    print(f"⚠ Error en configuración: {e}")
    print("Por favor verifica tu archivo .env")
