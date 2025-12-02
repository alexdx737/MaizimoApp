from models.empleado_model import EmpleadoModel

class InclusionLaboralController:
    """Controller de la sección Inclusión Laboral.

    Mantiene el listado de trabajadores en el programa (empleados vulnerables).
    """

    def __init__(self):
        self.trabajadores = []
        self.cargar_trabajadores()
    
    def cargar_trabajadores(self):
        """Cargar empleados vulnerables desde la base de datos"""
        try:
            empleados_db = EmpleadoModel.listar_vulnerables()
            self.trabajadores = []
            for e in empleados_db:
                # Formatear para la vista
                nombre_completo = f"{e['nombre']} {e['apellido_paterno']}"
                if e.get('apellido_materno'):
                    nombre_completo += f" {e['apellido_materno']}"
                
                situacion = e.get('descripcion', 'No especificada')
                ciclo = self._formatear_ciclo(e.get('ciclo', 'espera'))
                fecha = e.get('fecha_ingreso', '')
                
                self.trabajadores.append({
                    'id': e['id_empleado'],
                    'nombre': nombre_completo,
                    'situacion': situacion,
                    'ciclo': ciclo,
                    'ciclo_raw': e.get('ciclo', 'espera'),
                    'fecha': str(fecha),
                    'curp': e.get('curp', ''),
                    'nombre_raw': e['nombre'],
                    'apellido_paterno': e['apellido_paterno'],
                    'apellido_materno': e.get('apellido_materno', '')
                })
            
            print(f"✓ Cargados {len(self.trabajadores)} trabajadores vulnerables")
        except Exception as e:
            print(f"Error cargando trabajadores: {e}")
            self.trabajadores = []
    
    def _formatear_ciclo(self, ciclo):
        """Formatear ciclo para visualización"""
        formatos = {
            'espera': 'En Espera',
            'proceso': 'En Proceso',
            'finalizado': 'Finalizado'
        }
        return formatos.get(ciclo, ciclo)
    
    def agregar_trabajador(self, nombre, apellido_paterno, curp, fecha_ingreso, 
                          apellido_materno=None, descripcion=None, ciclo='espera'):
        """Agregar nuevo empleado vulnerable a la base de datos"""
        try:
            empleado = EmpleadoModel.crear(
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                curp=curp,
                fecha_ingreso=fecha_ingreso,
                vulnerable=True,
                ciclo=ciclo,
                apellido_materno=apellido_materno,
                descripcion=descripcion
            )
            
            if empleado:
                self.cargar_trabajadores()  # Recargar lista
                return True
            return False
        except Exception as e:
            print(f"Error agregando trabajador: {e}")
            return False
    
    def actualizar_trabajador(self, id_empleado, **kwargs):
        """Actualizar datos de un empleado"""
        try:
            empleado = EmpleadoModel.actualizar(id_empleado, **kwargs)
            if empleado:
                self.cargar_trabajadores()  # Recargar lista
                return True
            return False
        except Exception as e:
            print(f"Error actualizando trabajador: {e}")
            return False
    
    def eliminar_trabajador(self, id_empleado):
        """Eliminar empleado de la base de datos"""
        try:
            if EmpleadoModel.eliminar(id_empleado):
                self.cargar_trabajadores()  # Recargar lista
                return True
            return False
        except Exception as e:
            print(f"Error eliminando trabajador: {e}")
            return False
    
    def obtener_trabajador(self, id_empleado):
        """Obtener datos completos de un empleado"""
        for t in self.trabajadores:
            if t['id'] == id_empleado:
                return t
        return None
