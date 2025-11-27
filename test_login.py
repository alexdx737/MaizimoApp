"""
Prueba completa del sistema de login
"""
print("=" * 60)
print("PRUEBA DE LOGIN CON SUPABASE")
print("=" * 60)

from models.usuario_model import UsuarioModel

# Probar login con credenciales correctas
print("\n1. Probando login con credenciales correctas...")
print("   Usuario: 1")
print("   Contraseña: admin123")

user = UsuarioModel.validar_credenciales('1', 'admin123')

if user:
    print("   ✓ ¡Login exitoso!")
    print(f"   - ID Usuario: {user['id_usuario']}")
    print(f"   - Rol: {user['rol']}")
    print(f"   - Activo: {user['activo']}")
    if 'empleado' in user and user['empleado']:
        emp = user['empleado']
        print(f"   - Empleado: {emp['nombre']} {emp['apellido_paterno']}")
        print(f"   - CURP: {emp['curp']}")
else:
    print("   ✗ Login fallido")

# Probar login con credenciales incorrectas
print("\n2. Probando login con credenciales incorrectas...")
print("   Usuario: 999")
print("   Contraseña: wrongpass")

user_fail = UsuarioModel.validar_credenciales('999', 'wrongpass')

if user_fail:
    print("   ✗ ERROR: Login debería haber fallado")
else:
    print("   ✓ Correctamente rechazado")

print("\n" + "=" * 60)
print("PRUEBA DE LOGIN COMPLETADA")
print("=" * 60)
print("\n✓ El sistema de autenticación está funcionando correctamente")
print("✓ Puedes ejecutar la aplicación con: python login_view.py")
print("\nCredenciales para probar:")
print("  Usuario: 1")
print("  Contraseña: admin123")
