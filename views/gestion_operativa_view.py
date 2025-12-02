import tkinter as tk
from tkinter import ttk, messagebox

class GestionOperativaView(tk.Frame):
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
            text="Inventario de Productos",
            font=("Arial", 12, "bold"),
            fg=self.app.COLOR_TEXTO_PRIMARIO,
            bg=self.app.COLOR_FONDO_INTERIOR,
        ).pack(anchor="w", pady=(0, 10))

        boton_frame = tk.Frame(marco, bg=self.app.COLOR_FONDO_INTERIOR)
        boton_frame.pack(anchor="e", fill=tk.X, pady=(0, 10))

        tk.Button(
            boton_frame,
            text="+  Agregar Producto",
            font=("Arial", 10, "bold"),
            bg=self.app.COLOR_BOTON_FONDO,
            fg=self.app.COLOR_BOTON_TEXTO,
            relief=tk.FLAT,
            padx=15,
            pady=5,
            command=self.abrir_dialogo_agregar # Conectar comando
        ).pack(side=tk.RIGHT)

        columnas = ("producto", "cantidad", "unidad", "precio", "valor", "acciones")
        self.tree = ttk.Treeview(marco, columns=columnas, show="headings", height=6) # Guardar referencia a self.tree
        titulos = [
            "Producto",
            "Cantidad",
            "Unidad",
            "Precio Unitario",
            "Valor Total",
            "Acciones",
        ]
        for col, texto in zip(columnas, titulos):
            self.tree.heading(col, text=texto)
            self.tree.column(col, anchor="center", width=130)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(marco, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Bind doble click
        self.tree.bind("<Double-1>", self.on_double_click)

        self.refrescar_tabla()

    def refrescar_tabla(self):
        """Limpia y recarga la tabla desde el controlador"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for fila in self.controller.inventario:
            self.tree.insert("", tk.END, values=fila)

    def on_double_click(self, event):
        """Maneja el doble clic en una fila"""
        item_id = self.tree.selection()[0]
        index = self.tree.index(item_id)
        
        # Mostrar menú contextual o diálogo de opciones
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Editar", command=lambda: self.abrir_dialogo_editar(index))
        menu.add_command(label="Eliminar", command=lambda: self.confirmar_eliminar(index))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def abrir_dialogo_agregar(self):
        """Abre diálogo para agregar nuevo producto"""
        ProductDialog(self, "Agregar Producto", self.controller)

    def abrir_dialogo_editar(self, index):
        """Abre diálogo para editar producto existente"""
        producto = self.controller.obtener_producto_por_indice(index)
        if producto:
            ProductDialog(self, "Editar Producto", self.controller, producto, index)

    def confirmar_eliminar(self, index):
        """Confirma y elimina el producto"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este producto?"):
            success, message = self.controller.eliminar_producto(index)
            if success:
                self.refrescar_tabla()
                messagebox.showinfo("Éxito", message)
            else:
                messagebox.showerror("Error", message)

class ProductDialog(tk.Toplevel):
    """Diálogo para agregar/editar productos"""
    def __init__(self, parent, title, controller, producto=None, index=None):
        super().__init__(parent)
        self.controller = controller
        self.producto = producto
        self.index = index
        self.parent_view = parent
        
        self.title(title)
        self.geometry("400x500")
        self.configure(bg="#ffffff")
        
        # Modal
        self.transient(parent)
        self.grab_set()
        
        self._construir_form()
        
        if producto:
            self._llenar_datos()

    def _construir_form(self):
        frame = tk.Frame(self, bg="#ffffff", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Nombre
        tk.Label(frame, text="Nombre:", bg="#ffffff", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,0))
        self.nombre_entry = tk.Entry(frame, width=40)
        self.nombre_entry.pack(fill=tk.X, pady=(0,10))
        
        # Stock
        tk.Label(frame, text="Stock Inicial:", bg="#ffffff", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,0))
        self.stock_entry = tk.Entry(frame, width=40)
        self.stock_entry.pack(fill=tk.X, pady=(0,10))
        
        # Unidad
        tk.Label(frame, text="Unidad de Medida:", bg="#ffffff", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,0))
        self.unidad_combo = ttk.Combobox(frame, values=["kg", "l", "ml", "pz"], state="readonly")
        self.unidad_combo.pack(fill=tk.X, pady=(0,10))
        self.unidad_combo.set("kg")
        
        # Costo
        tk.Label(frame, text="Costo Unitario ($):", bg="#ffffff", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,0))
        self.costo_entry = tk.Entry(frame, width=40)
        self.costo_entry.pack(fill=tk.X, pady=(0,10))
        
        # Descripción
        tk.Label(frame, text="Descripción:", bg="#ffffff", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,0))
        self.desc_entry = tk.Entry(frame, width=40)
        self.desc_entry.pack(fill=tk.X, pady=(0,10))
        
        # Botones
        btn_frame = tk.Frame(frame, bg="#ffffff", pady=20)
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="Guardar", command=self.guardar, 
                 bg="#FDB813", fg="white", font=("Arial", 10, "bold"), relief=tk.FLAT, padx=20).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(btn_frame, text="Cancelar", command=self.destroy, 
                 bg="#cccccc", fg="black", font=("Arial", 10), relief=tk.FLAT, padx=20).pack(side=tk.RIGHT, padx=5)

    def _llenar_datos(self):
        self.nombre_entry.insert(0, self.producto['nombre'])
        self.stock_entry.insert(0, str(self.producto['stock']))
        self.unidad_combo.set(self.producto['unidad_medida'])
        self.costo_entry.insert(0, str(self.producto['costo_unitario']))
        if self.producto.get('descripcion'):
            self.desc_entry.insert(0, self.producto['descripcion'])

    def guardar(self):
        nombre = self.nombre_entry.get().strip()
        stock = self.stock_entry.get().strip()
        unidad = self.unidad_combo.get()
        costo = self.costo_entry.get().strip()
        desc = self.desc_entry.get().strip()
        
        if not nombre or not stock or not costo:
            messagebox.showerror("Error", "Nombre, Stock y Costo son obligatorios")
            return
            
        try:
            stock_val = float(stock)
            costo_val = float(costo)
        except ValueError:
            messagebox.showerror("Error", "Stock y Costo deben ser números válidos")
            return
            
        exito = False
        if self.producto: # Actualizar
            exito = self.controller.actualizar_producto(
                self.index, nombre, stock_val, unidad, costo_val, desc
            )
        else: # Agregar
            exito = self.controller.agregar_producto(
                nombre, stock_val, unidad, costo_val, desc
            )
            
        if exito:
            self.parent_view.refrescar_tabla()
            self.destroy()
            messagebox.showinfo("Éxito", "Operación realizada correctamente")
        else:
            messagebox.showerror("Error", "No se pudo guardar el producto")
