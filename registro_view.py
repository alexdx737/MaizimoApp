import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from models.empleado_model import EmpleadoModel
from models.usuario_model import UsuarioModel

# Colores globales (consistentes con login_view)
COLOR_TEXTO_PRIMARIO = "#333333"
COLOR_BOTON_FONDO = "#FDB813"
COLOR_BOTON_TEXTO = "white"
COLOR_FONDO_EXTERIOR = "#f0f0f0"
COLOR_FONDO_INTERIOR = "#ffffff"

class RegistroView:
    def __init__(self, root):
        self.root = root
        self.root.title("Maizimo App - Registro de Usuario")
        
        # Definir colores de instancia
        self.COLOR_TEXTO_PRIMARIO = COLOR_TEXTO_PRIMARIO
        self.COLOR_BOTON_FONDO = COLOR_BOTON_FONDO
        self.COLOR_BOTON_TEXTO = COLOR_BOTON_TEXTO
        self.COLOR_FONDO_EXTERIOR = COLOR_FONDO_EXTERIOR
        self.COLOR_FONDO_INTERIOR = COLOR_FONDO_INTERIOR
        
        # Configuración de ventana
        window_width = 1024
        window_height = 768
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.configure(bg=self.COLOR_FONDO_EXTERIOR)
        
        # Frame principal con scroll
        self.main_frame = tk.Frame(root, bg=self.COLOR_FONDO_EXTERIOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para scroll
        self.canvas = tk.Canvas(self.main_frame, bg=self.COLOR_FONDO_EXTERIOR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.COLOR_FONDO_INTERIOR, padx=40, pady=30)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((window_width//2, 0), window=self.scrollable_frame, anchor="n")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Habilitar scroll con mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        self.crear_widgets()
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def crear_widgets(self):
        row = 0
        
        # --- Título ---
        tk.Label(self.scrollable_frame, text="Registro de Nuevo Usuario", 
                 font=("Arial", 24, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=row, column=0, columnspan=2, pady=(0, 5))
        row += 1
        
        tk.Label(self.scrollable_frame, text="Complete todos los campos requeridos (*)", 
                 font=("Arial", 10), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=row, column=0, columnspan=2, pady=(0, 20))
        row += 1
        
        # --- SECCIÓN: Datos del Empleado ---
        tk.Label(self.scrollable_frame, text="DATOS DEL EMPLEADO", 
                 font=("Arial", 14, "bold"), fg=self.COLOR_BOTON_FONDO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=row, column=0, columnspan=2, pady=(10, 10), sticky="w")
        row += 1
        
        # Nombre *
        tk.Label(self.scrollable_frame, text="Nombre *", anchor="w", 
                 font=("Arial", 11, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.nombre_entry = tk.Entry(self.scrollable_frame, width=50, font=("Arial", 11), bd=1, relief=tk.FLAT)
        self.nombre_entry.grid(row=row, column=0, columnspan=2, pady=(2, 10), ipady=5, sticky="ew")
        row += 1
        
        # Apellido Paterno *
        tk.Label(self.scrollable_frame, text="Apellido Paterno *", anchor="w", 
                 font=("Arial", 11, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.apellido_paterno_entry = tk.Entry(self.scrollable_frame, width=50, font=("Arial", 11), bd=1, relief=tk.FLAT)
        self.apellido_paterno_entry.grid(row=row, column=0, columnspan=2, pady=(2, 10), ipady=5, sticky="ew")
        row += 1
        
        # Apellido Materno
        tk.Label(self.scrollable_frame, text="Apellido Materno", anchor="w", 
                 font=("Arial", 11, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.apellido_materno_entry = tk.Entry(self.scrollable_frame, width=50, font=("Arial", 11), bd=1, relief=tk.FLAT)
        self.apellido_materno_entry.grid(row=row, column=0, columnspan=2, pady=(2, 10), ipady=5, sticky="ew")
        row += 1
        
        # CURP *
        tk.Label(self.scrollable_frame, text="CURP * (18 caracteres)", anchor="w", 
                 font=("Arial", 11, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.curp_entry = tk.Entry(self.scrollable_frame, width=50, font=("Arial", 11), bd=1, relief=tk.FLAT)
        self.curp_entry.grid(row=row, column=0, columnspan=2, pady=(2, 10), ipady=5, sticky="ew")
        row += 1
        
        # Fecha de Ingreso *
        tk.Label(self.scrollable_frame, text="Fecha de Ingreso * (YYYY-MM-DD)", anchor="w", 
                 font=("Arial", 11, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.fecha_ingreso_entry = tk.Entry(self.scrollable_frame, width=50, font=("Arial", 11), bd=1, relief=tk.FLAT)
        self.fecha_ingreso_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.fecha_ingreso_entry.grid(row=row, column=0, columnspan=2, pady=(2, 10), ipady=5, sticky="ew")
        row += 1
        
        # Ciclo *
        tk.Label(self.scrollable_frame, text="Ciclo *", anchor="w", 
                 font=("Arial", 11, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.ciclo_var = tk.StringVar(value="espera")
        ciclo_frame = tk.Frame(self.scrollable_frame, bg=self.COLOR_FONDO_INTERIOR)
        ciclo_frame.grid(row=row, column=0, columnspan=2, pady=(2, 10), sticky="w")
        tk.Radiobutton(ciclo_frame, text="Espera", variable=self.ciclo_var, value="espera", 
                      bg=self.COLOR_FONDO_INTERIOR, font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 15))
        tk.Radiobutton(ciclo_frame, text="Proceso", variable=self.ciclo_var, value="proceso", 
                      bg=self.COLOR_FONDO_INTERIOR, font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 15))
        tk.Radiobutton(ciclo_frame, text="Finalizado", variable=self.ciclo_var, value="finalizado", 
                      bg=self.COLOR_FONDO_INTERIOR, font=("Arial", 10)).pack(side=tk.LEFT)
        row += 1
        
        # Vulnerable
        self.vulnerable_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.scrollable_frame, text="Empleado Vulnerable", variable=self.vulnerable_var,
                      bg=self.COLOR_FONDO_INTERIOR, font=("Arial", 11)).grid(row=row, column=0, columnspan=2, pady=(5, 10), sticky="w")
        row += 1
        
        # Descripción
        tk.Label(self.scrollable_frame, text="Descripción (opcional)", anchor="w", 
                 font=("Arial", 11, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.descripcion_empleado_entry = tk.Entry(self.scrollable_frame, width=50, font=("Arial", 11), bd=1, relief=tk.FLAT)
        self.descripcion_empleado_entry.grid(row=row, column=0, columnspan=2, pady=(2, 20), ipady=5, sticky="ew")
        row += 1
        
        # --- SECCIÓN: Datos del Usuario ---
        tk.Label(self.scrollable_frame, text="DATOS DE USUARIO", 
                 font=("Arial", 14, "bold"), fg=self.COLOR_BOTON_FONDO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=row, column=0, columnspan=2, pady=(10, 10), sticky="w")
        row += 1
        
        # Contraseña *
        tk.Label(self.scrollable_frame, text="Contraseña * (máximo 50 caracteres)", anchor="w", 
                 font=("Arial", 11, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.password_entry = tk.Entry(self.scrollable_frame, width=50, font=("Arial", 11), show="*", bd=1, relief=tk.FLAT)
        self.password_entry.grid(row=row, column=0, columnspan=2, pady=(2, 10), ipady=5, sticky="ew")
        row += 1
        
        # Confirmar Contraseña *
        tk.Label(self.scrollable_frame, text="Confirmar Contraseña *", anchor="w", 
                 font=("Arial", 11, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.confirm_password_entry = tk.Entry(self.scrollable_frame, width=50, font=("Arial", 11), show="*", bd=1, relief=tk.FLAT)
        self.confirm_password_entry.grid(row=row, column=0, columnspan=2, pady=(2, 10), ipady=5, sticky="ew")
        row += 1
        
        # Rol *
        tk.Label(self.scrollable_frame, text="Rol *", anchor="w", 
                 font=("Arial", 11, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=row, column=0, columnspan=2, sticky="w", pady=(5, 0))
        row += 1
        self.rol_var = tk.StringVar(value="trabajador")
        rol_frame = tk.Frame(self.scrollable_frame, bg=self.COLOR_FONDO_INTERIOR)
        rol_frame.grid(row=row, column=0, columnspan=2, pady=(2, 20), sticky="w")
        tk.Radiobutton(rol_frame, text="Trabajador", variable=self.rol_var, value="trabajador", 
                      bg=self.COLOR_FONDO_INTERIOR, font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 15))
        tk.Radiobutton(rol_frame, text="Administrador", variable=self.rol_var, value="administrador", 
                      bg=self.COLOR_FONDO_INTERIOR, font=("Arial", 10)).pack(side=tk.LEFT)
        row += 1
        
        # --- Botones ---
        button_frame = tk.Frame(self.scrollable_frame, bg=self.COLOR_FONDO_INTERIOR)
        button_frame.grid(row=row, column=0, columnspan=2, pady=(20, 10))
        
        tk.Button(button_frame, text="Registrarse", command=self.registrar_usuario,
                  bg=self.COLOR_BOTON_FONDO, fg=self.COLOR_BOTON_TEXTO,
                  font=("Arial", 12, "bold"), width=20, height=1, bd=0, relief=tk.FLAT,
                  activebackground="#D39210", activeforeground=self.COLOR_BOTON_TEXTO).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Volver al Login", command=self.volver_login,
                  bg="#666666", fg="white",
                  font=("Arial", 12, "bold"), width=20, height=1, bd=0, relief=tk.FLAT,
                  activebackground="#555555", activeforeground="white").pack(side=tk.LEFT, padx=5)
    
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
        fecha_ingreso = self.fecha_ingreso_entry.get().strip()
        if not fecha_ingreso:
            messagebox.showerror("Error", "La fecha de ingreso es requerida")
            return False
        
        try:
            datetime.strptime(fecha_ingreso, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
            return False
        
        # Validar contraseña
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "La contraseña es requerida")
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
        """Registrar nuevo usuario en el sistema"""
        if not self.validar_campos():
            return
        
        try:
            # 1. Crear empleado primero
            empleado = EmpleadoModel.crear(
                nombre=self.nombre_entry.get().strip(),
                apellido_paterno=self.apellido_paterno_entry.get().strip(),
                apellido_materno=self.apellido_materno_entry.get().strip() or None,
                curp=self.curp_entry.get().strip().upper(),
                fecha_ingreso=self.fecha_ingreso_entry.get().strip(),
                vulnerable=self.vulnerable_var.get(),
                ciclo=self.ciclo_var.get(),
                descripcion=self.descripcion_empleado_entry.get().strip() or None
            )
            
            if not empleado:
                messagebox.showerror("Error", "No se pudo crear el empleado. Verifique que el CURP no esté duplicado.")
                return
            
            # 2. Crear usuario con el ID del empleado
            usuario = UsuarioModel.crear_usuario(
                id_empleado=empleado['id_empleado'],
                password=self.password_entry.get(),
                rol=self.rol_var.get(),
                activo=True
            )
            
            if not usuario:
                messagebox.showerror("Error", "No se pudo crear el usuario")
                return
            
            # Éxito
            messagebox.showinfo("Éxito", 
                              f"Usuario registrado exitosamente!\n\n"
                              f"ID de Usuario: {usuario['id_usuario']}\n"
                              f"Nombre: {empleado['nombre']} {empleado['apellido_paterno']}\n"
                              f"Rol: {usuario['rol']}\n\n"
                              f"Puede iniciar sesión con su ID de usuario y contraseña.")
            
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
