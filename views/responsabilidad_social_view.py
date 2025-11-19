import tkinter as tk


class ResponsabilidadSocialView(tk.Frame):
    def __init__(self, parent, app: "MainApp", controller):
        super().__init__(parent, bg=app.COLOR_FONDO_EXTERIOR)
        self.app = app
        self.controller = controller
        self._construir_ui()

    def _construir_ui(self):
        marco = tk.Frame(self, bg=self.app.COLOR_FONDO_INTERIOR, padx=20, pady=20)
        marco.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        descuento_frame = tk.Frame(marco, bg=self.app.COLOR_FONDO_INTERIOR)
        descuento_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(
            descuento_frame,
            text="Descuento por No Usar Bolsa",
            font=("Arial", 12, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w")

        tk.Label(
            descuento_frame,
            text="Incentivo ecológico para clientes que traen su propia bolsa",
            font=("Arial", 10),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(5, 10))

        tk.Label(
            descuento_frame,
            text=f"Descuento actual: ${self.controller.descuento_bolsa:.0f} pesos por no usar bolsa plástica",
            font=("Arial", 11),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg="#E3D6A8",
            padx=10,
            pady=8,
        ).pack(fill=tk.X)

        redondeo_frame = tk.Frame(marco, bg=self.app.COLOR_FONDO_INTERIOR)
        redondeo_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            redondeo_frame,
            text="Sistema de Redondeo Solidario",
            font=("Arial", 12, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w")

        tk.Label(
            redondeo_frame,
            text="Los clientes pueden redondear su compra para donar tortillas a la comunidad",
            font=("Arial", 10),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(5, 10))

        info_frame = tk.Frame(redondeo_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        info_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            info_frame,
            text=f"Fondo Acumulado\n${self.controller.fondo_acumulado:.2f}",
            font=("Arial", 11),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg="#F4C97A",
            padx=15,
            pady=10,
        ).pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)

        tk.Label(
            info_frame,
            text=f"Equivalente en Tortillas\n{self.controller.equivalente_tortillas_kg} kg",
            font=("Arial", 11),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg="#D2E5A1",
            padx=15,
            pady=10,
        ).pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)

        sim_frame = tk.Frame(redondeo_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        sim_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            sim_frame,
            text="Simular Redondeo de Venta",
            font=("Arial", 11, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(10, 5))

        tk.Label(
            sim_frame,
            text="Ejemplo: Con el fondo actual se pueden donar 33 kg de tortillas (132 tortillas aproximadamente)",
            font=("Arial", 10),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(5, 10))

        tk.Button(
            sim_frame,
            text="Aplicar Redondeo",
            font=("Arial", 10, "bold"),
            bg=self.app.COLOR_BOTON_FONDO,
            fg=self.app.COLOR_BOTON_TEXTO,
            relief=tk.FLAT,
            padx=15,
            pady=6,
        ).pack(anchor="e")
