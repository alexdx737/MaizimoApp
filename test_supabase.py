"""
Script de prueba para verificar la conexión con Supabase
"""
print("=" * 60)
print("PRUEBA DE CONEXIÓN A SUPABASE")
print("=" * 60)

# Test 1: Conexión básica
print("\n1. Probando conexión básica...")
try:
    from database import get_supabase_client
    client = get_supabase_client()
    print("   ✓ Cliente Supabase conectado exitosamente")
except Exception as e:
    print(f"   ✗ Error: {e}")
    exit(1)

# Test 2: Listar productos
print("\n2. Probando modelo de productos...")
try:
    from models.producto_model import ProductoModel
    productos = ProductoModel.listar_todos()
    print(f"   ✓ Productos encontrados: {len(productos)}")
    for p in productos:
        print(f"     - {p['nombre']}: ${p['costo_unitario']} ({p['stock']} {p['unidad_medida']})")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Autenticación
print("\n3. Probando autenticación...")
try:
    from models.usuario_model import UsuarioModel
    user = UsuarioModel.validar_credenciales('1', 'admin123')
    if user:
        print(f"   ✓ Usuario autenticado exitosamente")
        print(f"     - Rol: {user['rol']}")
        print(f"     - Activo: {user['activo']}")
        if 'empleado' in user:
            print(f"     - Empleado: {user['empleado']['nombre']} {user['empleado']['apellido_paterno']}")
    else:
        print("   ✗ Error: Credenciales inválidas")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Listar clientes
print("\n4. Probando modelo de clientes...")
try:
    from models.cliente_model import ClienteModel
    clientes = ClienteModel.listar_todos()
    print(f"   ✓ Clientes encontrados: {len(clientes)}")
    for c in clientes:
        print(f"     - {c['nombre']} {c['apellido_paterno']} - Tel: {c['telefono']}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 5: Listar empleados
print("\n5. Probando modelo de empleados...")
try:
    from models.empleado_model import EmpleadoModel
    empleados = EmpleadoModel.listar_todos()
    print(f"   ✓ Empleados encontrados: {len(empleados)}")
    for e in empleados:
        print(f"     - {e['nombre']} {e['apellido_paterno']} - CURP: {e['curp']}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 6: Punto de venta
print("\n6. Probando controlador de punto de venta...")
try:
    from controllers.punto_venta_controller import PuntoVentaController
    pv = PuntoVentaController()
    print(f"   ✓ Controlador inicializado")
    print(f"   ✓ Productos cargados: {len(pv.productos)}")
    
    # Simular agregar al carrito
    if len(pv.productos) > 0:
        primer_producto = pv.productos[0]['nombre']
        pv.agregar_al_carrito(primer_producto)
        print(f"   ✓ Producto agregado al carrito: {primer_producto}")
        print(f"   ✓ Items en carrito: {len(pv.carrito)}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("PRUEBAS COMPLETADAS")
print("=" * 60)
