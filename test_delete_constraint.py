from controllers.gestion_operativa_controller import GestionOperativaController
from models.producto_model import ProductoModel
import time

def test_delete_constraint():
    print("Iniciando prueba de restricción de eliminación...")
    controller = GestionOperativaController()
    
    # 1. Buscar un producto que sabemos que tiene ventas (ej. Chips o Tortillas)
    # O crear uno nuevo, crearle una venta (si pudiéramos) y tratar de borrarlo.
    # Como no podemos crear ventas fácilmente sin toda la estructura, intentemos con uno existente.
    # El usuario mencionó "Chips".
    
    nombre_target = "Chips"
    indice_target = -1
    
    print(f"Buscando '{nombre_target}'...")
    for i, fila in enumerate(controller.inventario):
        if nombre_target in fila[0]:
            indice_target = i
            print(f"✓ Encontrado en índice {i}")
            break
            
    if indice_target == -1:
        print(f"⚠ No se encontró '{nombre_target}'. Intentando con el primer producto...")
        if len(controller.inventario) > 0:
            indice_target = 0
            print(f"Seleccionado: {controller.inventario[0][0]}")
        else:
            print("✗ Inventario vacío. No se puede probar.")
            return

    # 2. Intentar eliminar
    print("Intentando eliminar producto con ventas...")
    success, message = controller.eliminar_producto(indice_target)
    
    print(f"Resultado: Success={success}, Message='{message}'")
    
    if not success:
        if "ventas asociadas" in message:
            print("✓ PRUEBA EXITOSA: El sistema detectó la restricción y devolvió el mensaje correcto.")
        else:
            print(f"⚠ PRUEBA PARCIAL: Falló la eliminación pero con mensaje diferente: {message}")
    else:
        print("✗ PRUEBA FALLIDA: El sistema permitió eliminar el producto (o reportó éxito falsamente).")

if __name__ == "__main__":
    try:
        test_delete_constraint()
    except Exception as e:
        print(f"\nError durante la prueba: {e}")
