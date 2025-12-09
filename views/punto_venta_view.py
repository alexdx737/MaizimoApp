import tkinter as tk
from tkinter import ttk
import customtkinter as ctk



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
        # Registrar validación para entradas numéricas
        self.vcmd_decimal = (self.register(self._validar_numero_decimal), '%P')
        
        # Create canvas for scrolling (no visible scrollbars, gesture-only)
        canvas = tk.Canvas(self, bg=self.app.COLOR_FONDO_EXTERIOR, highlightthickness=0)
        scrollable_frame = tk.Frame(canvas, bg=self.app.COLOR_FONDO_EXTERIOR)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Bind canvas resize to update scrollable_frame width
        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)
        
        # Pack canvas
        canvas.pack(side="left", fill="both", expand=True)
        
        # Enable mousewheel/touchpad scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        
        # Enable horizontal scrolling with Shift+MouseWheel
        def _on_horizontal_mousewheel(event):
            canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<Shift-MouseWheel>", _on_horizontal_mousewheel)
        
        top_info = tk.Frame(scrollable_frame, bg=self.app.COLOR_FONDO_EXTERIOR)
        top_info.pack(fill=tk.X)

        fondo_frame = ctk.CTkFrame(top_info, fg_color=self.app.COLOR_FONDO_INTERIOR, corner_radius=15, height=150)
        fondo_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=10)
        fondo_frame.pack_propagate(False)
        
        # Inner frame for padding
        fondo_inner = tk.Frame(fondo_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        fondo_inner.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        tk.Label(
            fondo_inner,
            text="Fondo de Redondeo",
            font=("Arial", 10, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w")
        
        self.fondo_var = tk.StringVar(value="$0.00 MXN")
        tk.Label(
            fondo_inner,
            textvariable=self.fondo_var,
            font=("Arial", 12),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(5, 0))

        eq_frame = ctk.CTkFrame(top_info, fg_color=self.app.COLOR_FONDO_INTERIOR, corner_radius=15, height=150)
        eq_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0), pady=10)
        eq_frame.pack_propagate(False)
        
        # Inner frame for padding
        eq_inner = tk.Frame(eq_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        eq_inner.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        tk.Label(
            eq_inner,
            text="Equivalente en Tortillas",
            font=("Arial", 10, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w")
        
        self.equivalente_var = tk.StringVar(value="0 kg")
        tk.Label(
            eq_inner,
            textvariable=self.equivalente_var,
            font=("Arial", 12),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(5, 0))
        
        # Cargar datos de donaciones
        self._actualizar_fondo_donaciones()
        
        # Botón para reiniciar el fondo
        ctk.CTkButton(
            fondo_inner,
            text="Reiniciar Fondo",
            font=("Segoe UI", 9, "bold"),
            fg_color=self.app.COLOR_BOTON_FONDO,
            text_color="white",
            hover_color=self.app.COLOR_BOTON_FONDO,
            corner_radius=8,
            height=32,
            cursor="hand2",
            command=self._reiniciar_fondo_donaciones
        ).pack(anchor="w", pady=(12, 0))

        mid_frame = tk.Frame(scrollable_frame, bg=self.app.COLOR_FONDO_EXTERIOR)
        mid_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Configure grid layout for responsive columns
        mid_frame.columnconfigure(0, weight=1, minsize=250)
        mid_frame.columnconfigure(1, weight=1, minsize=250)
        mid_frame.columnconfigure(2, weight=1, minsize=250)
        mid_frame.rowconfigure(0, weight=1)

        productos_frame = ctk.CTkFrame(mid_frame, fg_color=self.app.COLOR_FONDO_INTERIOR, corner_radius=15)
        productos_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Inner frame for padding
        productos_inner = tk.Frame(productos_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        productos_inner.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        tk.Label(
            productos_inner,
            text="Productos",
            font=("Segoe UI", 13, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(0, 10))

        # Buscador de productos
        buscar_frame = tk.Frame(productos_inner, bg=self.app.COLOR_FONDO_INTERIOR)
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

        # Canvas para lista de productos (sin scrollbar visible, solo gestos)
        canvas_frame = tk.Frame(productos_inner, bg=self.app.COLOR_FONDO_INTERIOR)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.productos_canvas = tk.Canvas(canvas_frame, bg=self.app.COLOR_FONDO_INTERIOR, highlightthickness=0)
        self.productos_lista_frame = tk.Frame(self.productos_canvas, bg=self.app.COLOR_FONDO_INTERIOR)

        self.productos_lista_frame.bind(
            "<Configure>",
            lambda e: self.productos_canvas.configure(scrollregion=self.productos_canvas.bbox("all"))
        )

        self.productos_canvas.create_window((0, 0), window=self.productos_lista_frame, anchor="nw")

        self.productos_canvas.pack(fill="both", expand=True)
        
        # Enable mousewheel/touchpad scrolling for products list
        def _on_productos_mousewheel(event):
            self.productos_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.productos_canvas.bind("<MouseWheel>", _on_productos_mousewheel)

        self._render_productos()

        carrito_frame = ctk.CTkFrame(mid_frame, fg_color=self.app.COLOR_FONDO_INTERIOR, corner_radius=15)
        carrito_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        
        # Inner frame for padding
        carrito_inner = tk.Frame(carrito_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        carrito_inner.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        tk.Label(
            carrito_inner,
            text="Carrito de Venta",
            font=("Segoe UI", 13, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(0, 10))

        # Selección de cliente mayorista
        cliente_frame = tk.Frame(carrito_inner, bg=self.app.COLOR_FONDO_INTERIOR)
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

        self.carrito_items_frame = tk.Frame(carrito_inner, bg=self.app.COLOR_FONDO_INTERIOR)
        self.carrito_items_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 5))

        self.subtotal_label = tk.Label(
            carrito_inner,
            text="Subtotal: $0.00",
            font=("Arial", 11),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        )
        self.subtotal_label.pack(anchor="e", pady=(5, 0))

        # Label para mostrar descuento de cliente
        self.descuento_cliente_label = tk.Label(
            carrito_inner,
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
            carrito_inner,
            text="Total a Pagar: $0.00",
            font=("Arial", 11, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        )
        self.total_label.pack(anchor="e", pady=(8, 4))

        # Pago y Cambio
        pago_frame = tk.Frame(carrito_inner, bg=self.app.COLOR_FONDO_INTERIOR)
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
            width=10,
            validate="key",
            validatecommand=self.vcmd_decimal
        )
        self.pago_entry.pack(side=tk.LEFT, padx=5)
        self.pago_entry.bind("<KeyRelease>", lambda e: self._recalcular_totales())

        self.cambio_label = tk.Label(
            carrito_inner,
            text="Cambio: $0.00",
            font=("Arial", 11, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        )
        self.cambio_label.pack(anchor="e", pady=(5, 4))

        ctk.CTkButton(
            carrito_inner,
            text="Completar Venta",
            font=("Segoe UI", 11, "bold"),
            fg_color=self.app.COLOR_BOTON_FONDO,
            text_color="white",
            hover_color=self.app.COLOR_BOTON_FONDO,
            corner_radius=8,
            height=40,
            cursor="hand2",
            command=self._completar_venta,
        ).pack(fill=tk.X, pady=(10, 0))

        self._render_carrito()

        # Historial de Ventas - Tercera columna
        historial_frame = ctk.CTkFrame(mid_frame, fg_color=self.app.COLOR_FONDO_INTERIOR, corner_radius=15)
        historial_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        
        # Inner frame for padding
        historial_inner = tk.Frame(historial_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        historial_inner.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        # Header con título y botón
        header_frame = tk.Frame(historial_inner, bg=self.app.COLOR_FONDO_INTERIOR)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Pack buttons first (right to left)
        ctk.CTkButton(
            header_frame,
            text="🗑 Reiniciar",
            font=("Segoe UI", 8, "bold"),
            fg_color="#E57373",
            text_color="white",
            hover_color="#D32F2F",
            corner_radius=6,
            width=75,
            height=26,
            cursor="hand2",
            command=self._reiniciar_historial_ventas
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        ctk.CTkButton(
            header_frame,
            text="📊 Reporte Semanal",
            font=("Segoe UI", 8, "bold"),
            fg_color="#81C784",
            text_color="white",
            hover_color="#66BB6A",
            corner_radius=6,
            width=115,
            height=26,
            cursor="hand2",
            command=self._generar_reporte_semanal
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Then pack label (left side)
        tk.Label(
            header_frame,
            text="Historial de Ventas",
            font=("Segoe UI", 13, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(side=tk.LEFT)

        # Container for tree (sin scrollbar visible, solo gestos)
        tree_container = tk.Frame(historial_inner, bg=self.app.COLOR_FONDO_INTERIOR)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        # Configure Treeview style for distinct headers
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading",
                       background=self.app.COLOR_BOTON_FONDO,
                       foreground="white",
                       font=("Segoe UI", 10, "bold"),
                       relief="flat")
        style.map("Treeview.Heading",
                 background=[('active', self.app.COLOR_BOTON_FONDO)])
        style.configure("Treeview",
                       background="white",
                       fieldbackground="white",
                       foreground=self.app.COLOR_TEXTO_PRIMARIO,
                       font=("Segoe UI", 9))

        columnas = ("id", "fecha", "hora", "total", "redondeo", "donacion")
        self.tree = ttk.Treeview(tree_container, columns=columnas, show="headings", height=10, displaycolumns=("fecha", "hora", "total", "redondeo", "donacion"))

        for col, texto in zip(columnas[1:], ["Fecha", "Hora", "Total", "Redondeo", "Donación"]):
            self.tree.heading(col, text=texto, command=lambda c=col: self._ordenar_columna(self.tree, c, False))
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Enable mousewheel/touchpad scrolling for tree
        def _on_tree_mousewheel(event):
            self.tree.yview_scroll(int(-1*(event.delta/120)), "units")
        self.tree.bind("<MouseWheel>", _on_tree_mousewheel)
        self.tree.bind("<Double-1>", self._on_tree_double_click)

        self._cargar_historial()
        
        # Bind mousewheel to all widgets for scrolling from anywhere
        self._bind_mousewheel_recursively(self, canvas)

    def _bind_mousewheel_recursively(self, widget, canvas):
        """Bind mousewheel events to widget and all its children for scrolling"""
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _on_horizontal_mousewheel(event):
            canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind to this widget
        widget.bind("<MouseWheel>", _on_mousewheel)
        widget.bind("<Shift-MouseWheel>", _on_horizontal_mousewheel)
        
        # Recursively bind to all children
        for child in widget.winfo_children():
            # Skip the productos_canvas and tree to avoid conflicts with their own scrolling
            if child != getattr(self, 'productos_canvas', None) and child != getattr(self, 'tree', None):
                self._bind_mousewheel_recursively(child, canvas)

    # --- Métodos de productos ---
    def _actualizar_fondo_donaciones(self):
        """Actualizar el fondo de donaciones y equivalente en tortillas"""
        try:
            from models.donacion_model import DonacionModel
            total_donaciones = DonacionModel.obtener_total()
            
            # Actualizar fondo
            self.fondo_var.set(f"${total_donaciones:.2f} MXN")
            
            # Calcular equivalente en tortillas (asumiendo $25 por kg)
            precio_tortilla_kg = 25.0
            kg_equivalente = total_donaciones / precio_tortilla_kg if precio_tortilla_kg > 0 else 0
            self.equivalente_var.set(f"{kg_equivalente:.0f} kg")
            
        except Exception as e:
            print(f"Error actualizando fondo de donaciones: {e}")
            self.fondo_var.set("$0.00 MXN")
            self.equivalente_var.set("0 kg")
    
    def _solicitar_contrasena(self):
        """Solicitar contraseña del usuario para operaciones sensibles"""
        from tkinter import simpledialog, messagebox
        
        # Get current user's password from main app if available
        password = simpledialog.askstring(
            "Autenticación Requerida",
            "Ingrese su contraseña para continuar:",
            show='*'
        )
        
        if not password:
            return False
        
        # Validate password with current user
        try:
            from models.usuario_model import UsuarioModel
            
            # Get user ID from main app
            if hasattr(self.app, 'usuario_data') and self.app.usuario_data:
                user_id = self.app.usuario_data.get('id_usuario')
                if user_id:
                    user = UsuarioModel.validar_credenciales(str(user_id), password)
                    if user:
                        return True
            
            messagebox.showerror("Error", "Contraseña incorrecta")
            return False
        except Exception as e:
            print(f"Error validando contraseña: {e}")
            messagebox.showerror("Error", "No se pudo validar la contraseña")
            return False
    
    def _reiniciar_fondo_donaciones(self):
        """Reiniciar el fondo de donaciones a cero"""
        from tkinter import messagebox
        
        # Solicitar contraseña
        if not self._solicitar_contrasena():
            return
        
        # Confirmar con el usuario
        confirmacion = messagebox.askyesno(
            "Confirmar Reinicio",
            "¿Está seguro que desea reiniciar el fondo de donaciones a $0?\n\n"
            "Esta acción eliminará todos los registros de donaciones.\n"
            "Solo debe hacerse después de entregar las tortillas a las familias."
        )
        
        if not confirmacion:
            return
        
        try:
            from core.database import get_supabase_client
            supabase = get_supabase_client()
            
            # Eliminar todas las donaciones
            supabase.table('donacion').delete().neq('id_donacion', 0).execute()
            
            # Actualizar display
            self._actualizar_fondo_donaciones()
            messagebox.showinfo("Éxito", "El fondo de donaciones ha sido reiniciado a $0.00")
            
        except Exception as e:
            print(f"Error reiniciando fondo de donaciones: {e}")
            messagebox.showerror("Error", f"No se pudo reiniciar el fondo: {str(e)}")
    
    def _reiniciar_historial_ventas(self):
        """Reiniciar el historial de ventas"""
        from tkinter import messagebox
        
        # Solicitar contraseña
        if not self._solicitar_contrasena():
            return
        
        # Confirmar con el usuario
        confirmacion = messagebox.askyesno(
            "Confirmar Reinicio",
            "¿Está seguro que desea reiniciar el historial de ventas?\n\n"
            "Esta acción eliminará TODOS los registros de ventas.\n"
            "Esta operación es IRREVERSIBLE."
        )
        
        if not confirmacion:
            return
        
        try:
            from core.database import get_supabase_client
            supabase = get_supabase_client()
            
            # Eliminar todas las ventas (esto también eliminará items y donaciones por cascade)
            supabase.table('venta_completa').delete().neq('id_venta_completa', 0).execute()
            
            # Recargar historial
            self._cargar_historial()
            
            # Actualizar donaciones también
            self._actualizar_fondo_donaciones()
            
            messagebox.showinfo("Éxito", "El historial de ventas ha sido reiniciado")
            
        except Exception as e:
            print(f"Error reiniciando historial: {e}")
            messagebox.showerror("Error", f"No se pudo reiniciar el historial: {str(e)}")
    
    def _generar_reporte_semanal(self):
        """Generar y descargar reporte semanal de ventas en Excel"""
        from tkinter import filedialog, messagebox
        from datetime import datetime
        
        try:
            # Generar nombre de archivo por defecto
            fecha_actual = datetime.now().strftime("%Y%m%d")
            nombre_archivo = f"reporte_semanal_{fecha_actual}.pdf"
            
            # Abrir diálogo para guardar archivo
            ruta_archivo = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=nombre_archivo,
                title="Guardar Reporte Semanal"
            )
            
            # Si el usuario canceló, salir
            if not ruta_archivo:
                return
            
            # Generar el reporte
            exito = self.controller.generar_reporte_semanal(ruta_archivo)
            
            if exito:
                messagebox.showinfo(
                    "Éxito", 
                    f"Reporte semanal generado correctamente.\n\nArchivo guardado en:\n{ruta_archivo}"
                )
            else:
                messagebox.showerror(
                    "Error", 
                    "No se pudo generar el reporte semanal."
                )
                
        except Exception as e:
            print(f"Error generando reporte: {e}")
            messagebox.showerror("Error", f"Ocurrió un error al generar el reporte:\n{str(e)}")
    
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

            ctk.CTkButton(
                item_frame,
                text="+",
                font=("Segoe UI", 11, "bold"),
                fg_color=self.app.COLOR_BOTON_FONDO,
                text_color="white",
                hover_color=self.app.COLOR_BOTON_FONDO,
                corner_radius=8,
                width=35,
                height=28,
                cursor="hand2",
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
        
        
        # Si está marcado "donar el cambio", el cambio es 0 y mostramos la donación
        if self.redondeo_var.get() and pago >= total:
            donacion = pago - total
            cambio = 0.0
            self.cambio_label.config(text=f"Cambio: ${cambio:.2f} (Donación: ${donacion:.2f})", fg="green")
        else:
            cambio = pago - total
            self.cambio_label.config(text=f"Cambio: $ {cambio:.2f}", fg="green" if cambio >= 0 else "red")

    def _validar_numero_decimal(self, new_value):
        """Valida que la entrada sea un número decimal válido o vacío"""
        if new_value == "":
            return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    def _completar_venta(self):
        from tkinter import messagebox
        
        # Obtener totales actuales para verificar
        _, total_a_pagar, _ = self.controller.calcular_totales()

        # Obtener monto de pago
        try:
            monto_pago = float(self.pago_var.get())
        except ValueError:
            monto_pago = 0.0
            
        # Validar que el pago sea suficiente
        # Si hay redondeo y el pago es mayor o igual, ya se maneja en el cobro,
        # pero aquí aseguramos que cubra el monto.
        
        # Nota: Si el total es 0 (todo gratis o error), pasa. 
        # Pero si hay total, debe pagar.
        # Nota: Si el total es 0 (todo gratis o error), pasa. 
        # Pero si hay total, debe pagar.
        if total_a_pagar > 0 and monto_pago < total_a_pagar:
            falta = total_a_pagar - monto_pago
            messagebox.showwarning("Pago Insuficiente", f"El monto recibido es menor al total.\\nFaltan: ${falta:.2f}")
            return
        
        try:
            id_venta = self.controller.procesar_venta(monto_pago=monto_pago)
            
            if id_venta:
                messagebox.showinfo("Venta Exitosa", f"Venta registrada correctamente.\\nID: {id_venta}")
                self.pago_var.set("0")  # Reset payment field
                self._render_carrito()
                self._cargar_historial()
                # Refrescar lista de productos (stock actualizado)
                self._filtrar_productos()
                # Actualizar fondo de donaciones
                self._actualizar_fondo_donaciones()
            else:
                if not self.controller.carrito:
                    messagebox.showwarning("Carrito Vacío", "Agregue productos antes de completar la venta.")
                else:
                    messagebox.showerror("Error", "Ocurrió un error al procesar la venta.")
        except ValueError as ve:
            messagebox.showerror("Stock Insuficiente", str(ve))

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
        popup.geometry("550x550")
        popup.configure(bg=self.app.COLOR_FONDO_EXTERIOR)

        # Header
        header = tk.Frame(popup, bg=self.app.COLOR_FONDO_INTERIOR, padx=15, pady=10)
        header.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(header, text=f"Venta #{id_venta}", font=("Arial", 14, "bold"), bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w")
        tk.Label(header, text=f"Fecha: {venta['fecha']} {venta['hora'][:5]}", font=("Arial", 10), bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w")
        
        # Información del cliente
        cliente_info = venta.get('cliente')
        if cliente_info:
            cliente_nombre = cliente_info.get('nombre', 'N/A')
            cliente_descuento = cliente_info.get('descuento', 0)
            tk.Label(header, text=f"Cliente: {cliente_nombre} (Descuento: {cliente_descuento:.0f}%)", font=("Arial", 10), bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w")
        
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

        # Totales y detalles
        total_frame = tk.Frame(popup, bg=self.app.COLOR_FONDO_INTERIOR, padx=15, pady=10)
        total_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Calcular subtotal (suma de items)
        subtotal_items = sum(item['subtotal'] for item in venta.get('items', []))
        
        # Mostrar subtotal
        tk.Label(total_frame, text=f"Subtotal: ${subtotal_items:.2f}", font=("Arial", 10), bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO, anchor="e").pack(anchor="e")
        
        # Separador
        tk.Frame(total_frame, height=1, bg="#D0D0D0").pack(fill=tk.X, pady=5)
        
        # Total
        tk.Label(total_frame, text=f"Total: ${venta['monto_total']:.2f}", font=("Arial", 12, "bold"), bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO, anchor="e").pack(anchor="e")
        
        # Mostrar donación si aplica
        donaciones = venta.get('donacion', [])
        # Supabase returns donations as a list (1:N relationship)
        if isinstance(donaciones, list) and len(donaciones) > 0:
            monto_donacion = float(donaciones[0].get('monto_redondeo', 0))
            if monto_donacion > 0:
                tk.Label(total_frame, text=f"Donación para Tortillas: ${monto_donacion:.2f}", font=("Arial", 10, "bold"), bg=self.app.COLOR_FONDO_INTERIOR, fg="#FF6B35", anchor="e").pack(anchor="e", pady=(5, 0))
            else:
                tk.Label(total_frame, text="Donación: No se realizó donación", font=("Arial", 10), bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO, anchor="e").pack(anchor="e", pady=(5, 0))
        elif isinstance(donaciones, dict):
            # In case it returns a single object instead of list
            monto_donacion = float(donaciones.get('monto_redondeo', 0))
            if monto_donacion > 0:
                tk.Label(total_frame, text=f"Donación para Tortillas: ${monto_donacion:.2f}", font=("Arial", 10, "bold"), bg=self.app.COLOR_FONDO_INTERIOR, fg="#FF6B35", anchor="e").pack(anchor="e", pady=(5, 0))
            else:
                tk.Label(total_frame, text="Donación: No se realizó donación", font=("Arial", 10), bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO, anchor="e").pack(anchor="e", pady=(5, 0))
        else:
            tk.Label(total_frame, text="Donación: No se realizó donación", font=("Arial", 10), bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO, anchor="e").pack(anchor="e", pady=(5, 0))


