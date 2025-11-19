import tkinter as tk
from tkinter import ttk


class PuntoVentaView(tk.Frame):
    def __init__(self, parent, app: "MainApp", controller):
        super().__init__(parent, bg=app.COLOR_FONDO_EXTERIOR)
        self.app = app
        self.controller = controller

        self._construir_ui()

    def _construir_ui(self):
        top_info = tk.Frame(self, bg=self.app.COLOR_FONDO_EXTERIOR)
        top_info.pack(fill=tk.X)

        fondo_frame = tk.Frame(top_info, bg=self.app.COLOR_FONDO_INTERIOR, padx=15, pady=10)
        fondo_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=5)

        tk.Label(
            fondo_frame,
            text="Fondo de Redondeo",
            font=("Arial", 10, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w")
        tk.Label(
            fondo_frame,
            text="$1.25 MXN",
            font=("Arial", 12),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(5, 0))

        eq_frame = tk.Frame(top_info, bg=self.app.COLOR_FONDO_INTERIOR, padx=15, pady=10)
        eq_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0), pady=5)

        tk.Label(
            eq_frame,
            text="Equivalente en Tortillas",
            font=("Arial", 10, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w")
        tk.Label(
            eq_frame,
            text="0 kg",
            font=("Arial", 12),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(5, 0))

        mid_frame = tk.Frame(self, bg=self.app.COLOR_FONDO_EXTERIOR)
        mid_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        productos_frame = tk.Frame(mid_frame, bg=self.app.COLOR_FONDO_INTERIOR, padx=15, pady=15)
        productos_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(
            productos_frame,
            text="Productos",
            font=("Arial", 12, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w")

        # Productos provenientes del controller
        for nombre, precio in self.controller.productos:
            item_frame = tk.Frame(productos_frame, bg=self.app.COLOR_FONDO_INTERIOR)
            item_frame.pack(fill=tk.X, pady=5)

            tk.Label(
                item_frame,
                text=nombre,
                font=("Arial", 11),
                fg=self.app.COLOR_TEXTO_PRIMARIO,
                bg=self.app.COLOR_FONDO_INTERIOR,
            ).pack(side=tk.LEFT, anchor="w")

            tk.Label(
                item_frame,
                text=f"$ {precio:.2f}",
                font=("Arial", 10),
                fg=self.app.COLOR_TEXTO_PRIMARIO,
                bg=self.app.COLOR_FONDO_INTERIOR,
            ).pack(side=tk.LEFT, padx=10)

            tk.Button(
                item_frame,
                text="+",
                font=("Arial", 12, "bold"),
                bg=self.app.COLOR_BOTON_FONDO,
                fg=self.app.COLOR_BOTON_TEXTO,
                width=3,
                relief=tk.FLAT,
                command=lambda n=nombre, p=precio: self.agregar_al_carrito(n, p),
            ).pack(side=tk.RIGHT)

        carrito_frame = tk.Frame(mid_frame, bg=self.app.COLOR_FONDO_INTERIOR, padx=15, pady=15)
        carrito_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        tk.Label(
            carrito_frame,
            text="Carrito de Venta",
            font=("Arial", 12, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w")

        self.carrito_items_frame = tk.Frame(carrito_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        self.carrito_items_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 5))

        self.subtotal_label = tk.Label(
            carrito_frame,
            text="Subtotal: $0.00",
            font=("Arial", 11),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        )
        self.subtotal_label.pack(anchor="e", pady=(5, 0))

        self.bolsa_var = tk.BooleanVar(value=self.controller.bolsa)
        bolsa_frame = tk.Frame(carrito_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        bolsa_frame.pack(fill=tk.X, pady=(5, 0))

        tk.Checkbutton(
            bolsa_frame,
            text="¿Trae su propia bolsa? (Descuento de $2)",
            variable=self.bolsa_var,
            onvalue=True,
            offvalue=False,
            command=self._recalcular_totales,
            bg=self.app.COLOR_FONDO_INTERIOR,
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            anchor="w",
        ).pack(anchor="w")

        self.redondeo_var = tk.BooleanVar(value=self.controller.redondeo)
        redondeo_frame = tk.Frame(carrito_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        redondeo_frame.pack(fill=tk.X, pady=(5, 0))

        tk.Checkbutton(
            redondeo_frame,
            text="Redondear para donación de tortillas",
            variable=self.redondeo_var,
            onvalue=True,
            offvalue=False,
            command=self._recalcular_totales,
            bg=self.app.COLOR_FONDO_INTERIOR,
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            anchor="w",
        ).pack(anchor="w")

        self.total_label = tk.Label(
            carrito_frame,
            text="Total a Pagar: $0.00",
            font=("Arial", 11, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        )
        self.total_label.pack(anchor="e", pady=(8, 4))

        tk.Button(
            carrito_frame,
            text="Completar Venta",
            font=("Arial", 12, "bold"),
            bg=self.app.COLOR_BOTON_FONDO,
            fg=self.app.COLOR_BOTON_TEXTO,
            relief=tk.FLAT,
            padx=10,
            pady=6,
            command=self._completar_venta,
        ).pack(fill=tk.X, pady=(0, 0))

        self._render_carrito()

        bottom_frame = tk.Frame(self, bg=self.app.COLOR_FONDO_EXTERIOR)
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        historial_frame = tk.Frame(bottom_frame, bg=self.app.COLOR_FONDO_INTERIOR, padx=15, pady=15)
        historial_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            historial_frame,
            text="Historial de Ventas del Día",
            font=("Arial", 12, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(0, 10))

        columnas = ("fecha", "hora", "total", "redondeo", "donacion")
        tree = ttk.Treeview(historial_frame, columns=columnas, show="headings", height=4)
        for col, texto in zip(columnas, ["Fecha", "Hora", "Total", "Redondeo", "Donación"]):
            tree.heading(col, text=texto)
            tree.column(col, width=100, anchor="center")

        tree.pack(fill=tk.BOTH, expand=True)

        datos_demo = [
            ("2024-11-04", "09:15", "$75.00", "Sí", "$0.50"),
            ("2024-11-04", "10:30", "$128.00", "Sí", "$0.75"),
            ("2024-11-04", "11:45", "$50.00", "No", "$0.00"),
        ]
        for fila in datos_demo:
            tree.insert("", tk.END, values=fila)

    # --- Lógica de carrito ---
    def agregar_al_carrito(self, nombre, precio):
        self.controller.agregar_al_carrito(nombre)
        self._render_carrito()

    def _cambiar_cantidad(self, indice, delta):
        self.controller.cambiar_cantidad(indice, delta)
        self._render_carrito()

    def _eliminar_item(self, indice):
        self.controller.eliminar_item(indice)
        self._render_carrito()

    def _render_carrito(self):
        for w in self.carrito_items_frame.winfo_children():
            w.destroy()

        carrito = self.controller.carrito

        if not carrito:
            tk.Label(
                self.carrito_items_frame,
                text="No hay productos en el carrito",
                font=("Arial", 10),
                fg=self.app.COLOR_TEXTO_PRIMARIO,
                bg=self.app.COLOR_FONDO_INTERIOR,
            ).pack(anchor="w", pady=5)
        else:
            for idx, item in enumerate(carrito):
                fila = tk.Frame(self.carrito_items_frame, bg=self.app.COLOR_FONDO_INTERIOR)
                fila.pack(fill=tk.X, pady=3)

                texto = f"{item['nombre']}\n$ {item['precio']:.2f} x {item['cantidad']} = $ {item['precio']*item['cantidad']:.2f}"
                tk.Label(
                    fila,
                    text=texto,
                    font=("Arial", 10),
                    fg=self.app.COLOR_TEXTO_PRIMARIO,
                    bg=self.app.COLOR_FONDO_INTERIOR,
                    justify="left",
                ).pack(side=tk.LEFT, anchor="w")

                controles = tk.Frame(fila, bg=self.app.COLOR_FONDO_INTERIOR)
                controles.pack(side=tk.RIGHT)

                tk.Button(
                    controles,
                    text="-",
                    font=("Arial", 10, "bold"),
                    bg=self.app.COLOR_FONDO_INTERIOR,
                    fg=self.app.COLOR_TEXTO_PRIMARIO,
                    width=2,
                    relief=tk.FLAT,
                    command=lambda i=idx: self._cambiar_cantidad(i, -1),
                ).pack(side=tk.LEFT, padx=2)

                tk.Label(
                    controles,
                    text=str(item["cantidad"]),
                    font=("Arial", 10),
                    fg=self.app.COLOR_TEXTO_PRIMARIO,
                    bg=self.app.COLOR_FONDO_INTERIOR,
                    width=3,
                ).pack(side=tk.LEFT, padx=2)

                tk.Button(
                    controles,
                    text="+",
                    font=("Arial", 10, "bold"),
                    bg=self.app.COLOR_BOTON_FONDO,
                    fg=self.app.COLOR_BOTON_TEXTO,
                    width=2,
                    relief=tk.FLAT,
                    command=lambda i=idx: self._cambiar_cantidad(i, 1),
                ).pack(side=tk.LEFT, padx=2)

                tk.Button(
                    controles,
                    text="🗑",
                    font=("Arial", 10),
                    bg=self.app.COLOR_FONDO_INTERIOR,
                    fg=self.app.COLOR_TEXTO_PRIMARIO,
                    width=2,
                    relief=tk.FLAT,
                    command=lambda i=idx: self._eliminar_item(i),
                ).pack(side=tk.LEFT, padx=4)

        self._recalcular_totales()

    def _recalcular_totales(self):
        # Actualizar flags en el controller según los checkboxes
        self.controller.set_bolsa(self.bolsa_var.get())
        self.controller.set_redondeo(self.redondeo_var.get())

        subtotal, total = self.controller.calcular_totales()

        self.subtotal_label.config(text=f"Subtotal: $ {subtotal:.2f}")
        self.total_label.config(text=f"Total a Pagar: $ {total:.2f}")

    def _completar_venta(self):
        self.controller.limpiar_carrito()
        self._render_carrito()
