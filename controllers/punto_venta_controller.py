class PuntoVentaController:
    """Controller de la sección Punto de Venta.

    Maneja el estado del carrito, descuentos y cálculo de totales.
    Conectado a Supabase para productos y ventas.
    """

    def __init__(self):
        from models.producto_model import ProductoModel
        from models.venta_model import VentaModel
        
        self.ProductoModel = ProductoModel
        self.VentaModel = VentaModel
        
        # Cargar productos desde Supabase
        self.productos = []
        self.cargar_productos()

        # Carrito: lista de dicts {id_producto, nombre, precio, cantidad, unidad_medida}
        self.carrito = []

        self.bolsa = False
        self.redondeo = False
    
    def cargar_productos(self):
        """Cargar productos desde Supabase"""
        try:
            productos_db = self.ProductoModel.listar_todos()
            self.productos = [
                {
                    'id_producto': p['id_producto'],
                    'nombre': p['nombre'],
                    'precio': float(p['costo_unitario']),
                    'stock': float(p['stock']),
                    'unidad_medida': p['unidad_medida']
                }
                for p in productos_db
            ]
        except Exception as e:
            print(f"Error cargando productos: {e}")
            # Fallback a productos por defecto
            self.productos = [
                {'id_producto': 1, 'nombre': 'Tortillas (kg)', 'precio': 25.0, 'stock': 100, 'unidad_medida': 'kg'},
                {'id_producto': 2, 'nombre': 'Tostadas (paquete)', 'precio': 15.0, 'stock': 50, 'unidad_medida': 'pz'},
                {'id_producto': 3, 'nombre': 'Chips (bolsa)', 'precio': 20.0, 'stock': 30, 'unidad_medida': 'pz'},
                {'id_producto': 4, 'nombre': 'Tamales', 'precio': 12.0, 'stock': 25, 'unidad_medida': 'pz'},
            ]

    # --- Operaciones sobre el carrito ---
    def agregar_al_carrito(self, nombre):
        producto = self._obtener_producto(nombre)
        if producto is None:
            return
        for item in self.carrito:
            if item["nombre"] == nombre:
                item["cantidad"] += 1
                break
        else:
            self.carrito.append({
                "id_producto": producto['id_producto'],
                "nombre": producto['nombre'],
                "precio": producto['precio'],
                "cantidad": 1,
                "unidad_medida": producto['unidad_medida']
            })

    def cambiar_cantidad(self, indice, delta):
        if indice < 0 or indice >= len(self.carrito):
            return
        item = self.carrito[indice]
        item["cantidad"] += delta
        if item["cantidad"] <= 0:
            self.carrito.pop(indice)

    def eliminar_item(self, indice):
        if 0 <= indice < len(self.carrito):
            self.carrito.pop(indice)

    def limpiar_carrito(self):
        self.carrito = []

    # --- Flags de descuento / redondeo ---
    def set_bolsa(self, valor: bool):
        self.bolsa = bool(valor)

    def set_redondeo(self, valor: bool):
        self.redondeo = bool(valor)

    # --- Cálculo de totales ---
    def calcular_totales(self):
        subtotal = sum(item["precio"] * item["cantidad"] for item in self.carrito)

        descuento = 2.0 if self.bolsa and subtotal >= 2.0 else 0.0
        subtotal_desc = max(subtotal - descuento, 0.0)

        if self.redondeo and subtotal_desc > 0:
            total_redondeado = float(int(subtotal_desc + 0.9999))
        else:
            total_redondeado = subtotal_desc

        return subtotal, total_redondeado

    def procesar_venta(self, id_cliente=1):
        """
        Procesar y guardar la venta en Supabase
        Args:
            id_cliente: ID del cliente (default: 1 para cliente general)
        Returns: ID de venta_completa o None
        """
        if not self.carrito:
            print("Carrito vacío, no se puede procesar venta")
            return None
        
        try:
            id_venta = self.VentaModel.procesar_venta(
                carrito=self.carrito,
                id_cliente=id_cliente,
                descuento_bolsa=self.bolsa,
                redondeo=self.redondeo
            )
            
            if id_venta:
                print(f"✓ Venta procesada exitosamente: ID {id_venta}")
                self.limpiar_carrito()
                return id_venta
            else:
                print("✗ Error procesando venta")
                return None
                
        except Exception as e:
            print(f"Error en procesar_venta: {e}")
            return None

    # --- Helpers internos ---
    def _obtener_producto(self, nombre):
        """Obtener producto completo por nombre"""
        for producto in self.productos:
            if producto['nombre'] == nombre:
                return producto
        return None
    
    def _obtener_precio(self, nombre):
        """Obtener precio de producto por nombre (legacy)"""
        producto = self._obtener_producto(nombre)
        return producto['precio'] if producto else None
