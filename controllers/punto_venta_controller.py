class PuntoVentaController:
    """Controller de la sección Punto de Venta.

    Maneja el estado del carrito, descuentos y cálculo de totales.
    Por ahora trabaja solo en memoria; más adelante puede conectarse a modelos/BD.
    """

    def __init__(self):
        # Lista de productos disponibles (nombre, precio)
        self.productos = [
            ("Tortillas (kg)", 25.0),
            ("Tostadas (paquete)", 15.0),
            ("Chips (bolsa)", 20.0),
            ("Tamales", 12.0),
        ]

        # Carrito: lista de dicts {nombre, precio, cantidad}
        self.carrito = []

        self.bolsa = False
        self.redondeo = False

    # --- Operaciones sobre el carrito ---
    def agregar_al_carrito(self, nombre):
        precio = self._obtener_precio(nombre)
        if precio is None:
            return
        for item in self.carrito:
            if item["nombre"] == nombre:
                item["cantidad"] += 1
                break
        else:
            self.carrito.append({"nombre": nombre, "precio": precio, "cantidad": 1})

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

    # --- Helpers internos ---
    def _obtener_precio(self, nombre):
        for n, p in self.productos:
            if n == nombre:
                return p
        return None
