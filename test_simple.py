"""
Prueba simple de login
"""
print("Probando autenticación...")

try:
    # Importar directamente sin pasar por database
    import os
    from dotenv import load_dotenv
    from supabase import create_client
    
    load_dotenv()
    
    # Usar anon key en lugar de service key
    url = os.getenv('SUPABASE_URL')
    anon_key = os.getenv('SUPABASE_KEY')
    
    print(f"URL: {url}")
    print(f"Key: {anon_key[:20]}...")
    
    client = create_client(url, anon_key)
    print("✓ Cliente creado")
    
    # Intentar listar productos
    response = client.table('producto').select('*').execute()
    print(f"✓ Productos: {len(response.data)}")
    
    for p in response.data:
        print(f"  - {p['nombre']}: ${p['costo_unitario']}")
    
    # Intentar listar usuarios
    response2 = client.table('usuario').select('*').execute()
    print(f"\n✓ Usuarios: {len(response2.data)}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
