import tkinter as tk
from tkinter import ttk

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


class MainApp:
    COLOR_FONDO_EXTERIOR = "#FFF8E1"  # Creamy yellow background
    COLOR_FONDO_INTERIOR = "#ffffff"
    COLOR_TEXTO_PRIMARIO = "#333333"
    COLOR_BOTON_FONDO = "#FDB813"
    COLOR_BOTON_TEXTO = "white"

    def __init__(self, root, usuario_data=None):
        self.root = root
        self.root.title("Maizimo App")
        self.usuario_data = usuario_data or {}

        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.geometry("1200x700")

        self.root.configure(bg=self.COLOR_FONDO_EXTERIOR)

        self.seccion_activa = "Punto de Venta"
        self.vista_actual = None

        # Controllers
        self.pv_controller = PuntoVentaController()
        self.go_controller = GestionOperativaController()
        self.cm_controller = ClientesMayoristasController()
        self.rs_controller = ResponsabilidadSocialController()
        self.il_controller = InclusionLaboralController()

        self._crear_layout_base()
        self.mostrar_punto_venta()

    def _crear_layout_base(self):
        barra_superior = tk.Frame(self.root, bg=self.COLOR_FONDO_EXTERIOR, pady=10)
        barra_superior.pack(fill=tk.X)

        titulo_frame = tk.Frame(barra_superior, bg=self.COLOR_FONDO_EXTERIOR)
        titulo_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(
            titulo_frame,
            text="Maizimo App",
            font=("Arial", 18, "bold"),
            fg="#2C1810",  # Dark brown for better contrast
            bg=self.COLOR_FONDO_EXTERIOR,
        ).pack(anchor="w")

        tk.Label(
            titulo_frame,
            text="Sistema de Gestión Integral",
            font=("Arial", 11),
            fg=self.COLOR_TEXTO_PRIMARIO,
            bg=self.COLOR_FONDO_EXTERIOR,
        ).pack(anchor="w")

        # Profile section with icon and name
        profile_frame = tk.Frame(barra_superior, bg=self.COLOR_FONDO_EXTERIOR)
        profile_frame.pack(side=tk.RIGHT, padx=20)
        
        # Profile button with dropdown menu
        btn_perfil = tk.Button(
            profile_frame,
            text="👤",  # User icon
            font=("Arial", 16),
            bg=self.COLOR_FONDO_EXTERIOR,  # Match background
            fg=self.COLOR_TEXTO_PRIMARIO,
            relief=tk.FLAT,
            bd=0,  # No border
            padx=10,
            pady=0,
            cursor="hand2",  # Hand cursor on hover
            command=self._mostrar_menu_perfil
        )
        btn_perfil.pack()
        self.btn_perfil = btn_perfil
        
        # Get user name from empleado data
        nombre_usuario = "Usuario"
        if self.usuario_data and self.usuario_data.get('empleado'):
            empleado = self.usuario_data['empleado']
            nombre_usuario = empleado.get('nombre', 'Usuario')
        
        # User name label below icon
        tk.Label(
            profile_frame,
            text=nombre_usuario,
            font=("Arial", 9),
            fg=self.COLOR_TEXTO_PRIMARIO,
            bg=self.COLOR_FONDO_EXTERIOR
        ).pack()

        self.nav_bar = tk.Frame(self.root, bg=self.COLOR_FONDO_EXTERIOR, pady=5)
        self.nav_bar.pack(fill=tk.X)

        self.botones_nav = {}
        secciones = [
            "Punto de Venta",
            "Productos",
            "Clientes",
            "Responsabilidad Social",
            "Inclusión Laboral",
        ]

        for nombre in secciones:
            boton = tk.Button(
                self.nav_bar,
                text=nombre,
                font=("Arial", 10),
                relief=tk.GROOVE,
                bd=1,
                padx=25,
                pady=8,
                command=lambda n=nombre: self.cambiar_seccion(n),
            )
            boton.pack(side=tk.LEFT, padx=5)
            self.botones_nav[nombre] = boton

        self.contenido = tk.Frame(self.root, bg=self.COLOR_FONDO_EXTERIOR, padx=20, pady=10)
        self.contenido.pack(fill=tk.BOTH, expand=True)

        self._actualizar_estilos_nav()

    def _actualizar_estilos_nav(self):
        for nombre, boton in self.botones_nav.items():
            activo = nombre == self.seccion_activa
            boton.configure(
                font=("Arial", 10, "bold" if activo else "normal"),
                bg=self.COLOR_BOTON_FONDO if activo else self.COLOR_FONDO_INTERIOR,
                fg="white" if activo else self.COLOR_TEXTO_PRIMARIO,
                relief=tk.RAISED if activo else tk.GROOVE,
            )

    def cambiar_seccion(self, nombre):
        self.seccion_activa = nombre
        if self.vista_actual is not None:
            self.vista_actual.destroy()

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
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Ver Datos de Perfil", command=self._ver_datos_perfil)
        menu.add_separator()
        menu.add_command(label="Cambiar Contraseña", command=self._cambiar_contrasena)
        menu.add_command(label="Cambiar Nombre", command=self._cambiar_nombre)
        menu.add_separator()
        menu.add_command(label="Cerrar Sesión", command=self._cerrar_sesion)
        
        # Mostrar menú en la posición del botón
        x = self.btn_perfil.winfo_rootx()
        y = self.btn_perfil.winfo_rooty() + self.btn_perfil.winfo_height()
        menu.post(x, y)
    
    def _ver_datos_perfil(self):
        """Mostrar datos del empleado en un diálogo"""
        from tkinter import messagebox
        
        if not self.usuario_data or not self.usuario_data.get('empleado'):
            messagebox.showinfo("Perfil", "No hay datos de perfil disponibles")
            return
        
        empleado = self.usuario_data['empleado']
        
        # Crear diálogo personalizado
        dialog = tk.Toplevel(self.root)
        dialog.title("Datos de Perfil")
        dialog.geometry("400x500")
        dialog.configure(bg="#f0f0f0")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Frame principal
        main_frame = tk.Frame(dialog, bg="#ffffff", padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(
            main_frame,
            text="Información del Empleado",
            font=("Arial", 16, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(pady=(0, 20))
        
        # Función auxiliar para agregar campos
        def agregar_campo(label, valor):
            frame = tk.Frame(main_frame, bg="#ffffff")
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                frame,
                text=f"{label}:",
                font=("Arial", 10, "bold"),
                bg="#ffffff",
                fg="#555555",
                width=15,
                anchor="w"
            ).pack(side=tk.LEFT)
            
            tk.Label(
                frame,
                text=str(valor),
                font=("Arial", 10),
                bg="#ffffff",
                fg="#333333",
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
        
        # Botón cerrar
        tk.Button(
            main_frame,
            text="Cerrar",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=dialog.destroy
        ).pack(pady=(20, 0))
    
    def _cambiar_contrasena(self):
        """Abrir diálogo para cambiar contraseña"""
        from tkinter import simpledialog, messagebox
        
        # Solicitar contraseña actual
        old_password = simpledialog.askstring("Cambiar Contraseña", "Ingrese su contraseña actual:", show='*')
        if not old_password:
            return
        
        # Solicitar nueva contraseña
        new_password = simpledialog.askstring("Cambiar Contraseña", "Ingrese su nueva contraseña:", show='*')
        if not new_password:
            return
        
        # Confirmar nueva contraseña
        confirm_password = simpledialog.askstring("Cambiar Contraseña", "Confirme su nueva contraseña:", show='*')
        if not confirm_password:
            return
        
        if new_password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        # TODO: Implement password change logic with user model
        messagebox.showinfo("Éxito", "Contraseña cambiada correctamente")
    
    def _cambiar_nombre(self):
        """Abrir diálogo para cambiar nombre"""
        from tkinter import simpledialog, messagebox
        
        nuevo_nombre = simpledialog.askstring("Cambiar Nombre", "Ingrese su nuevo nombre:")
        if not nuevo_nombre:
            return
        
        # TODO: Implement name change logic with user model
        messagebox.showinfo("Éxito", "Nombre cambiado correctamente")
    
    def _cerrar_sesion(self):
        """Cerrar sesión y volver al login"""
        self.root.destroy()
        # Importar y abrir login
        from login_view import LoginView
        import tkinter as tk
        root = tk.Tk()
        app = LoginView(root)
        root.mainloop()


def run_main_app():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_main_app()
