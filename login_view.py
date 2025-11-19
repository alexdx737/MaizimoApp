import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 
import os 
from main_view import run_main_app

# --- SIMULACIÓN DE MÓDULOS ---
# Simula el controlador de autenticación (auth_controller.py)
# Reemplaza esto con tu importación real: from auth_controller import validar_credenciales
def validar_credenciales(usuario, password):
    # Lógica de validación dummy
    return usuario == "admin" and password == "admin123"
# --- FIN DE SIMULACIÓN ---


class LoginApp:
    # Paleta de colores basada en la imagen
    COLOR_FONDO_EXTERIOR = "#C7B299" 
    COLOR_FONDO_INTERIOR = "#D7C2A9"
    COLOR_TEXTO_PRIMARIO = "#333333"
    COLOR_BOTON_FONDO = "#FDB813"
    COLOR_BOTON_TEXTO = "white"

    def __init__(self, root):
        self.root = root
        self.root.title("Maizimo App - Iniciar Sesión")
        
        # 1. HACER LA VENTANA A PANTALLA COMPLETA
        try:
            # Intenta usar 'zoomed' para Windows/Linux
            self.root.state('zoomed')
        except tk.TclError:
            # Opción alternativa para macOS o si 'zoomed' no funciona
            self.root.attributes('-fullscreen', True) 
            
        self.root.configure(bg=self.COLOR_FONDO_EXTERIOR)
        
        # Centrar el Frame principal en la ventana
        # Se usa bd=20 y relief=tk.RAISED para darle un pequeño efecto de elevación (aunque sin las sombras de CSS)
        self.frame_login = tk.Frame(root, bg=self.COLOR_FONDO_INTERIOR, padx=30, pady=30, bd=0, relief=tk.FLAT)
        self.frame_login.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.crear_widgets()

    def cargar_imagen(self):
        # Asegúrate de que esta ruta sea correcta para tu imagen de perfil
        ruta_imagen = "image_60a746_profile.png" # <--- CAMBIA ESTO
        
        # Intenta cargar la imagen de perfil
        try:
            # Abrir y redimensionar la imagen (150x150)
            img = Image.open(ruta_imagen).resize((150, 150), Image.LANCZOS)
            self.perfil_img = ImageTk.PhotoImage(img)
            
            # Label para la imagen de perfil
            img_label = tk.Label(self.frame_login, image=self.perfil_img, bg=self.COLOR_FONDO_INTERIOR)
            img_label.grid(row=0, column=0, columnspan=2, pady=(10, 20)) 
        except FileNotFoundError:
            # Si la imagen no se encuentra, se muestra un espacio vacío
            print(f"ERROR: No se encontró la imagen en {ruta_imagen}. Asegúrate de tenerla.")
            tk.Label(self.frame_login, text="[Image]", font=("Arial", 10), 
                     width=15, height=7, bg="#AAAAAA").grid(row=0, column=0, columnspan=2, pady=(10, 20))
            
    def crear_widgets(self):
        # Cargar la imagen de perfil
        self.cargar_imagen()
        
        # --- Títulos ---
        tk.Label(self.frame_login, text="Maizimo App", 
                 font=("Arial", 24, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=1, column=0, columnspan=2, pady=(0, 5))
        
        tk.Label(self.frame_login, text="Sistema de Gestión Integral para Tortillería", 
                 font=("Arial", 11), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=2, column=0, columnspan=2, pady=(0, 30))

        # --- Campo de Usuario ---
        tk.Label(self.frame_login, text="Usuario", anchor="w", 
                 font=("Arial", 12, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 0))
        
        self.username_entry = tk.Entry(self.frame_login, width=40, font=("Arial", 12), bd=1, relief=tk.FLAT)
        self.username_entry.insert(0, "Ingrese su usuario") # Placeholder
        self.username_entry.bind("<FocusIn>", self._clear_placeholder)
        self.username_entry.bind("<FocusOut>", self._restore_placeholder)
        self.username_entry.grid(row=4, column=0, columnspan=2, pady=(5, 15), ipady=5)

        # --- Campo de Contraseña ---
        tk.Label(self.frame_login, text="Contraseña", anchor="w", 
                 font=("Arial", 12, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))
        
        self.password_entry = tk.Entry(self.frame_login, width=40, font=("Arial", 12), show="*", bd=1, relief=tk.FLAT)
        self.password_entry.insert(0, "Ingrese su contraseña") # Placeholder visual
        self.password_entry.bind("<FocusIn>", self._clear_placeholder_password)
        self.password_entry.bind("<FocusOut>", self._restore_placeholder_password)
        self.password_entry.grid(row=6, column=0, columnspan=2, pady=(5, 50), ipady=5)
        
        # --- Botón de Iniciar Sesión ---
        tk.Button(self.frame_login, text="Iniciar Sesión", command=self.Login,
                  bg=self.COLOR_BOTON_FONDO, fg=self.COLOR_BOTON_TEXTO,
                  font=("Arial", 14, "bold"), width=30, height=1, bd=0, relief=tk.FLAT,
                  activebackground="#D39210", activeforeground=self.COLOR_BOTON_TEXTO).grid(row=7, column=0, columnspan=2, pady=(0, 0))
        
        # *** Se omiten las etiquetas de "Usuario demo" y "Contraseña demo" ***


    # --- Métodos de Placeholder ---
    def _clear_placeholder(self, event):
        if self.username_entry.get() == "Ingrese su usuario":
            self.username_entry.delete(0, tk.END)

    def _restore_placeholder(self, event):
        if not self.username_entry.get():
            self.username_entry.insert(0, "Ingrese su usuario")

    def _clear_placeholder_password(self, event):
        current_text = self.password_entry.get()
        if current_text == "Ingrese su contraseña":
            # Cuando el usuario hace FocusIn, establecemos show="*" y limpiamos el texto
            self.password_entry.config(show="*")
            self.password_entry.delete(0, tk.END)

    def _restore_placeholder_password(self, event):
        if not self.password_entry.get():
            # Si el campo queda vacío al salir, mostramos el placeholder sin ocultar el texto
            self.password_entry.config(show="") 
            self.password_entry.insert(0, "Ingrese su contraseña")

    # --- Lógica de Login ---
    def Login(self):
        # Obtener los datos de entrada (entry)
        usuario = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Evitar usar el texto del placeholder como credencial
        if usuario == "Ingrese su usuario": usuario = ""
        if password == "Ingrese su contraseña": password = ""

        if not usuario or not password:
            messagebox.showwarning("Faltan datos", "Por favor ingresa usuario y contraseña.")
            return
        
        # Llama a la función de tu auth_controller.py
        if validar_credenciales(usuario, password):
            messagebox.showinfo("Acceso concedido", f"Bienvenido {usuario}!")
            # Cerrar la ventana de login y abrir la ventana principal
            self.root.destroy()
            run_main_app()
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()