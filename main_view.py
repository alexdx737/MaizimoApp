import tkinter as tk
from tkinter import ttk, messagebox

from views.punto_venta_view import PuntoVentaView
from views.gestion_operativa_view import GestionOperativaView
from views.clientes_mayoristas_view import ClientesMayoristasView
from views.responsabilidad_social_view import ResponsabilidadSocialView
from views.inclusion_laboral_view import InclusionLaboralView

from controllers.punto_venta_controller import PuntoVentaController
from controllers.gestion_operativa_controller import GestionOperativaController
from controllers.clientes_mayoristas_controller import ClientesMayoristasController
from controllers.responsabilidad_social_controller import ResponsabilidadSocialController
from controllers.inclusion_laboral_controller import InclusionLaboralController

from utils.theme import COLORS, FONTS, DIMENSIONS

class MainApp:
    def __init__(self, root, usuario_data=None):
        self.root = root
        self.root.title("Maizimo App")
        self.usuario_data = usuario_data or {}

        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.geometry("1200x700")
        
        # Set minimum window size for responsive design
        self.root.minsize(1000, 600)

        self.root.configure(bg=COLORS["background_main"])

        self.seccion_activa = "Punto de Venta"
        self.vista_actual = None

        # Controllers
        self.pv_controller = PuntoVentaController()
        self.go_controller = GestionOperativaController()
        self.cm_controller = ClientesMayoristasController()
        self.rs_controller = ResponsabilidadSocialController()
        self.il_controller = InclusionLaboralController()

        # Configuración de colores para compatibilidad con vistas antiguas
        self.COLOR_FONDO_EXTERIOR = COLORS["background_main"]
        self.COLOR_FONDO_INTERIOR = COLORS["background_card"]
        self.COLOR_TEXTO_PRIMARIO = COLORS["text_primary"]
        self.COLOR_BOTON_FONDO = COLORS["primary"]
        self.COLOR_BOTON_TEXTO = COLORS["primary_text"]

        self._crear_layout_base()
        self.mostrar_punto_venta()

    def _crear_layout_base(self):
        # --- HEADER SUPERIOR ---
        self.header_frame = tk.Frame(self.root, bg=COLORS["background_card"], pady=15, padx=30)
        self.header_frame.pack(fill=tk.X)

        # Contenedor Título (Izquierda)
        titulo_frame = tk.Frame(self.header_frame, bg=COLORS["background_card"])
        titulo_frame.pack(side=tk.LEFT)

        tk.Label(
            titulo_frame,
            text="Maizimo App",
            font=("Segoe UI", 20), # Más grande y fino/moderno
            fg=COLORS["text_primary"],
            bg=COLORS["background_card"],
        ).pack(anchor="w")

        tk.Label(
            titulo_frame,
            text="Sistema de Gestión Integral",
            font=("Segoe UI", 10),
            fg=COLORS["text_secondary"],
            bg=COLORS["background_card"],
        ).pack(anchor="w")

        # Contenedor Perfil (Derecha)
        profile_frame = tk.Frame(self.header_frame, bg=COLORS["background_card"])
        profile_frame.pack(side=tk.RIGHT)
        
        # Icono y Nombre
        # Usamos un frame para alinearlos horizontalmente como en el mockup si se prefiere, 
        # o vertical como estaba. El mockup parece horizontal: Icono Nombre
        
        # Get user name
        nombre_usuario = "Usuario"
        if self.usuario_data and self.usuario_data.get('empleado'):
            empleado = self.usuario_data['empleado']
            nombre_usuario = f"{empleado.get('nombre', '')} {empleado.get('apellido_paterno', '')}"

        self.btn_perfil = tk.Button(
            profile_frame,
            text="👤",  # Icono
            font=("Segoe UI Symbol", 14),
            bg=COLORS["background_card"],
            fg=COLORS["text_primary"],
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self._mostrar_menu_perfil,
            activebackground=COLORS["background_card"]
        )
        self.btn_perfil.pack(side=tk.LEFT, padx=(0, 5))

        tk.Label(
            profile_frame,
            text=nombre_usuario,
            font=("Segoe UI", 11),
            fg=COLORS["text_primary"],
            bg=COLORS["background_card"]
        ).pack(side=tk.LEFT)

        # --- SEPARADOR HEADER ---
        tk.Frame(self.root, bg=COLORS["border"], height=1).pack(fill=tk.X)

        # --- BARRA DE NAVEGACIÓN ---
        self.nav_bar = tk.Frame(self.root, bg=COLORS["background_card"], pady=0, padx=20)
        self.nav_bar.pack(fill=tk.X)

        self.botones_nav_container = tk.Frame(self.nav_bar, bg=COLORS["background_card"])
        self.botones_nav_container.pack(fill=tk.X)

        self.botones_nav = {} # Guardará referencias a (Button, IndicatorFrame)
        secciones = [
            "Punto de Venta",
            "Productos",
            "Clientes",
            "Responsabilidad Social",
            "Inclusión Laboral",
        ]

        # Estilo de pestañas
        for nombre in secciones:
            # Container for each tab (Button + Indicator)
            tab_frame = tk.Frame(self.botones_nav_container, bg=COLORS["background_card"], padx=10)
            tab_frame.pack(side=tk.LEFT)
            
            boton = tk.Button(
                tab_frame,
                text=nombre,
                font=("Segoe UI", 11),
                relief=tk.FLAT,
                bd=0,
                bg=COLORS["background_card"],
                activebackground=COLORS["background_card"],
                cursor="hand2",
                pady=15, # Padding vertical para altura de barra
                command=lambda n=nombre: self.cambiar_seccion(n),
            )
            boton.pack(fill=tk.X)
            
            # Indicator line (hidden by default)
            indicator = tk.Frame(tab_frame, bg=COLORS["background_card"], height=3)
            indicator.pack(fill=tk.X)
            
            self.botones_nav[nombre] = (boton, indicator)

        # --- SEPARADOR NAV ---
        # tk.Frame(self.root, bg=COLORS["border"], height=1).pack(fill=tk.X) 
        # El mockup muestra una línea sutil separando todo el header del contenido:
        tk.Frame(self.root, bg="#E8E8E8", height=2).pack(fill=tk.X) # Sombra sutil o borde

        # --- CONTENIDO PRINCIPAL ---
        self.contenido = tk.Frame(self.root, bg=COLORS["background_main"], padx=20, pady=20)
        self.contenido.pack(fill=tk.BOTH, expand=True)

        self._actualizar_estilos_nav()

    def _actualizar_estilos_nav(self):
        for nombre, (boton, indicator) in self.botones_nav.items():
            activo = nombre == self.seccion_activa
            
            if activo:
                boton.configure(
                    fg=COLORS["primary"], # Gold
                    # font=("Segoe UI", 11) # Mantener regular o bold? Mockup parece regular o semibold
                )
                indicator.configure(bg=COLORS["primary"]) # Gold underline
            else:
                boton.configure(
                    fg=COLORS["text_secondary"], # Gris
                )
                indicator.configure(bg=COLORS["background_card"]) # Hide (same color as bg)

    def cambiar_seccion(self, nombre):
        self.seccion_activa = nombre
        if self.vista_actual is not None:
            self.vista_actual.destroy()

        # Instanciar vista
        if nombre == "Punto de Venta":
            self.vista_actual = PuntoVentaView(self.contenido, self, self.pv_controller)
        elif nombre == "Productos":
            self.vista_actual = GestionOperativaView(self.contenido, self, self.go_controller)
        elif nombre == "Clientes":
            self.vista_actual = ClientesMayoristasView(self.contenido, self, self.cm_controller)
        elif nombre == "Responsabilidad Social":
            self.vista_actual = ResponsabilidadSocialView(self.contenido, self, self.rs_controller)
        elif nombre == "Inclusión Laboral":
            self.vista_actual = InclusionLaboralView(self.contenido, self, self.il_controller)

        if self.vista_actual is not None:
            self.vista_actual.pack(fill=tk.BOTH, expand=True)

        self._actualizar_estilos_nav()

    def mostrar_punto_venta(self):
        self.cambiar_seccion("Punto de Venta")

    def mostrar_gestion_operativa(self):
        self.cambiar_seccion("Productos")

    def mostrar_clientes_mayoristas(self):
        self.cambiar_seccion("Clientes")

    def mostrar_responsabilidad_social(self):
        self.cambiar_seccion("Responsabilidad Social")

    def mostrar_inclusion_laboral(self):
        self.cambiar_seccion("Inclusión Laboral")
    
    def _mostrar_menu_perfil(self):
        """Mostrar menú desplegable del perfil"""
        menu = tk.Menu(self.root, tearoff=0, bg="white", fg=COLORS["text_primary"])
        menu.add_command(label="Ver Datos de Perfil", command=self._ver_datos_perfil)
        menu.add_separator()
        menu.add_command(label="Cambiar Contraseña", command=self._cambiar_contrasena)
        menu.add_separator()
        menu.add_command(label="Cerrar Sesión", command=self._cerrar_sesion)
        
        # Mostrar menú en la posición del botón
        x = self.btn_perfil.winfo_rootx()
        y = self.btn_perfil.winfo_rooty() + self.btn_perfil.winfo_height()
        menu.post(x, y)
    
    def _ver_datos_perfil(self):
        """Mostrar datos del empleado en un diálogo"""
        if not self.usuario_data or not self.usuario_data.get('empleado'):
            messagebox.showinfo("Perfil", "No hay datos de perfil disponibles")
            return
        
        empleado = self.usuario_data['empleado']
        
        # Crear diálogo personalizado
        dialog = tk.Toplevel(self.root)
        dialog.title("Datos de Perfil")
        dialog.geometry("450x550")
        dialog.configure(bg=COLORS["background_main"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Frame principal
        main_frame = tk.Frame(dialog, bg=COLORS["background_card"], padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(
            main_frame,
            text="Información del Empleado",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS["background_card"],
            fg=COLORS["primary"]
        ).pack(pady=(0, 20))
        
        # Función auxiliar
        def agregar_campo(label, valor):
            frame = tk.Frame(main_frame, bg=COLORS["background_card"])
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                frame,
                text=f"{label}:",
                font=("Segoe UI", 10, "bold"),
                bg=COLORS["background_card"],
                fg=COLORS["text_secondary"],
                width=15,
                anchor="w"
            ).pack(side=tk.LEFT)
            
            tk.Label(
                frame,
                text=str(valor),
                font=("Segoe UI", 10),
                bg=COLORS["background_card"],
                fg=COLORS["text_primary"],
                anchor="w"
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Mostrar datos
        agregar_campo("ID Empleado", empleado.get('id_empleado', 'N/A'))
        agregar_campo("Nombre", empleado.get('nombre', 'N/A'))
        agregar_campo("Apellido Paterno", empleado.get('apellido_paterno', 'N/A'))
        agregar_campo("Apellido Materno", empleado.get('apellido_materno', 'N/A') or 'N/A')
        agregar_campo("CURP", empleado.get('curp', 'N/A'))
        agregar_campo("Teléfono", empleado.get('telefono', 'N/A') or 'N/A')
        agregar_campo("Fecha de Ingreso", empleado.get('fecha_ingreso', 'N/A'))
        agregar_campo("Salario Base", f"${empleado.get('salario_base', 0):.2f}" if empleado.get('salario_base') else 'N/A')
        agregar_campo("Puesto", empleado.get('puesto', 'N/A') or 'N/A')
        
        # Botón cerrar con estilo
        tk.Button(
            main_frame,
            text="Cerrar",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["primary"],
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=dialog.destroy
        ).pack(pady=(20, 0))
    
    def _cambiar_contrasena(self):
        """Abrir diálogo para cambiar contraseña"""
        # Crear diálogo personalizado
        dialog = tk.Toplevel(self.root)
        dialog.title("Cambiar Contraseña")
        dialog.geometry("450x350")
        dialog.configure(bg=COLORS["background_main"])
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Centrar el diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f"450x350+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(dialog, bg=COLORS["background_card"], padx=40, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        passwords = {'old': None, 'new': None, 'confirm': None}
        estado = {'actual': 0}
        
        # Título
        titulo_label = tk.Label(
            main_frame,
            text="Cambiar Contraseña",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS["background_card"],
            fg=COLORS["text_primary"]
        )
        titulo_label.pack(pady=(0, 20))
        
        # Label de instrucción
        instruccion_label = tk.Label(
            main_frame,
            text="Ingrese su contraseña actual:",
            font=("Segoe UI", 11),
            bg=COLORS["background_card"],
            fg=COLORS["text_secondary"]
        )
        instruccion_label.pack(pady=(0, 10))
        
        # Entry para contraseña
        password_entry = tk.Entry(
            main_frame,
            font=("Segoe UI", 12),
            show="*",
            width=30,
            relief=tk.SOLID,
            bd=1,
            bg="white"
        )
        password_entry.pack(pady=(0, 20), ipady=5)
        password_entry.focus()
        
        # Frame para botones
        button_frame = tk.Frame(main_frame, bg=COLORS["background_card"])
        button_frame.pack(pady=(10, 0))
        
        def siguiente():
            """Procesar el campo actual y pasar al siguiente"""
            valor = password_entry.get()
            
            if not valor:
                messagebox.showwarning("Advertencia", "Por favor ingrese un valor", parent=dialog)
                return
            
            if estado['actual'] == 0:
                passwords['old'] = valor
                estado['actual'] = 1
                instruccion_label.config(text="Ingrese su nueva contraseña:")
                password_entry.delete(0, tk.END)
                password_entry.focus()
                
            elif estado['actual'] == 1:
                passwords['new'] = valor
                estado['actual'] = 2
                instruccion_label.config(text="Confirme su nueva contraseña:")
                password_entry.delete(0, tk.END)
                password_entry.focus()
                btn_siguiente.config(text="Cambiar Contraseña")
                
            elif estado['actual'] == 2:
                passwords['confirm'] = valor
                
                if passwords['new'] != passwords['confirm']:
                    messagebox.showerror("Error", "Las contraseñas no coinciden", parent=dialog)
                    estado['actual'] = 1
                    instruccion_label.config(text="Ingrese su nueva contraseña:")
                    password_entry.delete(0, tk.END)
                    password_entry.focus()
                    btn_siguiente.config(text="Siguiente")
                    return
                
                if len(passwords['new']) > 50:
                    messagebox.showerror("Error", "La contraseña no puede tener más de 50 caracteres", parent=dialog)
                    estado['actual'] = 1
                    instruccion_label.config(text="Ingrese su nueva contraseña:")
                    password_entry.delete(0, tk.END)
                    password_entry.focus()
                    btn_siguiente.config(text="Siguiente")
                    return
                
                from models.usuario_model import UsuarioModel
                
                if not self.usuario_data or 'id_usuario' not in self.usuario_data:
                    messagebox.showerror("Error", "No se pudo identificar el usuario actual", parent=dialog)
                    dialog.destroy()
                    return
                
                id_usuario = self.usuario_data['id_usuario']
                
                exito = UsuarioModel.cambiar_contraseña(
                    id_usuario=id_usuario,
                    contraseña_actual=passwords['old'],
                    contraseña_nueva=passwords['new']
                )
                
                if exito:
                    messagebox.showinfo("Éxito", "Contraseña cambiada correctamente.", parent=dialog)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo cambiar la contraseña. Verifique su actual.", parent=dialog)
                    estado['actual'] = 0
                    instruccion_label.config(text="Ingrese su contraseña actual:")
                    password_entry.delete(0, tk.END)
                    password_entry.focus()
                    btn_siguiente.config(text="Siguiente")
        
        def cancelar():
            dialog.destroy()
        
        password_entry.bind('<Return>', lambda e: siguiente())
        
        btn_siguiente = tk.Button(
            button_frame,
            text="Siguiente",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["success"],
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=siguiente
        )
        btn_siguiente.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = tk.Button(
            button_frame,
            text="Cancelar",
            font=("Segoe UI", 11, "bold"),
            bg="#999999",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=cancelar
        )
        btn_cancelar.pack(side=tk.LEFT, padx=5)
    
    def _cerrar_sesion(self):
        """Cerrar sesión y volver al login"""
        self.root.destroy()
        from login_view import LoginView
        root = tk.Tk()
        app = LoginView(root)
        root.mainloop()

def run_main_app():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_main_app()
