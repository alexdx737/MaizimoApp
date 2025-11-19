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
    COLOR_FONDO_EXTERIOR = "#C7B299"
    COLOR_FONDO_INTERIOR = "#D7C2A9"
    COLOR_TEXTO_PRIMARIO = "#333333"
    COLOR_BOTON_FONDO = "#FDB813"
    COLOR_BOTON_TEXTO = "white"

    def __init__(self, root):
        self.root = root
        self.root.title("Maizimo App")

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
            fg="#FF9800",
            bg=self.COLOR_FONDO_EXTERIOR,
        ).pack(anchor="w")

        tk.Label(
            titulo_frame,
            text="Sistema de Gestión Integral",
            font=("Arial", 11),
            fg=self.COLOR_TEXTO_PRIMARIO,
            bg=self.COLOR_FONDO_EXTERIOR,
        ).pack(anchor="w")

        btn_cerrar = tk.Button(
            barra_superior,
            text="Cerrar Sesión",
            font=("Arial", 10, "bold"),
            bg=self.COLOR_FONDO_INTERIOR,
            fg=self.COLOR_TEXTO_PRIMARIO,
            relief=tk.FLAT,
            padx=15,
            pady=5,
            command=self.root.destroy,
        )
        btn_cerrar.pack(side=tk.RIGHT, padx=20)

        self.nav_bar = tk.Frame(self.root, bg=self.COLOR_FONDO_EXTERIOR, pady=5)
        self.nav_bar.pack(fill=tk.X)

        self.botones_nav = {}
        secciones = [
            "Punto de Venta",
            "Gestión Operativa",
            "Clientes Mayoristas",
            "Responsabilidad Social",
            "Inclusión Laboral",
        ]

        for nombre in secciones:
            boton = tk.Button(
                self.nav_bar,
                text=nombre,
                font=("Arial", 10),
                relief=tk.FLAT,
                padx=20,
                pady=6,
                command=lambda n=nombre: self.cambiar_seccion(n),
            )
            boton.pack(side=tk.LEFT, padx=3)
            self.botones_nav[nombre] = boton

        self.contenido = tk.Frame(self.root, bg=self.COLOR_FONDO_EXTERIOR, padx=20, pady=10)
        self.contenido.pack(fill=tk.BOTH, expand=True)

        self._actualizar_estilos_nav()

    def _actualizar_estilos_nav(self):
        for nombre, boton in self.botones_nav.items():
            activo = nombre == self.seccion_activa
            boton.configure(
                font=("Arial", 10, "bold" if activo else "normal"),
                bg=self.COLOR_FONDO_INTERIOR if activo else self.COLOR_FONDO_EXTERIOR,
                fg=self.COLOR_TEXTO_PRIMARIO,
            )

    def cambiar_seccion(self, nombre):
        self.seccion_activa = nombre
        if self.vista_actual is not None:
            self.vista_actual.destroy()

        if nombre == "Punto de Venta":
            self.vista_actual = PuntoVentaView(self.contenido, self, self.pv_controller)
        elif nombre == "Gestión Operativa":
            self.vista_actual = GestionOperativaView(self.contenido, self, self.go_controller)
        elif nombre == "Clientes Mayoristas":
            self.vista_actual = ClientesMayoristasView(self.contenido, self, self.cm_controller)
        elif nombre == "Responsabilidad Social":
            self.vista_actual = ResponsabilidadSocialView(self.contenido, self, self.rs_controller)
        elif nombre == "Inclusión Laboral":
            self.vista_actual = InclusionLaboralView(self.contenido, self, self.il_controller)

        if self.vista_actual is not None:
            self.vista_actual.pack(fill=tk.BOTH, expand=True)

        self._actualizar_estilos_nav()

    def mostrar_punto_venta(self):
        # Por compatibilidad, delega en cambiar_seccion
        self.cambiar_seccion("Punto de Venta")

    def mostrar_gestion_operativa(self):
        self.cambiar_seccion("Gestión Operativa")

    def mostrar_clientes_mayoristas(self):
        self.cambiar_seccion("Clientes Mayoristas")

    def mostrar_responsabilidad_social(self):
        self.cambiar_seccion("Responsabilidad Social")

    def mostrar_inclusion_laboral(self):
        self.cambiar_seccion("Inclusión Laboral")


def run_main_app():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
