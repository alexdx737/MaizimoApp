import tkinter as tk
from tkinter import ttk


class ClientesMayoristasView(tk.Frame):
    def __init__(self, parent, app: "MainApp", controller):
        super().__init__(parent, bg=app.COLOR_FONDO_EXTERIOR)
        self.app = app
        self.controller = controller
        self._construir_ui()

    def _construir_ui(self):
        marco = tk.Frame(self, bg=self.app.COLOR_FONDO_INTERIOR, padx=20, pady=20)
        marco.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        tk.Label(
            marco,
            text="Clientes Mayoristas",
            font=("Arial", 12, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(0, 10))

        boton_frame = tk.Frame(marco, bg=self.app.COLOR_FONDO_INTERIOR)
        boton_frame.pack(anchor="e", fill=tk.X, pady=(0, 10))

        tk.Button(
            boton_frame,
            text="+  Agregar Cliente",
            font=("Arial", 10, "bold"),
            bg=self.app.COLOR_BOTON_FONDO,
            fg=self.app.COLOR_BOTON_TEXTO,
            relief=tk.FLAT,
            padx=15,
            pady=5,
        ).pack(side=tk.RIGHT)

        columnas = ("cliente", "contacto", "descuento", "acciones")
        tree = ttk.Treeview(marco, columns=columnas, show="headings", height=6)
        titulos = ["Cliente", "Contacto", "Descuento Aplicado", "Acciones"]
        for col, texto in zip(columnas, titulos):
            tree.heading(col, text=texto)
            tree.column(col, anchor="center", width=180)

        tree.pack(fill=tk.BOTH, expand=True)

        for fila in self.controller.clientes:
            tree.insert("", tk.END, values=fila)
