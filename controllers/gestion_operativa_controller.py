class GestionOperativaController:
    """Controller de la sección Gestión Operativa.

    Maneja el inventario de productos (por ahora estático en memoria).
    """

    def __init__(self):
        self.inventario = [
            ("Tortillas de Maíz (kg)", 150, "kg", "$25", "$3750.00", "✏"),
            ("Tortillas Integrales (kg)", 80, "kg", "$30", "$2400.00", "✏"),
            ("Totopos (bolsa)", 45, "bolsa", "$15", "$675.00", "✏"),
            ("Masa para Tamales (kg)", 60, "kg", "$22", "$1320.00", "✏"),
        ]
