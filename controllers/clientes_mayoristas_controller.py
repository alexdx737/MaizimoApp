from models.cliente_model import ClienteModel

class ClientesMayoristasController:
    """Controller de la sección Clientes Mayoristas.

    Maneja la gestión CRUD de clientes mayoristas desde la base de datos.
    """

    def __init__(self):
        self.clientes = []
        self.cargar_clientes()
    
    def cargar_clientes(self):
        """Cargar clientes desde la base de datos"""
        try:
            clientes_db = ClienteModel.listar_todos()
            self.clientes = []
            for c in clientes_db:
                # Formatear para la vista
                nombre_completo = f"{c['nombre']} {c['apellido_paterno']}"
                if c.get('apellido_materno'):
                    nombre_completo += f" {c['apellido_materno']}"
                
                telefono = c.get('telefono', 'Sin teléfono')
                descuento = f"{float(c['descuento']):.0f}%"
                
                self.clientes.append({
                    'id': c['id_cliente'],
                    'nombre': nombre_completo,
                    'nombre_raw': c['nombre'],
                    'apellido_paterno': c['apellido_paterno'],
                    'apellido_materno': c.get('apellido_materno', ''),
                    'telefono': telefono,
                    'descuento_pct': float(c['descuento']),
                    'descuento_str': descuento,
                    'direccion': c.get('direccion', ''),
                    'descripcion': c.get('descripcion', '')
                })
            
            print(f"✓ Cargados {len(self.clientes)} clientes")
        except Exception as e:
            print(f"Error cargando clientes: {e}")
            self.clientes = []
    
    def agregar_cliente(self, nombre, apellido_paterno, telefono, apellido_materno=None, 
                       direccion=None, descuento=0.0, descripcion=None):
        """Agregar nuevo cliente a la base de datos"""
        try:
            cliente = ClienteModel.crear(
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                telefono=telefono,
                apellido_materno=apellido_materno,
                direccion=direccion,
                descuento=descuento,
                descripcion=descripcion
            )
            
            if cliente:
                self.cargar_clientes()  # Recargar lista
                return True
            return False
        except Exception as e:
            print(f"Error agregando cliente: {e}")
            return False
    
    def actualizar_cliente(self, id_cliente, **kwargs):
        """Actualizar datos de un cliente"""
        try:
            cliente = ClienteModel.actualizar(id_cliente, **kwargs)
            if cliente:
                self.cargar_clientes()  # Recargar lista
                return True
            return False
        except Exception as e:
            print(f"Error actualizando cliente: {e}")
            return False
    
    def eliminar_cliente(self, id_cliente):
        """Eliminar cliente de la base de datos"""
        try:
            if ClienteModel.eliminar(id_cliente):
                self.cargar_clientes()  # Recargar lista
                return True
            return False
        except Exception as e:
            print(f"Error eliminando cliente: {e}")
            return False
    
    def obtener_cliente(self, id_cliente):
        """Obtener datos completos de un cliente"""
        for c in self.clientes:
            if c['id'] == id_cliente:
                return c
        return None

