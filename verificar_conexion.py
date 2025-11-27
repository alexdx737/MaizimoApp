"""
Script simple para verificar conexión a Supabase
"""
from database import get_supabase_client

print("Probando conexión a Supabase...")
try:
    client = get_supabase_client()
    print("✓ Conexión exitosa!")
    
    # Probar consulta simple
    from models.producto_model import ProductoModel
    productos = ProductoModel.listar_todos()
    print(f"✓ {len(productos)} productos encontrados")
    
    print("\nProductos disponibles:")
    for p in productos:
        print(f"  - {p['nombre']}: ${p['costo_unitario']}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
