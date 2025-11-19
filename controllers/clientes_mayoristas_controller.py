class ClientesMayoristasController:
    """Controller de la sección Clientes Mayoristas.

    Mantiene la lista de clientes mayoristas (por ahora estática).
    """

    def __init__(self):
        self.clientes = [
            ("Restaurante El Buen Sabor", "555-0101", "15%", "✏"),
            ("Tienda La Esquina", "555-0102", "10%", "✏"),
            ("Comedor Comunitario Centro", "555-0103", "20%", "✏"),
            ("Super Abarrotes del Norte", "555-0104", "12%", "✏"),
        ]
