import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class ClientesMayoristasView(tk.Frame):
    def __init__(self, parent, app: "MainApp", controller):
        super().__init__(parent, bg=app.COLOR_FONDO_EXTERIOR)
        self.app = app
        self.controller = controller
        self._construir_ui()

    def _construir_ui(self):
        marco = tk.Frame(self, bg=self.app.COLOR_FONDO_INTERIOR, padx=25, pady=25, relief=tk.FLAT, bd=1, highlightbackground="#D0D0D0", highlightthickness=1)
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
            command=self._agregar_cliente
        ).pack(side=tk.RIGHT)

        # Treeview container con scrollbar
        tree_frame = tk.Frame(marco, bg=self.app.COLOR_FONDO_INTERIOR)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columnas = ("id", "cliente", "contacto", "descuento")
        self.tree = ttk.Treeview(tree_frame, columns=columnas, show="headings", 
                                 height=10, yscrollcommand=scrollbar.set,
                                 displaycolumns=("cliente", "contacto", "descuento"))
        
        scrollbar.config(command=self.tree.yview)

        titulos = ["Cliente", "Contacto", "Descuento"]
        columnas_display = ("cliente", "contacto", "descuento")
        for col, texto in zip(columnas_display, titulos):
            self.tree.heading(col, text=texto)
            self.tree.column(col, anchor="center", width=180)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind double click para editar
        self.tree.bind("<Double-1>", self._on_doble_click)
        
        # Menu contextual (click derecho)
        self.menu_contextual = tk.Menu(self, tearoff=0)
        self.menu_contextual.add_command(label="Editar", command=self._editar_seleccionado)
        self.menu_contextual.add_command(label="Eliminar", command=self._eliminar_seleccionado)
        
        self.tree.bind("<Button-3>", self._mostrar_menu_contextual)

        self._cargar_datos()

    def _cargar_datos(self):
        """Cargar datos en el Treeview"""
        # Limpiar Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar clientes
        for cliente in self.controller.clientes:
            self.tree.insert("", tk.END, values=(
                cliente['id'],
                cliente['nombre'],
                cliente['telefono'],
                cliente['descuento_str']
            ))
    
    def _on_doble_click(self, event):
        """Manejar doble click en una fila"""
        item_id = self.tree.selection()
        if not item_id:
            return
        
        item = self.tree.item(item_id)
        valores = item['values']
        if not valores:
            return
        
        id_cliente = valores[0]
        self._editar_cliente(id_cliente)
    
    def _agregar_cliente(self):
        """Mostrar diálogo para agregar cliente"""
        dialog = ClienteDialog(self, self.app, "Agregar Cliente")
        dialog.wait_window()
        
        if dialog.resultado:
            datos = dialog.resultado
            exito = self.controller.agregar_cliente(
                nombre=datos['nombre'],
                apellido_paterno=datos['apellido_paterno'],
                telefono=datos['telefono'],
                apellido_materno=datos.get('apellido_materno'),
                direccion=datos.get('direccion'),
                descuento=datos.get('descuento', 0.0),
                descripcion=datos.get('descripcion')
            )
            
            if exito:
                messagebox.showinfo("Éxito", "Cliente agregado correctamente")
                self._cargar_datos()
            else:
                messagebox.showerror("Error", "No se pudo agregar el cliente")
    
    def _editar_cliente(self, id_cliente):
        """Mostrar diálogo para editar cliente"""
        cliente = self.controller.obtener_cliente(id_cliente)
        if not cliente:
            return
        
        dialog = ClienteDialog(self, self.app, "Editar Cliente", cliente)
        dialog.wait_window()
        
        if dialog.resultado:
            datos = dialog.resultado
            exito = self.controller.actualizar_cliente(
                id_cliente=id_cliente,
                nombre=datos['nombre'],
                apellido_paterno=datos['apellido_paterno'],
                apellido_materno=datos.get('apellido_materno'),
                telefono=datos['telefono'],
                direccion=datos.get('direccion'),
                descuento=datos.get('descuento', 0.0),
                descripcion=datos.get('descripcion')
            )
            
            if exito:
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
                self._cargar_datos()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el cliente")

    def _mostrar_menu_contextual(self, event):
        """Mostrar menú contextual en la posición del mouse"""
        item_id = self.tree.identify_row(event.y)
        if item_id:
            self.tree.selection_set(item_id)
            self.menu_contextual.post(event.x_root, event.y_root)

    def _editar_seleccionado(self):
        """Wrapper para editar desde menú"""
        item_id = self.tree.selection()
        if item_id:
            item = self.tree.item(item_id)
            valores = item['values']
            if valores:
                self._editar_cliente(valores[0])

    def _eliminar_seleccionado(self):
        """Eliminar cliente seleccionado"""
        item_id = self.tree.selection()
        if not item_id:
            return
            
        item = self.tree.item(item_id)
        valores = item['values']
        if not valores:
            return
            
        id_cliente = valores[0]
        nombre = valores[1]
        
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar al cliente '{nombre}'?\\nEsta acción no se puede deshacer."
        )
        
        if confirmacion:
            exito = self.controller.eliminar_cliente(id_cliente)
            if exito:
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self._cargar_datos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente")


