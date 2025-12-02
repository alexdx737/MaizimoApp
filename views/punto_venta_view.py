import tkinter as tk
from tkinter import ttk


class PuntoVentaView(tk.Frame):
    def __init__(self, parent, app: "MainApp", controller):
        super().__init__(parent, bg=app.COLOR_FONDO_EXTERIOR)
        self.app = app
        self.controller = controller

        # Recargar datos al abrir la vista para asegurar que esté actualizada
        self.controller.cargar_clientes()
        self.controller.cargar_productos()

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

        # Buscador de productos
        buscar_frame = tk.Frame(productos_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        buscar_frame.pack(fill=tk.X, pady=(5, 10))

        tk.Label(
            buscar_frame,
            text="🔍",
            font=("Arial", 12),
            bg=self.app.COLOR_FONDO_INTERIOR,
            fg=self.app.COLOR_TEXTO_PRIMARIO,
        ).pack(side=tk.LEFT)

        self.buscar_var = tk.StringVar()
        self.buscar_var.trace('w', lambda *args: self._filtrar_productos())
        tk.Entry(
            buscar_frame,
            textvariable=self.buscar_var,
            font=("Arial", 10),
            width=20
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Canvas y scrollbar para lista de productos
        canvas_frame = tk.Frame(productos_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.productos_canvas = tk.Canvas(canvas_frame, bg=self.app.COLOR_FONDO_INTERIOR, highlightthickness=0)
        scrollbar_productos = tk.Scrollbar(canvas_frame, orient="vertical", command=self.productos_canvas.yview)
        self.productos_lista_frame = tk.Frame(self.productos_canvas, bg=self.app.COLOR_FONDO_INTERIOR)

        self.productos_lista_frame.bind(
            "<Configure>",
            lambda e: self.productos_canvas.configure(scrollregion=self.productos_canvas.bbox("all"))
        )

        self.productos_canvas.create_window((0, 0), window=self.productos_lista_frame, anchor="nw")
        self.productos_canvas.configure(yscrollcommand=scrollbar_productos.set)

        self.productos_canvas.pack(side="left", fill="both", expand=True)
        scrollbar_productos.pack(side="right", fill="y")

        self._render_productos()

        carrito_frame = tk.Frame(mid_frame, bg=self.app.COLOR_FONDO_INTERIOR, padx=15, pady=15)
        carrito_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        tk.Label(
            carrito_frame,
            text="Carrito de Venta",
            font=("Arial", 12, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w")

        # Selección de cliente mayorista
        cliente_frame = tk.Frame(carrito_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        cliente_frame.pack(fill=tk.X, pady=(5, 10))

        tk.Label(
            cliente_frame,
            text="Cliente:",
            font=("Arial", 10),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(side=tk.LEFT, padx=(0, 5))

        # Crear lista de opciones para combobox
        cliente_opciones = [f"{c['nombre']} ({c['descuento']:.0f}%)" for c in self.controller.clientes]
        self.cliente_combo_var = tk.StringVar()
        if cliente_opciones:
            self.cliente_combo_var.set(cliente_opciones[0])
        
        cliente_combo = ttk.Combobox(
            cliente_frame,
            textvariable=self.cliente_combo_var,
            values=cliente_opciones,
            state="readonly",
            font=("Arial", 9),
            width=25
        )
        cliente_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        cliente_combo.bind("<<ComboboxSelected>>", self._on_cliente_seleccionado)

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

        # Label para mostrar descuento de cliente
        self.descuento_cliente_label = tk.Label(
            carrito_frame,
            text="Descuento Cliente: $0.00",
            font=("Arial", 10),
            fg="green",
            bg=self.app.COLOR_FONDO_INTERIOR,
        )
        self.descuento_cliente_label.pack(anchor="e", pady=(2, 0))

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
            text="Donar el cambio para tortillas",
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

        # Pago y Cambio
        pago_frame = tk.Frame(carrito_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        pago_frame.pack(fill=tk.X, pady=(5, 0))

        tk.Label(
            pago_frame,
            text="Pago con:",
            font=("Arial", 10),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(side=tk.LEFT)

        self.pago_var = tk.StringVar(value="0")
        self.pago_entry = tk.Entry(
            pago_frame,
            textvariable=self.pago_var,
            font=("Arial", 10),
            width=10
        )
        self.pago_entry.pack(side=tk.LEFT, padx=5)
        self.pago_entry.bind("<KeyRelease>", lambda e: self._recalcular_totales())

        self.cambio_label = tk.Label(
            carrito_frame,
            text="Cambio: $0.00",
            font=("Arial", 11, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        )
        self.cambio_label.pack(anchor="e", pady=(5, 4))

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
            text="Historial de Ventas",
            font=("Arial", 12, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(0, 10))

        # Container for tree and scrollbar
        tree_container = tk.Frame(historial_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        tree_container.pack(fill=tk.X, expand=False)

        scrollbar = tk.Scrollbar(tree_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columnas = ("id", "fecha", "hora", "total", "redondeo", "donacion")
        self.tree = ttk.Treeview(tree_container, columns=columnas, show="headings", height=12, yscrollcommand=scrollbar.set, displaycolumns=("fecha", "hora", "total", "redondeo", "donacion"))
        
        scrollbar.config(command=self.tree.yview)

        for col, texto in zip(columnas[1:], ["Fecha", "Hora", "Total", "Redondeo", "Donación"]):
            self.tree.heading(col, text=texto, command=lambda c=col: self._ordenar_columna(self.tree, c, False))
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self._on_tree_double_click)

        self._cargar_historial()

    # --- Métodos de productos ---
    def _render_productos(self):
        """Renderizar lista de productos filtrados"""
        # Limpiar productos actuales
        for w in self.productos_lista_frame.winfo_children():
            w.destroy()
        
        # Mostrar productos filtrados
        for producto in self.controller.productos_filtrados:
            nombre = producto['nombre']
            precio = producto['precio']
            
            item_frame = tk.Frame(self.productos_lista_frame, bg=self.app.COLOR_FONDO_INTERIOR)
            item_frame.pack(fill=tk.X, pady=3)

            tk.Label(
                item_frame,
                text=nombre,
                font=("Arial", 10),
                fg=self.app.COLOR_TEXTO_PRIMARIO,
                bg=self.app.COLOR_FONDO_INTERIOR,
            ).pack(side=tk.LEFT, anchor="w")

            tk.Label(
                item_frame,
                text=f"$ {precio:.2f}",
                font=("Arial", 9),
                fg=self.app.COLOR_TEXTO_PRIMARIO,
                bg=self.app.COLOR_FONDO_INTERIOR,
            ).pack(side=tk.LEFT, padx=5)

            tk.Button(
                item_frame,
                text="+",
                font=("Arial", 10, "bold"),
                bg=self.app.COLOR_BOTON_FONDO,
                fg=self.app.COLOR_BOTON_TEXTO,
                width=3,
                relief=tk.FLAT,
                command=lambda n=nombre, p=precio: self.agregar_al_carrito(n, p),
            ).pack(side=tk.RIGHT)
    
    def _filtrar_productos(self):
        """Filtrar productos según búsqueda"""
        termino = self.buscar_var.get()
        self.controller.filtrar_productos(termino)
        self._render_productos()
    
    def _on_cliente_seleccionado(self, event=None):
        """Manejar selección de cliente"""
        # Obtener índice seleccionado
        seleccion = self.cliente_combo_var.get()
        
        # Buscar cliente correspondiente
        for i, c in enumerate(self.controller.clientes):
            if f"{c['nombre']} ({c['descuento']:.0f}%)" == seleccion:
                self.controller.set_cliente(c['id'])
                self._recalcular_totales()
                break

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

        subtotal, total, descuento_cliente_monto = self.controller.calcular_totales()

        self.subtotal_label.config(text=f"Subtotal: $ {subtotal:.2f}")
        
        # Mostrar descuento de cliente si aplica
        if descuento_cliente_monto > 0:
            self.descuento_cliente_label.config(text=f"Descuento Cliente: -$ {descuento_cliente_monto:.2f}")
        else:
            self.descuento_cliente_label.config(text="Descuento Cliente: $0.00")
        
        self.total_label.config(text=f"Total a Pagar: $ {total:.2f}")

        # Calcular cambio
        try:
            pago = float(self.pago_var.get())
        except ValueError:
            pago = 0.0
        
        # Si está marcado "donar el cambio", el cambio es 0
        if self.redondeo_var.get() and pago >= total:
            cambio = 0.0
            self.cambio_label.config(text=f"Cambio: $ {cambio:.2f} (donado)", fg="green")
        else:
            cambio = pago - total
            self.cambio_label.config(text=f"Cambio: $ {cambio:.2f}", fg="green" if cambio >= 0 else "red")

    def _completar_venta(self):
        from tkinter import messagebox
        
        # Obtener monto de pago
        try:
            monto_pago = float(self.pago_var.get())
        except ValueError:
            monto_pago = 0.0
        
        id_venta = self.controller.procesar_venta(monto_pago=monto_pago)
        
        if id_venta:
            messagebox.showinfo("Venta Exitosa", f"Venta registrada correctamente.\\nID: {id_venta}")
            self.pago_var.set("0")  # Reset payment field
            self._render_carrito()
            self._cargar_historial()
        else:
            if not self.controller.carrito:
                messagebox.showwarning("Carrito Vacío", "Agregue productos antes de completar la venta.")
            else:
                messagebox.showerror("Error", "Ocurrió un error al procesar la venta.")

    def _ordenar_columna(self, tree, col, reverse):
        """Ordenar treeview por columna"""
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        
        # Intentar convertir a float para ordenamiento numérico (removiendo $)
        try:
            # Detectar si es moneda o número
            sample = l[0][0] if l else ""
            if "$" in sample:
                l.sort(key=lambda t: float(t[0].replace('$', '').replace(',', '')), reverse=reverse)
            else:
                # Intento genérico de float
                l.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            # Fallback a string sort
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

        # Invertir orden para la próxima vez
        tree.heading(col, command=lambda: self._ordenar_columna(tree, col, not reverse))

    def _cargar_historial(self):
        """Cargar y mostrar historial de ventas"""
        # Limpiar tabla actual
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Cargar datos reales
        datos = self.controller.obtener_historial_ventas()
        for fila in datos:
            self.tree.insert("", tk.END, values=fila)

    def _on_tree_double_click(self, event):
        """Manejar doble click en historial"""
        item_id = self.tree.selection()
        if not item_id:
            return
            
        item = self.tree.item(item_id)
        valores = item['values']
        if not valores:
            return
            
        # ID es el primer valor
        id_venta = valores[0]
        self._mostrar_detalle_popup(id_venta)

    def _mostrar_detalle_popup(self, id_venta):
        """Mostrar popup con detalles de la venta"""
        venta = self.controller.obtener_detalle_venta(id_venta)
        if not venta:
            return

        popup = tk.Toplevel(self)
        popup.title(f"Detalle de Venta #{id_venta}")
        popup.geometry("500x400")
        popup.configure(bg=self.app.COLOR_FONDO_EXTERIOR)

        # Header
        header = tk.Frame(popup, bg=self.app.COLOR_FONDO_INTERIOR, padx=15, pady=10)
        header.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(header, text=f"Venta #{id_venta}", font=("Arial", 14, "bold"), bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w")
        tk.Label(header, text=f"Fecha: {venta['fecha']} {venta['hora'][:5]}", font=("Arial", 10), bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w")
        
        # Items
        items_frame = tk.Frame(popup, bg=self.app.COLOR_FONDO_INTERIOR, padx=15, pady=10)
        items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        tk.Label(items_frame, text="Productos", font=("Arial", 11, "bold"), bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w", pady=(0, 5))

        # Lista de items
        canvas = tk.Canvas(items_frame, bg=self.app.COLOR_FONDO_INTERIOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(items_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.app.COLOR_FONDO_INTERIOR)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Headers items
        h_frame = tk.Frame(scrollable_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        h_frame.pack(fill=tk.X, pady=2)
        tk.Label(h_frame, text="Producto", width=25, anchor="w", font=("Arial", 9, "bold"), bg=self.app.COLOR_FONDO_INTERIOR).pack(side=tk.LEFT)
        tk.Label(h_frame, text="Cant.", width=8, anchor="center", font=("Arial", 9, "bold"), bg=self.app.COLOR_FONDO_INTERIOR).pack(side=tk.LEFT)
        tk.Label(h_frame, text="Total", width=10, anchor="e", font=("Arial", 9, "bold"), bg=self.app.COLOR_FONDO_INTERIOR).pack(side=tk.LEFT)

        for item in venta.get('items', []):
            p_nombre = item['producto']['nombre'] if item.get('producto') else "Producto desconocido"
            cantidad = item['cantidad_vendida']
            subtotal = item['subtotal']
            
            row = tk.Frame(scrollable_frame, bg=self.app.COLOR_FONDO_INTERIOR)
            row.pack(fill=tk.X, pady=2)
            
            tk.Label(row, text=p_nombre, width=25, anchor="w", font=("Arial", 9), bg=self.app.COLOR_FONDO_INTERIOR).pack(side=tk.LEFT)
            tk.Label(row, text=f"{cantidad}", width=8, anchor="center", font=("Arial", 9), bg=self.app.COLOR_FONDO_INTERIOR).pack(side=tk.LEFT)
            tk.Label(row, text=f"${subtotal:.2f}", width=10, anchor="e", font=("Arial", 9), bg=self.app.COLOR_FONDO_INTERIOR).pack(side=tk.LEFT)

        # Totales
        total_frame = tk.Frame(popup, bg=self.app.COLOR_FONDO_INTERIOR, padx=15, pady=10)
        total_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(total_frame, text=f"Total: ${venta['monto_total']:.2f}", font=("Arial", 12, "bold"), bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="e")

