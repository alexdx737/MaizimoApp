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
        total = max(subtotal - descuento, 0.0)

        return subtotal, total

    def procesar_venta(self, id_cliente=1, monto_pago=0):
        """
        Procesar y guardar la venta en Supabase
        Args:
            id_cliente: ID del cliente (default: 1 para cliente general)
            monto_pago: Monto con el que paga el cliente
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
                redondeo=self.redondeo,
                monto_pago=monto_pago
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

    # --- auxiliares internos ---
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

    def obtener_historial_ventas(self):
        """Obtener historial completo de ventas formateado para la vista"""
        ventas = self.VentaModel.listar_ventas(limit=50) # Limit 50 for now, maybe more? User said "historial de ventas", not just today.
        
        datos_formateados = []
        for v in ventas:
            # Formatear fecha y hora
            fecha = v.get('fecha', '')
            hora = v.get('hora', '')[:5] if v.get('hora') else ''
            
            # Formatear total
            total = float(v.get('monto_total', 0))
            
            # Verificar donación
            donaciones = v.get('donacion', [])
            # Supabase might return None, [], or object. Handle list.
            if isinstance(donaciones, list) and len(donaciones) > 0:
                redondeo = "Sí"
                monto_donacion = float(donaciones[0].get('monto_redondeo', 0))
            elif isinstance(donaciones, dict): # Should not happen with 1:N but just in case
                redondeo = "Sí"
                monto_donacion = float(donaciones.get('monto_redondeo', 0))
            else:
                redondeo = "No"
                monto_donacion = 0.0
                
            datos_formateados.append((
                v['id_venta_completa'],
                fecha,
                hora,
                f"${total:.2f}",
                redondeo,
                f"${monto_donacion:.2f}"
            ))
            
        return datos_formateados

    def obtener_detalle_venta(self, id_venta):
        """Obtener detalle completo de una venta"""
        return self.VentaModel.obtener_venta_completa(id_venta)
