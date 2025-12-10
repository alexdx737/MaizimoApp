import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from models.usuario_model import UsuarioModel
from main_view import MainApp
import os
from utils.theme import COLORS, FONTS, DIMENSIONS
from utils.components import RoundedButton, RoundedEntry

def validar_credenciales(usuario, password):
    """Wrapper para validar credenciales usando el modelo"""
    user = UsuarioModel.validar_credenciales(usuario, password)
    return user is not None

def run_main_app(usuario_data=None):
    """Iniciar la aplicación principal"""
    root = tk.Tk()
    app = MainApp(root, usuario_data=usuario_data)
    root.mainloop()

class LoginView:
    def __init__(self, root):
        self.root = root    
        self.root.title("Maizimo App - Iniciar Sesión")
        
        # Configuración de ventana
        window_width = 1024
        window_height = 768
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.configure(bg=COLORS["background_main"])
        
        # Frame principal (Tarjeta centrada)
        # Usamos Canvas para dibujar el borde redondeado de la tarjeta si fuera necesario, 
        # pero un Frame blanco limpio funciona bien para este estilo "Clean"
        self.frame_login = tk.Frame(root, bg=COLORS["background_card"], padx=60, pady=60)
        self.frame_login.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Sombra simple (Frame gris oscuro detrás)
        self.shadow_frame = tk.Frame(root, bg="#E0E0E0")
        self.shadow_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=505, height=605) # Ligeramente más grande
        self.frame_login.lift() # Asegurar que la tarjeta esté encima

        self.crear_widgets()

    def cargar_imagen(self):
        # Usar el logo de Maizimo o Texto estilizado
        try:
            ruta_imagen = "assets/maizimo_logo.png" 
            if not os.path.exists(ruta_imagen):
                 ruta_imagen = "maizimo_logo.png"
                 
            if os.path.exists(ruta_imagen):
                # Logo más pequeño y estilizado
                img = Image.open(ruta_imagen).resize((80, 80), Image.LANCZOS)
                self.perfil_img = ImageTk.PhotoImage(img)
                img_label = tk.Label(self.frame_login, image=self.perfil_img, bg=COLORS["background_card"])
                img_label.pack(pady=(0, 10))
            else:
                # Título estilo Badge si no hay logo
               raise FileNotFoundError
        except Exception:
             # Badge estético "MAIZIMO"
             badge_frame = tk.Frame(self.frame_login, bg=COLORS["primary"], padx=20, pady=5)
             badge_frame.pack(pady=(0, 10))
             tk.Label(badge_frame, text="MAIZIMO", font=("Segoe UI", 16, "bold"), 
                      bg=COLORS["primary"], fg="white").pack()

    def crear_widgets(self):
        self.cargar_imagen()
        
        # Título
        tk.Label(self.frame_login, text="MAIZIMO", font=("Segoe UI", 24, "bold"), 
                 bg=COLORS["background_card"], fg="#D4A319").pack(pady=(0, 5))
                 
        tk.Label(self.frame_login, text="Sistema de Gestión Integral", font=("Segoe UI", 11), 
                 bg=COLORS["background_card"], fg=COLORS["text_secondary"]).pack(pady=(0, 30))

        # --- Inputs ---
        
        # Usuario
        tk.Label(self.frame_login, text="ID Usuario", font=("Segoe UI", 10, "bold"), 
                 bg=COLORS["background_card"], fg=COLORS["text_primary"], anchor="w").pack(fill="x", pady=(0, 5))
        
        self.username_entry = RoundedEntry(self.frame_login, width=380, height=45, 
                                           placeholder="Ingrese su ID", icon="👤")
        self.username_entry.pack(pady=(0, 20))

        # Contraseña
        tk.Label(self.frame_login, text="Contraseña", font=("Segoe UI", 10, "bold"), 
                 bg=COLORS["background_card"], fg=COLORS["text_primary"], anchor="w").pack(fill="x", pady=(0, 5))
        
        self.password_entry = RoundedEntry(self.frame_login, width=380, height=45, 
                                           placeholder="********", show="*", icon="🔒")
        self.password_entry.pack(pady=(0, 30))

        # --- Botones ---
        
        # Iniciar Sesión (Relleno)
        self.btn_login = RoundedButton(self.frame_login, text="Iniciar Sesión", width=380, height=45,
                                       bg_color=COLORS["primary"], text_color="white",
                                       hover_color=COLORS["primary_hover"],
                                       command=self.Login)
        self.btn_login.pack(pady=(0, 15))
        
        # Registrarse (Borde)
        self.btn_registro = RoundedButton(self.frame_login, text="Registrarse", width=380, height=45,
                                          bg_color=COLORS["background_card"], text_color=COLORS["text_secondary"],
                                          border_color=COLORS["primary"], hover_color=COLORS["primary"],
                                          command=self.abrir_registro)
        self.btn_registro.pack()

    def Login(self):
        usuario_val = self.username_entry.get().strip()
        password_val = self.password_entry.get().strip()
        
        if not usuario_val or not password_val:
            messagebox.showwarning("Faltan datos", "Por favor ingresa usuario y contraseña.")
            return
            
        if not usuario_val.isdigit():
            messagebox.showerror("Error", "El ID de usuario debe ser numérico.")
            return
        
        try:
            user = UsuarioModel.validar_credenciales(usuario_val, password_val)
            if user:
                # Obtener el nombre del empleado
                nombre_usuario = user.get('empleado', {}).get('nombre', f"Usuario {user['id_usuario']}")
                
                # Mostrar mensaje de bienvenida
                messagebox.showinfo("Bienvenido", 
                                  f"¡Bienvenido(a) {nombre_usuario}!\n\nRol: {user['rol']}")
                # Transición suave (opcional) o mensaje
                self.root.destroy()
                run_main_app(usuario_data=user)
            else:
                messagebox.showerror("Acceso denegado", "ID o contraseña incorrectos.")
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {e}")
            import traceback
            traceback.print_exc()
    
    def abrir_registro(self):
        self.root.destroy()
        from registro_view import RegistroView
        root = tk.Tk()
        app = RegistroView(root)
        root.mainloop()

if __name__ == "__main__":
    print("Iniciando interfaz gráfica con tema Blossom...")
    root = tk.Tk()
    app = LoginView(root)
    root.mainloop()
