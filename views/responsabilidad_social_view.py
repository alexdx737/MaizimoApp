import tkinter as tk
from tkinter import ttk


class ResponsabilidadSocialView(tk.Frame):
    def __init__(self, parent, app: "MainApp", controller):
        super().__init__(parent, bg=app.COLOR_FONDO_EXTERIOR)
        self.app = app
        self.controller = controller
        self._construir_ui()

    def _construir_ui(self):
        # Simple scrollable layout
        canvas = tk.Canvas(self, bg=self.app.COLOR_FONDO_EXTERIOR, highlightthickness=0)
        scrollbar_v = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.app.COLOR_FONDO_EXTERIOR)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="n", width=canvas.winfo_width())
        canvas.configure(yscrollcommand=scrollbar_v.set)
        
        def on_canvas_resize(event):
            canvas.itemconfig("all", width=event.width)
        
        canvas.bind("<Configure>", on_canvas_resize)
        
        # Pack scrollbar and canvas
        scrollbar_v.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        
        # Content wrapper for centering
        content_wrapper = tk.Frame(scrollable_frame, bg=self.app.COLOR_FONDO_EXTERIOR)
        content_wrapper.pack(expand=True, fill="both", padx=20, pady=20)
        
        marco = tk.Frame(content_wrapper, bg=self.app.COLOR_FONDO_INTERIOR, padx=25, pady=25, relief=tk.FLAT, bd=1, highlightbackground="#D0D0D0", highlightthickness=1)
        marco.pack(expand=True)
        
        # Top container - Info cards side by side
        top_container = tk.Frame(marco, bg=self.app.COLOR_FONDO_INTERIOR)
        top_container.pack(fill=tk.X, pady=(0, 20))
        
        # Left card - Descuento por No Usar Bolsa
        descuento_frame = tk.Frame(top_container, bg=self.app.COLOR_FONDO_INTERIOR)
        descuento_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

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

        # Right card - Sistema de Redondeo Solidario
        redondeo_frame = tk.Frame(top_container, bg=self.app.COLOR_FONDO_INTERIOR)
        redondeo_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

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

        self.fondo_label = tk.Label(
            info_frame,
            text=f"Fondo Acumulado\n${self.controller.fondo_acumulado:.2f}",
            font=("Arial", 11),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg="#F4C97A",
            padx=15,
            pady=10,
        )
        self.fondo_label.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)

        self.tortillas_label = tk.Label(
            info_frame,
            text=f"Equivalente en Tortillas\n{self.controller.equivalente_tortillas_kg} kg",
            font=("Arial", 11),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg="#D2E5A1",
            padx=15,
            pady=10,
        )
        self.tortillas_label.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Botón para refrescar datos
        tk.Button(
            redondeo_frame,
            text="🔄 Actualizar Datos",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            command=self.actualizar_valores
        ).pack(anchor="w", pady=(5, 0))
        
        # Bottom container - Donation history table
        bottom_container = tk.Frame(marco, bg=self.app.COLOR_FONDO_INTERIOR)
        bottom_container.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            bottom_container,
            text="Historial de Donaciones",
            font=("Arial", 11, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(0, 10))

        # Treeview container
        tree_container = tk.Frame(bottom_container, bg=self.app.COLOR_FONDO_INTERIOR)
        tree_container.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(tree_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
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

        columnas = ("id_venta", "fecha", "hora", "monto")
        self.tree = ttk.Treeview(tree_container, columns=columnas, show="headings", 
                                 height=8, yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=self.tree.yview)

        titulos = ["ID Venta", "Fecha", "Hora", "Monto Donado"]
        for col, texto in zip(columnas, titulos):
            self.tree.heading(col, text=texto)
            if col == "monto":
                self.tree.column(col, anchor="center", width=120)
            elif col == "id_venta":
                self.tree.column(col, anchor="center", width=80)
            else:
                self.tree.column(col, anchor="center", width=100)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._cargar_donaciones()
    
    def _cargar_donaciones(self):
        """Cargar donaciones en el Treeview"""
        # Limpiar Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar donaciones
        for donacion in self.controller.donaciones:
            self.tree.insert("", tk.END, values=(
                donacion['id_venta'],
                donacion['fecha'],
                donacion['hora'],
                f"${donacion['monto']:.2f}"
            ))
    
    def actualizar_valores(self):
        """Actualizar valores mostrados en la interfaz"""
        self.controller.actualizar_datos()
        
        # Actualizar labels
        self.fondo_label.config(text=f"Fondo Acumulado\n${self.controller.fondo_acumulado:.2f}")
        self.tortillas_label.config(text=f"Equivalente en Tortillas\n{self.controller.equivalente_tortillas_kg} kg")
        
        # Recargar donaciones
        self._cargar_donaciones()
