"""
Database connection module for Maizimo App
Uses Supabase (PostgreSQL) for data persistence
"""
from supabase import create_client, Client
from .config import Config
import psycopg2
from psycopg2 import pool, Error

# Global Supabase client
_supabase_client: Client = None
_pg_pool = None

def get_supabase_client() -> Client:
    """
    Get or create Supabase client instance
    Uses service role key for backend operations (bypasses RLS)
    Returns: Supabase client for API operations
    """
    global _supabase_client
    
    if _supabase_client is None:
        try:
            # Use service role key for backend operations
            # This bypasses RLS policies - appropriate for backend/server-side code
            _supabase_client = create_client(
                Config.SUPABASE_URL,
                Config.SUPABASE_BACKEND_KEY
            )
            print("✓ Conexión con Supabase establecida (service role)")
        except Exception as e:
            print(f"✗ Error al conectar a Supabase: {e}")
            raise
    
    return _supabase_client

def crear_conexion():
    """
    Create direct PostgreSQL connection (legacy compatibility)
    Returns: psycopg2 connection object
    """
    try:
        conexion = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        print("✓ Conexión directa con PostgreSQL establecida")
        return conexion
    except Error as e:
        print(f"✗ Error al conectar a PostgreSQL: {e}")
        return None

def get_connection_pool():
    """
    Get or create PostgreSQL connection pool
    Returns: Connection pool for efficient database operations
    """
    global _pg_pool
    
    if _pg_pool is None:
        try:
            _pg_pool = psycopg2.pool.SimpleConnectionPool(
                1, 10,  # min and max connections
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD
            )
            print("✓ Pool de conexiones PostgreSQL creado")
        except Error as e:
            print(f"✗ Error al crear pool de conexiones: {e}")
            raise
    
    return _pg_pool

def get_connection_from_pool():
    """Get a connection from the pool"""
    pool = get_connection_pool()
    return pool.getconn()

def return_connection_to_pool(conn):
    """Return a connection to the pool"""
    pool = get_connection_pool()
    pool.putconn(conn)

def close_all_connections():
    """Close all connections in the pool"""
    global _pg_pool
    if _pg_pool:
        _pg_pool.closeall()
        print("✓ Todas las conexiones cerradas")

# Probar la conexión en este archivo
if __name__ == "__main__":
    print("Probando conexión a Supabase...")
    try:
        client = get_supabase_client()
        print(f"Cliente Supabase: {client}")
        
        # Test direct connection
        print("\nProbando conexión directa a PostgreSQL...")
        conn = crear_conexion()
        if conn:
            print("Conexión exitosa!")
            conn.close()
    except Exception as e:
        print(f"Error en prueba: {e}")
