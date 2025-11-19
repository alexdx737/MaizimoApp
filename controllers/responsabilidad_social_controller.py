class ResponsabilidadSocialController:
    """Controller de la sección Responsabilidad Social.

    Mantiene la configuración de descuentos y redondeo solidario.
    """

    def __init__(self):
        self.descuento_bolsa = 2.0  # pesos
        self.fondo_acumulado = 847.50
        self.equivalente_tortillas_kg = 33