class ClienteDialog(tk.Toplevel):
    """Diálogo para agregar/editar cliente"""
    
    def __init__(self, parent, app, titulo, cliente=None):
        super().__init__(parent)
        self.app = app
        self.cliente = cliente
        self.resultado = None
        
        self.title(titulo)
        self.geometry("400x600")
        self.configure(bg=app.COLOR_FONDO_EXTERIOR)
        self.resizable(True, True)
        
        # Hacer modal
        self.transient(parent)
        self.grab_set()
        
        self._construir_ui()
        
        # Centrar ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def _construir_ui(self):
        # Registrar validaciones
        vcmd_entero = (self.register(self._validar_entero), '%P')
        vcmd_decimal = (self.register(self._validar_decimal), '%P')

        frame = tk.Frame(self, bg=self.app.COLOR_FONDO_INTERIOR, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Nombre
        tk.Label(frame, text="Nombre:", font=("Arial", 10), 
                bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w", pady=(5,0))
        self.nombre_var = tk.StringVar(value=self.cliente.get('nombre_raw', '') if self.cliente else "")
        tk.Entry(frame, textvariable=self.nombre_var, font=("Arial", 10)).pack(fill=tk.X, pady=(0,5))
        
        # Apellido Paterno
        tk.Label(frame, text="Apellido Paterno:", font=("Arial", 10), 
                bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w", pady=(5,0))
        self.apellido_p_var = tk.StringVar(value=self.cliente.get('apellido_paterno', '') if self.cliente else "")
        tk.Entry(frame, textvariable=self.apellido_p_var, font=("Arial", 10)).pack(fill=tk.X, pady=(0,5))
        
        # Apellido Materno
        tk.Label(frame, text="Apellido Materno (opcional):", font=("Arial", 10), 
                bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w", pady=(5,0))
        self.apellido_m_var = tk.StringVar(value=self.cliente.get('apellido_materno', '') if self.cliente else "")
        tk.Entry(frame, textvariable=self.apellido_m_var, font=("Arial", 10)).pack(fill=tk.X, pady=(0,5))
        
        # Teléfono
        tk.Label(frame, text="Teléfono:", font=("Arial", 10), 
                bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w", pady=(5,0))
        self.telefono_var = tk.StringVar(value=self.cliente['telefono'] if self.cliente else "")
        tk.Entry(
            frame, 
            textvariable=self.telefono_var, 
            font=("Arial", 10),
            validate="key",
            validatecommand=vcmd_entero
        ).pack(fill=tk.X, pady=(0,5))
        
        # Dirección
        tk.Label(frame, text="Dirección (opcional):", font=("Arial", 10), 
                bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w", pady=(5,0))
        self.direccion_var = tk.StringVar(value=self.cliente['direccion'] if self.cliente else "")
        tk.Entry(frame, textvariable=self.direccion_var, font=("Arial", 10)).pack(fill=tk.X, pady=(0,5))
        
        # Descuento
        tk.Label(frame, text="Descuento (%):", font=("Arial", 10), 
                bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w", pady=(5,0))
        self.descuento_var = tk.StringVar(value=str(self.cliente['descuento_pct']) if self.cliente else "0")
        tk.Entry(
            frame, 
            textvariable=self.descuento_var, 
            font=("Arial", 10),
            validate="key",
            validatecommand=vcmd_decimal
        ).pack(fill=tk.X, pady=(0,5))
        
        # Descripción
        tk.Label(frame, text="Descripción (opcional):", font=("Arial", 10), 
                bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w", pady=(5,0))
        self.descripcion_var = tk.StringVar(value=self.cliente['descripcion'] if self.cliente else "")
        tk.Entry(frame, textvariable=self.descripcion_var, font=("Arial", 10)).pack(fill=tk.X, pady=(0,10))
        
        # Botones
        botones_frame = tk.Frame(frame, bg=self.app.COLOR_FONDO_INTERIOR)
        botones_frame.pack(fill=tk.X, pady=(10,0))
        
        tk.Button(
            botones_frame,
            text="Guardar",
            font=("Arial", 10, "bold"),
            bg=self.app.COLOR_BOTON_FONDO,
            fg=self.app.COLOR_BOTON_TEXTO,
            relief=tk.FLAT,
            padx=20,
            pady=5,
            command=self._guardar
        ).pack(side=tk.RIGHT, padx=(5,0))
        
        tk.Button(
            botones_frame,
            text="Cancelar",
            font=("Arial", 10),
            bg="#CCCCCC",
            fg="#000000",
            relief=tk.FLAT,
            padx=20,
            pady=5,
            command=self.destroy
        ).pack(side=tk.RIGHT)
    
    def _validar_entero(self, new_value):
        if new_value == "": return True
        return new_value.isdigit()

    def _validar_decimal(self, new_value):
        if new_value == "": return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False
    
    def _guardar(self):
        """Validar y guardar datos"""
        nombre = self.nombre_var.get().strip()
        apellido_p = self.apellido_p_var.get().strip()
        telefono = self.telefono_var.get().strip()
        
        if not nombre or not apellido_p or not telefono:
            messagebox.showerror("Error", "Nombre, Apellido Paterno y Teléfono son obligatorios")
            return
        
        try:
            descuento = float(self.descuento_var.get())
            if descuento < 0 or descuento > 100:
                messagebox.showerror("Error", "El descuento debe estar entre 0 y 100")
                return
        except ValueError:
            messagebox.showerror("Error", "El descuento debe ser un número")
            return
        
        self.resultado = {
            'nombre': nombre,
            'apellido_paterno': apellido_p,
            'apellido_materno': self.apellido_m_var.get().strip() or None,
            'telefono': telefono,
            'direccion': self.direccion_var.get().strip() or None,
            'descuento': descuento,
            'descripcion': self.descripcion_var.get().strip() or None
        }
        
        self.destroy()
