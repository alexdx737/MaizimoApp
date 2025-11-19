class InclusionLaboralController:
    """Controller de la sección Inclusión Laboral.

    Mantiene el listado de trabajadores en el programa.
    """

    def __init__(self):
        self.trabajadores = [
            ("María González", "Madre soltera", "En Espera", "2024-09-01", "✏"),
            ("Juan Pérez", "Persona con discapacidad", "En Curso", "2024-08-15", "✏"),
            ("Ana Martínez", "Adulto mayor", "Finalizando", "2024-03-10", "✏"),
            ("Carlos Ramírez", "Joven en riesgo", "En Espera", "2024-11-01", "✏"),
        ]
