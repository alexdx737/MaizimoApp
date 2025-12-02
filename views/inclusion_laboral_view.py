import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


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
            command=self._agregar_trabajador
        ).pack(side=tk.RIGHT)

        # Treeview container
        tree_container = tk.Frame(tabla_frame, bg=self.app.COLOR_FONDO_INTERIOR)
        tree_container.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(tree_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columnas = ("id", "nombre", "situacion", "ciclo", "fecha", "acciones")
        self.tree = ttk.Treeview(tree_container, columns=columnas, show="headings", 
                                 height=10, yscrollcommand=scrollbar.set,
                                 displaycolumns=("nombre", "situacion", "ciclo", "fecha", "acciones"))
        
        scrollbar.config(command=self.tree.yview)
        
        titulos = [
            "Nombre",
            "Situación de Vulnerabilidad",
            "Ciclo de Trabajo",
            "Fecha de Inicio",
            "Acciones",
        ]
        columnas_display = ("nombre", "situacion", "ciclo", "fecha", "acciones")
        for col, texto in zip(columnas_display, titulos):
            self.tree.heading(col, text=texto)
            self.tree.column(col, anchor="center", width=170)

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
        
        # Cargar trabajadores
        for trabajador in self.controller.trabajadores:
            self.tree.insert("", tk.END, values=(
                trabajador['id'],
                trabajador['nombre'],
                trabajador['situacion'],
                trabajador['ciclo'],
                trabajador['fecha'],
                "✏ 🗑"
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
        
        id_empleado = valores[0]
        self._editar_trabajador(id_empleado)
    
    def _agregar_trabajador(self):
        """Mostrar diálogo para agregar trabajador"""
        dialog = TrabajadorDialog(self, self.app, "Agregar Trabajador")
        dialog.wait_window()
        
        if dialog.resultado:
            datos = dialog.resultado
            exito = self.controller.agregar_trabajador(
                nombre=datos['nombre'],
                apellido_paterno=datos['apellido_paterno'],
                curp=datos['curp'],
                fecha_ingreso=datos['fecha_ingreso'],
                apellido_materno=datos.get('apellido_materno'),
                descripcion=datos.get('descripcion'),
                ciclo=datos.get('ciclo', 'espera')
            )
            
            if exito:
                messagebox.showinfo("Éxito", "Trabajador agregado correctamente")
                self._cargar_datos()
            else:
                messagebox.showerror("Error", "No se pudo agregar el trabajador")
    
    def _editar_trabajador(self, id_empleado):
        """Mostrar diálogo para editar trabajador"""
        trabajador = self.controller.obtener_trabajador(id_empleado)
        if not trabajador:
            return
        
        dialog = TrabajadorDialog(self, self.app, "Editar Trabajador", trabajador)
        dialog.wait_window()
        
        if dialog.resultado:
            datos = dialog.resultado
            exito = self.controller.actualizar_trabajador(
                id_empleado=id_empleado,
                nombre=datos['nombre'],
                apellido_paterno=datos['apellido_paterno'],
                apellido_materno=datos.get('apellido_materno'),
                curp=datos['curp'],
                fecha_ingreso=datos['fecha_ingreso'],
                descripcion=datos.get('descripcion'),
                ciclo=datos.get('ciclo', 'espera')
            )
            
            if exito:
                messagebox.showinfo("Éxito", "Trabajador actualizado correctamente")
                self._cargar_datos()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el trabajador")

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
                self._editar_trabajador(valores[0])

    def _eliminar_seleccionado(self):
        """Eliminar trabajador seleccionado"""
        item_id = self.tree.selection()
        if not item_id:
            return
            
        item = self.tree.item(item_id)
        valores = item['values']
        if not valores:
            return
            
        id_empleado = valores[0]
        nombre = valores[1]
        
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar al trabajador '{nombre}'?\\nEsta acción no se puede deshacer."
        )
        
        if confirmacion:
            exito = self.controller.eliminar_trabajador(id_empleado)
            if exito:
                messagebox.showinfo("Éxito", "Trabajador eliminado correctamente")
                self._cargar_datos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el trabajador")


class TrabajadorDialog(tk.Toplevel):
    """Diálogo para agregar/editar trabajador"""
    
    def __init__(self, parent, app, titulo, trabajador=None):
        super().__init__(parent)
        self.app = app
        self.trabajador = trabajador
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
        frame = tk.Frame(self, bg=self.app.COLOR_FONDO_INTERIOR, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Nombre
        tk.Label(frame, text="Nombre:", font=("Arial", 10), 
                bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w", pady=(5,0))
        self.nombre_var = tk.StringVar(value=self.trabajador['nombre_raw'] if self.trabajador else "")
        tk.Entry(frame, textvariable=self.nombre_var, font=("Arial", 10)).pack(fill=tk.X, pady=(0,5))
        
        # Apellido Paterno
        tk.Label(frame, text="Apellido Paterno:", font=("Arial", 10), 
                bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w", pady=(5,0))
        self.apellido_p_var = tk.StringVar(value=self.trabajador['apellido_paterno'] if self.trabajador else "")
        tk.Entry(frame, textvariable=self.apellido_p_var, font=("Arial", 10)).pack(fill=tk.X, pady=(0,5))
        
        # Apellido Materno
        tk.Label(frame, text="Apellido Materno (opcional):", font=("Arial", 10), 
                bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w", pady=(5,0))
        self.apellido_m_var = tk.StringVar(value=self.trabajador['apellido_materno'] if self.trabajador else "")
        tk.Entry(frame, textvariable=self.apellido_m_var, font=("Arial", 10)).pack(fill=tk.X, pady=(0,5))
        
        # CURP
        tk.Label(frame, text="CURP:", font=("Arial", 10), 
                bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w", pady=(5,0))
        self.curp_var = tk.StringVar(value=self.trabajador['curp'] if self.trabajador else "")
        tk.Entry(frame, textvariable=self.curp_var, font=("Arial", 10)).pack(fill=tk.X, pady=(0,5))
        
        # Fecha de Ingreso
        tk.Label(frame, text="Fecha de Ingreso (YYYY-MM-DD):", font=("Arial", 10), 
                bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w", pady=(5,0))
        fecha_default = self.trabajador['fecha'] if self.trabajador else datetime.now().strftime("%Y-%m-%d")
        self.fecha_var = tk.StringVar(value=fecha_default)
        tk.Entry(frame, textvariable=self.fecha_var, font=("Arial", 10)).pack(fill=tk.X, pady=(0,5))
        
        # Ciclo
        tk.Label(frame, text="Ciclo de Trabajo:", font=("Arial", 10), 
                bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w", pady=(5,0))
        self.ciclo_var = tk.StringVar(value=self.trabajador['ciclo_raw'] if self.trabajador else "espera")
        ciclo_combo = ttk.Combobox(frame, textvariable=self.ciclo_var, 
                                    values=["espera", "proceso", "finalizado"],
                                    state="readonly", font=("Arial", 10))
        ciclo_combo.pack(fill=tk.X, pady=(0,5))
        
        # Situación de Vulnerabilidad
        tk.Label(frame, text="Situación de Vulnerabilidad:", font=("Arial", 10), 
                bg=self.app.COLOR_FONDO_INTERIOR, fg=self.app.COLOR_TEXTO_PRIMARIO).pack(anchor="w", pady=(5,0))
        self.descripcion_var = tk.StringVar(value=self.trabajador['situacion'] if self.trabajador else "")
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
    
    def _guardar(self):
        """Validar y guardar datos"""
        nombre = self.nombre_var.get().strip()
        apellido_p = self.apellido_p_var.get().strip()
        curp = self.curp_var.get().strip()
        fecha = self.fecha_var.get().strip()
        
        if not nombre or not apellido_p or not curp or not fecha:
            messagebox.showerror("Error", "Nombre, Apellido Paterno, CURP y Fecha son obligatorios")
            return
        
        # Validar formato de fecha
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
            return
        
        self.resultado = {
            'nombre': nombre,
            'apellido_paterno': apellido_p,
            'apellido_materno': self.apellido_m_var.get().strip() or None,
            'curp': curp,
            'fecha_ingreso': fecha,
            'ciclo': self.ciclo_var.get(),
            'descripcion': self.descripcion_var.get().strip() or None
        }
        
        self.destroy()
