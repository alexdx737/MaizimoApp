from models.donacion_model import DonacionModel
from models.producto_model import ProductoModel

class ResponsabilidadSocialController:
    """Controller de la sección Responsabilidad Social.

    Mantiene la configuración de descuentos y redondeo solidario.
    """

    def __init__(self):
        self.descuento_bolsa = 2.0  # pesos
        self.fondo_acumulado = 0.0
        self.equivalente_tortillas_kg = 0
        self.donaciones = []
        self.actualizar_datos()
    
    def actualizar_datos(self):
        """Actualizar fondo acumulado y donaciones desde la base de datos"""
        try:
            # Calcular fondo acumulado
            self.fondo_acumulado = DonacionModel.obtener_total()
            
            # Calcular equivalente en tortillas (asumiendo precio de tortillas 25 pesos/kg)
            precio_tortillas_kg = 25.0  # Esto podría venir de la base de datos
            try:
                # Intentar obtener precio real de tortillas
                productos = ProductoModel.listar_todos()
                for p in productos:
                    if 'tortilla' in p['nombre'].lower() and p['unidad_medida'] == 'kg':
                        precio_tortillas_kg = float(p['costo_unitario'])
                        break
            except:
                pass  # Usar precio por defecto
            
            self.equivalente_tortillas_kg = int(self.fondo_acumulado / precio_tortillas_kg) if precio_tortillas_kg > 0 else 0
            
            # Cargar lista de donaciones
            self.cargar_donaciones()
            
            print(f"✓ Fondo acumulado: ${self.fondo_acumulado:.2f}, Equivalente: {self.equivalente_tortillas_kg} kg")
        except Exception as e:
            print(f"Error actualizando datos de donaciones: {e}")
            self.fondo_acumulado = 0.0
            self.equivalente_tortillas_kg = 0
            self.donaciones = []
    
    def cargar_donaciones(self):
        """Cargar lista de donaciones desde la base de datos"""
        try:
            donaciones_db = DonacionModel.listar_todas()
            self.donaciones = []
            
            for d in donaciones_db:
                # Obtener info de la venta
                venta_info = d.get('venta_completa', {})
                fecha = venta_info.get('fecha', 'N/A') if venta_info else 'N/A'
                hora = venta_info.get('hora', 'N/A') if venta_info else 'N/A'
                if hora and hora != 'N/A':
                    hora = hora[:5]  # Solo HH:MM
                
                self.donaciones.append({
                    'id_donacion': d['id_donacion'],
                    'id_venta': d['id_venta_completa'],
                    'monto': float(d['monto_redondeo']),
                    'fecha': str(fecha),
                    'hora': str(hora)
                })
            
            print(f"✓ Cargadas {len(self.donaciones)} donaciones")
        except Exception as e:
            print(f"Error cargando donaciones: {e}")
            self.donaciones = []
