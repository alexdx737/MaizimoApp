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
    
    def obtener_datos_top_clientes(self, limit=10, dias=7):
        """
        Obtener datos para gráfico de Top Clientes por Ventas
        Args:
            limit: Número de clientes a mostrar (default: 10)
            dias: Días hacia atrás para consultar (default: 7)
        Returns: tuple (labels, values) para matplotlib
        """
        try:
            from models.venta_model import VentaModel
            from datetime import datetime, timedelta
            import pandas as pd
            
            # Calcular rango de fechas
            fecha_fin = datetime.now().date()
            fecha_inicio = fecha_fin - timedelta(days=dias)
            
            # Obtener ventas
            ventas = VentaModel.listar_ventas(
                fecha_inicio=fecha_inicio.isoformat(),
                fecha_fin=fecha_fin.isoformat(),
                limit=1000
            )
            
            # Agrupar por cliente
            ventas_data = []
            for venta in ventas:
                cliente_info = venta.get('cliente', {})
                cliente_nombre = f"{cliente_info.get('nombre', 'General')} {cliente_info.get('apellido_paterno', '')}".strip()
                total_venta = float(venta.get('monto_total', 0))
                ventas_data.append({'Cliente': cliente_nombre, 'Total': total_venta})
            
            if not ventas_data:
                return [], []
            
            df = pd.DataFrame(ventas_data)
            df_grouped = df.groupby('Cliente')['Total'].sum().sort_values(ascending=True).tail(limit)
            
            return df_grouped.index.tolist(), df_grouped.values.tolist()
            
        except Exception as e:
            print(f"Error obteniendo datos de top clientes: {e}")
            return [], []
    
    def obtener_datos_top_productos(self, limit=10, dias=7):
        """
        Obtener datos para gráfico de Top Productos Más Vendidos
        Args:
            limit: Número de productos a mostrar (default: 10)
            dias: Días hacia atrás para consultar (default: 7)
        Returns: tuple (labels, values) para matplotlib
        """
        try:
            from models.venta_model import VentaModel
            from datetime import datetime, timedelta
            import pandas as pd
            
            # Calcular rango de fechas
            fecha_fin = datetime.now().date()
            fecha_inicio = fecha_fin - timedelta(days=dias)
            
            # Obtener ventas
            ventas = VentaModel.listar_ventas(
                fecha_inicio=fecha_inicio.isoformat(),
                fecha_fin=fecha_fin.isoformat(),
                limit=1000
            )
            
            # Recopilar productos vendidos
            productos_data = []
            for venta in ventas:
                venta_detalle = VentaModel.obtener_venta_completa(venta['id_venta_completa'])
                if venta_detalle and venta_detalle.get('items'):
                    for item in venta_detalle['items']:
                        producto = item.get('producto', {})
                        productos_data.append({
                            'Producto': producto.get('nombre', 'N/A'),
                            'Total': round(item.get('subtotal', 0), 2)
                        })
            
            if not productos_data:
                return [], []
            
            df = pd.DataFrame(productos_data)
            df_grouped = df.groupby('Producto')['Total'].sum().sort_values(ascending=True).tail(limit)
            
            return df_grouped.index.tolist(), df_grouped.values.tolist()
            
        except Exception as e:
            print(f"Error obteniendo datos de top productos: {e}")
            return [], []
    
    def obtener_datos_distribucion(self, dias=7):
        """
        Obtener datos para gráfico de Distribución de Ingresos (Ventas vs Donaciones)
        Args:
            dias: Días hacia atrás para consultar (default: 7)
        Returns: tuple (labels, sizes, colors) para matplotlib pie chart
        """
        try:
            from models.venta_model import VentaModel
            from datetime import datetime, timedelta
            import pandas as pd
            
            # Calcular rango de fechas
            fecha_fin = datetime.now().date()
            fecha_inicio = fecha_fin - timedelta(days=dias)
            
            # Obtener ventas
            ventas = VentaModel.listar_ventas(
                fecha_inicio=fecha_inicio.isoformat(),
                fecha_fin=fecha_fin.isoformat(),
                limit=1000
            )
            
            total_ventas = 0.0
            total_donaciones = 0.0
            
            for venta in ventas:
                total_ventas += float(venta.get('monto_total', 0))
                
                # Obtener donaciones
                donaciones = venta.get('donacion', [])
                if isinstance(donaciones, list) and len(donaciones) > 0:
                    total_donaciones += float(donaciones[0].get('monto_redondeo', 0))
                elif isinstance(donaciones, dict):
                    total_donaciones += float(donaciones.get('monto_redondeo', 0))
            
            if total_ventas == 0 and total_donaciones == 0:
                return [], [], []
            
            labels = [f'Ventas\n${total_ventas:.2f}', f'Donaciones\n${total_donaciones:.2f}']
            sizes = [total_ventas, total_donaciones]
            colors = ['#3498DB', '#F39C12']
            
            return labels, sizes, colors
            
        except Exception as e:
            print(f"Error obteniendo datos de distribución: {e}")
            return [], [], []
