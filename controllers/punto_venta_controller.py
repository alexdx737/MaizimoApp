class PuntoVentaController:
    """Controller de la sección Punto de Venta.

    Maneja el estado del carrito, descuentos y cálculo de totales.
    Conectado a Supabase para productos y ventas.
    """

    def __init__(self):
        from models.producto_model import ProductoModel
        from models.venta_model import VentaModel
        from models.cliente_model import ClienteModel
        
        self.ProductoModel = ProductoModel
        self.VentaModel = VentaModel
        self.ClienteModel = ClienteModel
        
        # Cargar productos desde Supabase
        self.productos = []
        self.productos_filtrados = []  # Para búsqueda
        self.cargar_productos()

        # Cargar clientes para selección
        self.clientes = []
        self.cargar_clientes()
        
        # Cliente seleccionado (default: cliente general ID 1)
        self.id_cliente_seleccionado = 1
        self.descuento_cliente = 0.0  # Porcentaje de descuento

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
        
        # Inicializar productos filtrados con todos los productos
        self.productos_filtrados = self.productos[:]
    
    def cargar_clientes(self):
        """Cargar clientes desde Supabase"""
        try:
            clientes_db = self.ClienteModel.listar_todos()
            self.clientes = [
                {
                    'id': c['id_cliente'],
                    'nombre': f"{c['nombre']} {c['apellido_paterno']}",
                    'descuento': float(c['descuento'])
                }
                for c in clientes_db
            ]
            print(f"✓ Cargados {len(self.clientes)} clientes")
        except Exception as e:
            print(f"Error cargando clientes: {e}")
            self.clientes = [{'id': 1, 'nombre': 'Cliente General', 'descuento': 0.0}]
    
    def set_cliente(self, id_cliente):
        """Establecer cliente seleccionado y su descuento"""
        self.id_cliente_seleccionado = id_cliente
        
        # Buscar descuento del cliente
        for cliente in self.clientes:
            if cliente['id'] == id_cliente:
                self.descuento_cliente = cliente['descuento']
                print(f"✓ Cliente seleccionado: {cliente['nombre']}, Descuento: {self.descuento_cliente}%")
                return
        
        # Si no se encuentra, usar cliente general
        self.descuento_cliente = 0.0
    
    def filtrar_productos(self, termino):
        """Filtrar productos por nombre o ID"""
        if not termino or termino.strip() == "":
            # Si no hay término, mostrar todos
            self.productos_filtrados = self.productos[:]
        else:
            termino = termino.lower().strip()
            self.productos_filtrados = []
            
            for p in self.productos:
                # Buscar por nombre
                if termino in p['nombre'].lower():
                    self.productos_filtrados.append(p)
                # Buscar por ID (convertir a string)
                elif termino in str(p['id_producto']):
                    self.productos_filtrados.append(p)
        
        print(f"✓ Filtrados {len(self.productos_filtrados)} productos")

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

        # Descuento por bolsa
        descuento_bolsa = 2.0 if self.bolsa and subtotal >= 2.0 else 0.0
        
        # Descuento de cliente mayorista (porcentaje)
        descuento_cliente_monto = (subtotal * self.descuento_cliente) / 100.0
        
        # Total de descuentos
        descuento_total = descuento_bolsa + descuento_cliente_monto
        
        total = max(subtotal - descuento_total, 0.0)

        return subtotal, total, descuento_cliente_monto

    def procesar_venta(self, monto_pago=0):
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
                id_cliente=self.id_cliente_seleccionado,
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
