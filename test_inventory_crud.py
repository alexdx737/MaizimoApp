from controllers.gestion_operativa_controller import GestionOperativaController
import time

def test_crud():
    print("Iniciando prueba de CRUD de inventario...")
    controller = GestionOperativaController()
    
    # 1. Listar inicial
    print(f"Inventario inicial: {len(controller.inventario)} productos")
    
    # 2. Agregar
    print("Agregando producto de prueba...")
    nombre_prueba = f"Producto Test {int(time.time())}"
    if controller.agregar_producto(nombre_prueba, 100, "pz", 50.0, "Descripcion test"):
        print("✓ Producto agregado")
    else:
        print("✗ Error agregando producto")
        return

    # Verificar que se agregó
    encontrado = False
    indice_prueba = -1
    for i, fila in enumerate(controller.inventario):
        if fila[0] == nombre_prueba:
            encontrado = True
            indice_prueba = i
            print(f"✓ Producto encontrado en índice {i}")
            break
    
    if not encontrado:
        print("✗ Producto no encontrado en inventario")
        return

    # 3. Actualizar
    print("Actualizando producto...")
    nuevo_nombre = nombre_prueba + " EDITADO"
    if controller.actualizar_producto(indice_prueba, nuevo_nombre, 150, "pz", 55.0, "Descripcion editada"):
        print("✓ Producto actualizado")
    else:
        print("✗ Error actualizando producto")
        return

    # Verificar actualización
    controller.refrescar_inventario() # Recargar para asegurar
    encontrado_editado = False
    for fila in controller.inventario:
        if fila[0] == nuevo_nombre:
            encontrado_editado = True
            print("✓ Cambio de nombre verificado")
            if fila[1] == "150.00": # Stock formateado
                print("✓ Cambio de stock verificado")
            break
            
    if not encontrado_editado:
        print("✗ Producto editado no encontrado")

    # 4. Eliminar
    # Necesitamos buscar el índice de nuevo porque al refrescar pudo cambiar el orden o los IDs
    # Pero en este controlador simple, el mapa se reconstruye en orden.
    # Busquemos el índice del producto editado.
    indice_eliminar = -1
    for i, fila in enumerate(controller.inventario):
        if fila[0] == nuevo_nombre:
            indice_eliminar = i
            break
            
    print(f"Eliminando producto en índice {indice_eliminar}...")
    if controller.eliminar_producto(indice_eliminar):
        print("✓ Producto eliminado")
    else:
        print("✗ Error eliminando producto")
        return

    # Verificar eliminación
    controller.refrescar_inventario()
    encontrado_final = False
    for fila in controller.inventario:
        if fila[0] == nuevo_nombre:
            encontrado_final = True
            break
            
    if not encontrado_final:
        print("✓ Verificado que el producto ya no existe")
    else:
        print("✗ El producto sigue existiendo")

if __name__ == "__main__":
    try:
        test_crud()
        print("\nPrueba completada exitosamente.")
    except Exception as e:
        print(f"\nError durante la prueba: {e}")
