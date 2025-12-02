import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from models.usuario_model import UsuarioModel
from main_view import MainApp
import os

# Colores globales
COLOR_TEXTO_PRIMARIO = "#333333"
COLOR_BOTON_FONDO = "#FDB813"
COLOR_BOTON_TEXTO = "white"
COLOR_FONDO_EXTERIOR = "#f0f0f0"
COLOR_FONDO_INTERIOR = "#ffffff"

def validar_credenciales(usuario, password):
    """Wrapper para validar credenciales usando el modelo"""
    user = UsuarioModel.validar_credenciales(usuario, password)
    return user is not None

def run_main_app():
    """Iniciar la aplicación principal"""
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

class LoginView:
    def __init__(self, root):
        self.root = root    
        self.root.title("Maizimo App - Iniciar Sesión")
        
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
        
        # Centrar el Frame principal en la ventana
        self.frame_login = tk.Frame(root, bg=self.COLOR_FONDO_INTERIOR, padx=30, pady=30, bd=0, relief=tk.FLAT)
        self.frame_login.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.crear_widgets()

    def cargar_imagen(self):
        # Asegúrate de que esta ruta sea correcta para tu imagen de perfil
        ruta_imagen = "image_60a746_profile.png" 
        
        try:
            if os.path.exists(ruta_imagen):
                img = Image.open(ruta_imagen).resize((150, 150), Image.LANCZOS)
                self.perfil_img = ImageTk.PhotoImage(img)
                img_label = tk.Label(self.frame_login, image=self.perfil_img, bg=self.COLOR_FONDO_INTERIOR)
                img_label.grid(row=0, column=0, columnspan=2, pady=(10, 20)) 
            else:
                raise FileNotFoundError
        except Exception:
            # Placeholder si no hay imagen
            lbl = tk.Label(self.frame_login, text="MAIZIMO", font=("Arial", 20, "bold"), 
                     width=10, height=2, bg="#FDB813", fg="white")
            lbl.grid(row=0, column=0, columnspan=2, pady=(10, 20))
            
    def crear_widgets(self):
        self.cargar_imagen()
        
        # --- Títulos ---
        tk.Label(self.frame_login, text="Maizimo App", 
                 font=("Arial", 24, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=1, column=0, columnspan=2, pady=(0, 5))
        
        tk.Label(self.frame_login, text="Sistema de Gestión Integral", 
                 font=("Arial", 11), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=2, column=0, columnspan=2, pady=(0, 30))

        # --- Campo de Usuario ---
        tk.Label(self.frame_login, text="ID Usuario", anchor="w", 
                 font=("Arial", 12, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 0))
        
        self.username_entry = tk.Entry(self.frame_login, width=40, font=("Arial", 12), bd=1, relief=tk.FLAT)
        self.username_entry.insert(0, "Ingrese su ID (ej: 1)")
        self.username_entry.bind("<FocusIn>", self._clear_placeholder)
        self.username_entry.bind("<FocusOut>", self._restore_placeholder)
        self.username_entry.grid(row=4, column=0, columnspan=2, pady=(5, 15), ipady=5)

        # --- Campo de Contraseña ---
        tk.Label(self.frame_login, text="Contraseña", anchor="w", 
                 font=("Arial", 12, "bold"), fg=self.COLOR_TEXTO_PRIMARIO, 
                 bg=self.COLOR_FONDO_INTERIOR).grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))
        
        self.password_entry = tk.Entry(self.frame_login, width=40, font=("Arial", 12), show="*", bd=1, relief=tk.FLAT)
        self.password_entry.insert(0, "Ingrese su contraseña")
        self.password_entry.bind("<FocusIn>", self._clear_placeholder_password)
        self.password_entry.bind("<FocusOut>", self._restore_placeholder_password)
        self.password_entry.grid(row=6, column=0, columnspan=2, pady=(5, 50), ipady=5)
        
        # --- Botón de Iniciar Sesión ---
        tk.Button(self.frame_login, text="Iniciar Sesión", command=self.Login,
                  bg=self.COLOR_BOTON_FONDO, fg=self.COLOR_BOTON_TEXTO,
                  font=("Arial", 14, "bold"), width=30, height=1, bd=0, relief=tk.FLAT,
                  activebackground="#D39210", activeforeground=self.COLOR_BOTON_TEXTO).grid(row=7, column=0, columnspan=2, pady=(0, 10))
        
        # --- Botón de Registrarse ---
        tk.Button(self.frame_login, text="Registrarse", command=self.abrir_registro,
                  bg="#666666", fg="white",
                  font=("Arial", 12, "bold"), width=30, height=1, bd=0, relief=tk.FLAT,
                  activebackground="#555555", activeforeground="white").grid(row=8, column=0, columnspan=2, pady=(0, 0))

    # --- Métodos de Placeholder ---
    def _clear_placeholder(self, event):
        if self.username_entry.get() == "Ingrese su ID (ej: 1)":
            self.username_entry.delete(0, tk.END)

    def _restore_placeholder(self, event):
        if not self.username_entry.get():
            self.username_entry.insert(0, "Ingrese su ID (ej: 1)")

    def _clear_placeholder_password(self, event):
        current_text = self.password_entry.get()
        if current_text == "Ingrese su contraseña":
            self.password_entry.config(show="*")
            self.password_entry.delete(0, tk.END)

    def _restore_placeholder_password(self, event):
        if not self.password_entry.get():
            self.password_entry.config(show="") 
            self.password_entry.insert(0, "Ingrese su contraseña")

    # --- Lógica de Login ---
    def Login(self):
        usuario = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if usuario == "Ingrese su ID (ej: 1)": usuario = ""
        if password == "Ingrese su contraseña": password = ""

        if not usuario or not password:
            messagebox.showwarning("Faltan datos", "Por favor ingresa usuario y contraseña.")
            return
            
        # Validación de tipo de dato (ID debe ser numérico)
        if not usuario.isdigit():
            messagebox.showerror("Error de formato", "El Usuario debe ser el ID numérico (ej: 1).")
            return
        
        try:
            if validar_credenciales(usuario, password):
                messagebox.showinfo("Acceso concedido", f"Bienvenido!")
                self.root.destroy()
                run_main_app()
            else:
                messagebox.showerror("Acceso denegado", "ID o contraseña incorrectos.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al conectar: {e}")
    
    def abrir_registro(self):
        """Abrir la ventana de registro"""
        self.root.destroy()
        from registro_view import RegistroView
        root = tk.Tk()
        app = RegistroView(root)
        root.mainloop()

if __name__ == "__main__":
    print("Iniciando interfaz gráfica...")
    root = tk.Tk()
    app = LoginView(root)
    root.mainloop()