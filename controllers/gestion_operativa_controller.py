from models.producto_model import ProductoModel

class GestionOperativaController:
    """Controller de la sección Gestión Operativa.

    Maneja el inventario de productos desde la base de datos.
    """

    def __init__(self):
        self.inventario = []
        # Diccionario para mapear índice de fila a ID de producto
        self.mapa_ids = {} 
        self.cargar_inventario()
    
    def cargar_inventario(self):
        """Carga el inventario desde la base de datos"""
        try:
            productos = ProductoModel.listar_todos()
            self.inventario = []
            self.mapa_ids = {}
            
            for index, producto in enumerate(productos):
                # Guardar ID para referencia futura
                self.mapa_ids[index] = producto['id_producto']
                
                # Formatear datos para la vista
                nombre = producto['nombre']
                stock = float(producto['stock'])
                unidad = producto['unidad_medida']
                costo_unitario = float(producto['costo_unitario'])
                valor_total = stock * costo_unitario
                
                # Formato: (nombre, stock, unidad, precio_unitario, valor_total, acciones)
                fila = (
                    nombre,
                    f"{stock:.2f}",
                    unidad,
                    f"${costo_unitario:.2f}",
                    f"${valor_total:.2f}",
                    "✏ / 🗑" # Indicador visual de acciones
                )
                self.inventario.append(fila)
        except Exception as e:
            print(f"Error cargando inventario: {e}")
            self.inventario = []
            self.mapa_ids = {}
    
    def refrescar_inventario(self):
        """Refresca el inventario desde la base de datos"""
        self.cargar_inventario()

    def obtener_producto_por_indice(self, index):
        """Obtiene los datos completos del producto dado el índice de la fila"""
        if index in self.mapa_ids:
            id_producto = self.mapa_ids[index]
            return ProductoModel.obtener_por_id(id_producto)
        return None

    def agregar_producto(self, nombre, stock, unidad, costo, descripcion):
        """Agrega un nuevo producto"""
        try:
            ProductoModel.crear(nombre, stock, unidad, costo, descripcion)
            self.refrescar_inventario()
            return True
        except Exception as e:
            print(f"Error agregando producto: {e}")
            return False

    def actualizar_producto(self, index, nombre, stock, unidad, costo, descripcion):
        """Actualiza un producto existente"""
        if index in self.mapa_ids:
            id_producto = self.mapa_ids[index]
            try:
                ProductoModel.actualizar(
                    id_producto, 
                    nombre=nombre, 
                    stock=stock, 
                    unidad_medida=unidad, 
                    costo_unitario=costo, 
                    descripcion=descripcion
                )
                self.refrescar_inventario()
                return True
            except Exception as e:
                print(f"Error actualizando producto: {e}")
                return False
        return False

    def eliminar_producto(self, index):
        """Elimina un producto"""
        if index in self.mapa_ids:
            id_producto = self.mapa_ids[index]
            try:
                ProductoModel.eliminar(id_producto)
                self.refrescar_inventario()
                return True, "Producto eliminado correctamente"
            except Exception as e:
                print(f"Error eliminando producto: {e}")
                # Intentar extraer mensaje más amigable
                msg = str(e)
                if "foreign key" in msg.lower() or "violates foreign key constraint" in msg.lower():
                    return False, "No se puede eliminar el producto porque tiene ventas asociadas."
                return False, f"Error al eliminar: {msg}"
        return False, "Producto no encontrado"
