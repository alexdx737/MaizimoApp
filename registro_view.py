import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from models.empleado_model import EmpleadoModel
from models.usuario_model import UsuarioModel

# Importar tema y componentes personalizados
from utils.theme import COLORS, FONTS, DIMENSIONS
from utils.components import RoundedButton, RoundedEntry

class RegistroView:
    def __init__(self, root):
        self.root = root
        self.root.title("Maizimo App - Registro de Usuario")
        
        # Configuración de ventana
        window_width = 1024
        window_height = 768
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Centrar ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        root.configure(bg=COLORS["background_main"])
        
        # Configurar estilos ttk para Combobox y Radiobutton
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=COLORS["background_card"], background=COLORS["background_card"])
        
        # Crear frame principal con scroll pero con estilo "Tarjeta" sobre fondo crema
        self.main_container = tk.Frame(root, bg=COLORS["background_main"])
        self.main_container.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Tarjeta blanca central
        self.card_frame = tk.Frame(self.main_container, bg=COLORS["background_card"], padx=2, pady=2)
        self.card_frame.pack(fill="both", expand=True)
        
        # Canvas y scrollbar para el contenido dentro de la tarjeta
        self.canvas = tk.Canvas(self.card_frame, bg=COLORS["background_card"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.card_frame, orient="vertical", command=self.canvas.yview)
        
        # Frame scrollable
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS["background_card"], padx=60, pady=40)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Guardar ID de la ventana en el canvas para moverla después
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Habilitar scroll con mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Evento para mantener centrado
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        self.crear_widgets()
    
    def _on_canvas_configure(self, event):
        """Centrar el frame dentro del canvas y ajustar scrollregion"""
        # Ancho del canvas
        canvas_width = event.width
        # Mover la ventana al centro
        self.canvas.coords(self.canvas_window, canvas_width // 2, 20) # 20px padding top
        # Actualizar región de scroll
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _validar_curp(self, new_value):
        """Valida longitud máxima del CURP"""
        if len(new_value) > 18:
            return False
        return True
    
    def crear_widgets(self):
        row = 0
        
        # --- Título ---
        tk.Label(self.scrollable_frame, text="Registro de Nuevo Usuario", 
                 font=("Segoe UI", 24, "bold"), fg=COLORS["text_primary"], 
                 bg=COLORS["background_card"]).grid(row=row, column=0, columnspan=2, pady=(0, 5))
        row += 1
        
        tk.Label(self.scrollable_frame, text="Complete todos los campos requeridos (*)", 
                 font=("Segoe UI", 10), fg=COLORS["text_secondary"], 
                 bg=COLORS["background_card"]).grid(row=row, column=0, columnspan=2, pady=(0, 30))
        row += 1
        
        # --- SECCIÓN: Datos del Empleado ---
        tk.Label(self.scrollable_frame, text="DATOS DEL EMPLEADO", 
                 font=("Segoe UI", 14, "bold"), fg=COLORS["primary"], 
                 bg=COLORS["background_card"]).grid(row=row, column=0, columnspan=2, pady=(10, 15), sticky="w")
        row += 1
        
        input_width = 800 # Ancho total para inputs

        # Nombre *
        tk.Label(self.scrollable_frame, text="Nombre *", anchor="w", 
                 font=("Segoe UI", 10, "bold"), fg=COLORS["text_primary"], 
                 bg=COLORS["background_card"]).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.nombre_entry = RoundedEntry(self.scrollable_frame, width=input_width, height=45)
        self.nombre_entry.grid(row=row, column=0, columnspan=2, pady=(2, 15)) # Usar grid directamente en canvas/widget mix
        row += 1
        
        # Apellido Paterno *
        tk.Label(self.scrollable_frame, text="Apellido Paterno *", anchor="w", 
                 font=("Segoe UI", 10, "bold"), fg=COLORS["text_primary"], 
                 bg=COLORS["background_card"]).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.apellido_paterno_entry = RoundedEntry(self.scrollable_frame, width=input_width, height=45)
        self.apellido_paterno_entry.grid(row=row, column=0, columnspan=2, pady=(2, 15))
        row += 1
        
        # Apellido Materno
        tk.Label(self.scrollable_frame, text="Apellido Materno", anchor="w", 
                 font=("Segoe UI", 10, "bold"), fg=COLORS["text_primary"], 
                 bg=COLORS["background_card"]).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.apellido_materno_entry = RoundedEntry(self.scrollable_frame, width=input_width, height=45)
        self.apellido_materno_entry.grid(row=row, column=0, columnspan=2, pady=(2, 15))
        row += 1
        
        # CURP *
        tk.Label(self.scrollable_frame, text="CURP * (18 caracteres)", anchor="w", 
                 font=("Segoe UI", 10, "bold"), fg=COLORS["text_primary"], 
                 bg=COLORS["background_card"]).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        
        # Para validación en RoundedEntry necesitaríamos exponer el validatecommand
        # Simplificación: RoundedEntry no soporta native validation fácilmente sin exponer entry.
        # Vamos a usar RoundedEntry pero la validación será manual al guardar o accediendo al entry interno.
        # Sin embargo, para limitar longitud, accedemos al entry interno.
        self.curp_entry = RoundedEntry(self.scrollable_frame, width=input_width, height=45)
        vcmd_curp = (self.root.register(self._validar_curp), '%P')
        self.curp_entry.entry.config(validate="key", validatecommand=vcmd_curp) # Acceso directo al entry interno
        self.curp_entry.grid(row=row, column=0, columnspan=2, pady=(2, 15))
        row += 1
        
        # Fecha de Ingreso *
        tk.Label(self.scrollable_frame, text="Fecha de Ingreso *", anchor="w", 
                 font=("Segoe UI", 10, "bold"), fg=COLORS["text_primary"], 
                 bg=COLORS["background_card"]).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        
        fecha_frame = tk.Frame(self.scrollable_frame, bg=COLORS["background_card"])
        fecha_frame.grid(row=row, column=0, columnspan=2, pady=(2, 15), sticky="w")
        
        # Día
        tk.Label(fecha_frame, text="Día:", bg=COLORS["background_card"], font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 5))
        self.dia_combo = ttk.Combobox(fecha_frame, values=[str(i) for i in range(1, 32)], state="readonly", width=5, font=("Segoe UI", 10))
        self.dia_combo.set(datetime.now().day)
        self.dia_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        # Mes
        tk.Label(fecha_frame, text="Mes:", bg=COLORS["background_card"], font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 5))
        self.mes_combo = ttk.Combobox(fecha_frame, values=[str(i) for i in range(1, 13)], state="readonly", width=5, font=("Segoe UI", 10))
        self.mes_combo.set(datetime.now().month)
        self.mes_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        # Año
        tk.Label(fecha_frame, text="Año:", bg=COLORS["background_card"], font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 5))
        self.anio_combo = ttk.Combobox(fecha_frame, values=[str(i) for i in range(1960, 2026)], state="readonly", width=10, font=("Segoe UI", 10))
        self.anio_combo.set(datetime.now().year)
        self.anio_combo.pack(side=tk.LEFT)
        row += 1
        
        # Ciclo *
        tk.Label(self.scrollable_frame, text="Ciclo *", anchor="w", 
                 font=("Segoe UI", 10, "bold"), fg=COLORS["text_primary"], 
                 bg=COLORS["background_card"]).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.ciclo_var = tk.StringVar(value="espera")
        ciclo_frame = tk.Frame(self.scrollable_frame, bg=COLORS["background_card"])
        ciclo_frame.grid(row=row, column=0, columnspan=2, pady=(2, 15), sticky="w")
        
        # Estilo para Radiobuttons (simple)
        tk.Radiobutton(ciclo_frame, text="Espera", variable=self.ciclo_var, value="espera", 
                      bg=COLORS["background_card"], activebackground=COLORS["background_card"], font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(0, 15))
        tk.Radiobutton(ciclo_frame, text="Proceso", variable=self.ciclo_var, value="proceso", 
                      bg=COLORS["background_card"], activebackground=COLORS["background_card"], font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(0, 15))
        tk.Radiobutton(ciclo_frame, text="Finalizado", variable=self.ciclo_var, value="finalizado", 
                      bg=COLORS["background_card"], activebackground=COLORS["background_card"], font=("Segoe UI", 10)).pack(side=tk.LEFT)
        row += 1
        
        # Vulnerable
        self.vulnerable_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.scrollable_frame, text="Empleado Vulnerable", variable=self.vulnerable_var,
                      bg=COLORS["background_card"], activebackground=COLORS["background_card"], font=("Segoe UI", 10)).grid(row=row, column=0, columnspan=2, pady=(5, 15), sticky="w")
        row += 1
        
        # Descripción
        tk.Label(self.scrollable_frame, text="Descripción (opcional)", anchor="w", 
                 font=("Segoe UI", 10, "bold"), fg=COLORS["text_primary"], 
                 bg=COLORS["background_card"]).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.descripcion_empleado_entry = RoundedEntry(self.scrollable_frame, width=input_width, height=45)
        self.descripcion_empleado_entry.grid(row=row, column=0, columnspan=2, pady=(2, 25))
        row += 1
        
        # --- SECCIÓN: Datos del Usuario ---
        tk.Label(self.scrollable_frame, text="DATOS DE USUARIO", 
                 font=("Segoe UI", 14, "bold"), fg=COLORS["primary"], 
                 bg=COLORS["background_card"]).grid(row=row, column=0, columnspan=2, pady=(10, 15), sticky="w")
        row += 1
        
        # Rol *
        tk.Label(self.scrollable_frame, text="Rol *", anchor="w", 
                 font=("Segoe UI", 10, "bold"), fg=COLORS["text_primary"], 
                 bg=COLORS["background_card"]).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.rol_var = tk.StringVar(value="trabajador")
        rol_frame = tk.Frame(self.scrollable_frame, bg=COLORS["background_card"])
        rol_frame.grid(row=row, column=0, columnspan=2, pady=(2, 20), sticky="w")
        
        tk.Radiobutton(rol_frame, text="Trabajador", variable=self.rol_var, value="trabajador", 
                      bg=COLORS["background_card"], activebackground=COLORS["background_card"], font=("Segoe UI", 10), command=self._actualizar_campos_usuario).pack(side=tk.LEFT, padx=(0, 15))
        tk.Radiobutton(rol_frame, text="Administrador", variable=self.rol_var, value="administrador", 
                      bg=COLORS["background_card"], activebackground=COLORS["background_card"], font=("Segoe UI", 10), command=self._actualizar_campos_usuario).pack(side=tk.LEFT)
        row += 1

        # Contraseña *
        tk.Label(self.scrollable_frame, text="Contraseña * (máximo 50 caracteres)", anchor="w", 
                 font=("Segoe UI", 10, "bold"), fg=COLORS["text_primary"], 
                 bg=COLORS["background_card"]).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.password_entry = RoundedEntry(self.scrollable_frame, width=input_width, height=45, show="*", icon="🔒")
        self.password_entry.grid(row=row, column=0, columnspan=2, pady=(2, 15))
        row += 1
        
        # Confirmar Contraseña *
        tk.Label(self.scrollable_frame, text="Confirmar Contraseña *", anchor="w", 
                 font=("Segoe UI", 10, "bold"), fg=COLORS["text_primary"], 
                 bg=COLORS["background_card"]).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.confirm_password_entry = RoundedEntry(self.scrollable_frame, width=input_width, height=45, show="*", icon="🔒")
        self.confirm_password_entry.grid(row=row, column=0, columnspan=2, pady=(2, 15))
        row += 1
        
        # --- BOTONES ---
        button_frame = tk.Frame(self.scrollable_frame, bg=COLORS["background_card"])
        button_frame.grid(row=row, column=0, columnspan=2, pady=(30, 20))
        
        # Usar RoundedButton
        self.btn_registrar = RoundedButton(button_frame, text="Registrar Usuario", command=self.registrar_usuario,
                                        width=250, height=45, bg_color=COLORS["primary"], text_color=COLORS["primary_text"],
                                        hover_color=COLORS["primary_hover"])
        self.btn_registrar.pack(side=tk.LEFT, padx=10)
        
        self.btn_volver = RoundedButton(button_frame, text="Volver al Login", command=self.volver_login,
                                     width=250, height=45, bg_color="#666666", text_color="white",
                                     hover_color="#555555")
        self.btn_volver.pack(side=tk.LEFT, padx=10)
        
        # Inicializar estado de campos
        self._actualizar_campos_usuario()
    
    def _actualizar_campos_usuario(self):
        """Habilitar o deshabilitar campos de usuario según el rol"""
        rol = self.rol_var.get()
        if rol == "trabajador":
            # Deshabilitar y limpiar campos
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(state="disabled")
            self.confirm_password_entry.delete(0, tk.END)
            self.confirm_password_entry.config(state="disabled")
        else:
            # Habilitar campos
            self.password_entry.config(state="normal")
            self.confirm_password_entry.config(state="normal")
    
    def validar_campos(self):
        """Validar todos los campos del formulario"""
        # Validar campos requeridos de empleado
        if not self.nombre_entry.get().strip():
            messagebox.showerror("Error", "El nombre es requerido")
            return False
        
        if not self.apellido_paterno_entry.get().strip():
            messagebox.showerror("Error", "El apellido paterno es requerido")
            return False
        
        # Validar CURP
        curp = self.curp_entry.get().strip()
        if not curp:
            messagebox.showerror("Error", "El CURP es requerido")
            return False
        
        if len(curp) != 18:
            messagebox.showerror("Error", "El CURP debe tener exactamente 18 caracteres")
            return False
        
        # Validar fecha de ingreso
        dia = self.dia_combo.get()
        mes = self.mes_combo.get()
        anio = self.anio_combo.get()
        
        if not (dia and mes and anio):
            messagebox.showerror("Error", "Debe seleccionar Día, Mes y Año de ingreso")
            return False
            
        try:
            # Validar que sea una fecha real
            fecha_str = f"{anio}-{mes.zfill(2)}-{dia.zfill(2)}"
            datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Fecha inválida (ej. 30 de Febrero)")
            return False
        
        # Validar contraseña solo si es administrador
        rol = self.rol_var.get()
        if rol == "administrador":
            password = self.password_entry.get()
            if not password:
                messagebox.showerror("Error", "La contraseña es requerida para Administradores")
                return False
            
            if len(password) > 50:
                messagebox.showerror("Error", "La contraseña no puede tener más de 50 caracteres")
                return False
            
            # Validar confirmación de contraseña
            confirm_password = self.confirm_password_entry.get()
            if password != confirm_password:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return False
        
        return True
    
    def registrar_usuario(self):
        """Registrar nuevo usuario/empleado en el sistema"""
        if not self.validar_campos():
            return
        
        try:
            # 1. Crear empleado primero
            empleado = EmpleadoModel.crear(
                nombre=self.nombre_entry.get().strip(),
                apellido_paterno=self.apellido_paterno_entry.get().strip(),
                apellido_materno=self.apellido_materno_entry.get().strip() or None,
                curp=self.curp_entry.get().strip().upper(),
                fecha_ingreso=f"{self.anio_combo.get()}-{self.mes_combo.get().zfill(2)}-{self.dia_combo.get().zfill(2)}",
                vulnerable=self.vulnerable_var.get(),
                ciclo=self.ciclo_var.get(),
                descripcion=self.descripcion_empleado_entry.get().strip() or None
            )
            
            if not empleado:
                messagebox.showerror("Error", "No se pudo crear el empleado. Verifique que el CURP no esté duplicado.")
                return
            
            rol = self.rol_var.get()
            
            # 2. Crear usuario SOLO si es administrador
            if rol == "administrador":
                usuario = UsuarioModel.crear_usuario(
                    id_empleado=empleado['id_empleado'],
                    password=self.password_entry.get(),
                    rol=rol,
                    activo=True
                )
                
                if not usuario:
                    messagebox.showerror("Error", "No se pudo crear el usuario administrador")
                    return
                
                # Éxito Administrador
                messagebox.showinfo("Éxito", 
                                  f"Administrador registrado exitosamente!\n\n"
                                  f"ID de Usuario: {usuario['id_usuario']}\n"
                                  f"Nombre: {empleado['nombre']} {empleado['apellido_paterno']}\n"
                                  f"Rol: {usuario['rol']}\n\n"
                                  f"Puede iniciar sesión con su ID de usuario y contraseña.")
            else:
                # Éxito Trabajador (solo empleado)
                messagebox.showinfo("Éxito", 
                                  f"Trabajador registrado exitosamente!\n\n"
                                  f"Nombre: {empleado['nombre']} {empleado['apellido_paterno']}\n"
                                  f"Rol: Trabajador\n\n"
                                  f"El trabajador ha sido registrado en el sistema correctamente.")
            
            # Volver al login
            self.volver_login()
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error durante el registro: {str(e)}")
    
    def volver_login(self):
        """Volver a la pantalla de login"""
        self.root.destroy()
        # Importar aquí para evitar importación circular
        from login_view import LoginView
        root = tk.Tk()
        app = LoginView(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroView(root)
    root.mainloop()
