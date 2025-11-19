import tkinter as tk
from tkinter import ttk


class InclusionLaboralView(tk.Frame):
    def __init__(self, parent, app: "MainApp", controller):
        super().__init__(parent, bg=app.COLOR_FONDO_EXTERIOR)
        self.app = app
        self.controller = controller
        self._construir_ui()

    def _construir_ui(self):
        marco = tk.Frame(self, bg=self.app.COLOR_FONDO_INTERIOR, padx=20, pady=20)
        marco.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        resumen_frame = tk.Frame(marco, bg=self.app.COLOR_FONDO_INTERIOR)
        resumen_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(
            resumen_frame,
            text="Programa de Inclusión Laboral",
            font=("Arial", 12, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(0, 10))

        tabla_frame = tk.Frame(marco, bg=self.app.COLOR_FONDO_INTERIOR)
        tabla_frame.pack(fill=tk.BOTH, expand=True)

        boton_frame = tk.Frame(tabla_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        boton_frame.pack(anchor="e", fill=tk.X, pady=(0, 10))

        tk.Button(
            boton_frame,
            text="+  Agregar Trabajador",
            font=("Arial", 10, "bold"),
            bg=self.app.COLOR_BOTON_FONDO,
            fg=self.app.COLOR_BOTON_TEXTO,
            relief=tk.FLAT,
            padx=15,
            pady=5,
        ).pack(side=tk.RIGHT)

        columnas = ("nombre", "situacion", "ciclo", "fecha", "acciones")
        tree = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=6)
        titulos = [
            "Nombre",
            "Situación de Vulnerabilidad",
            "Ciclo de Trabajo",
            "Fecha de Inicio",
            "Acciones",
        ]
        for col, texto in zip(columnas, titulos):
            tree.heading(col, text=texto)
            tree.column(col, anchor="center", width=170)

        tree.pack(fill=tk.BOTH, expand=True)

        for fila in self.controller.trabajadores:
            tree.insert("", tk.END, values=fila)
