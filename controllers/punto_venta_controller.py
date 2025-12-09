class PuntoVentaController:
    """Controller de la sección Punto de Venta.

    Maneja el estado del carrito, descuentos y cálculo de totales.
    Conectado a Supabase para productos y ventas.
    """

    def __init__(self):
        from models.producto_model import ProductoModel
        from models.venta_model import VentaModel
        from models.cliente_model import ClienteModel
        
        self.ProductoModel = ProductoModel
        self.VentaModel = VentaModel
        self.ClienteModel = ClienteModel
        
        # Cargar productos desde Supabase
        self.productos = []
        self.productos_filtrados = []  # Para búsqueda
        self.cargar_productos()

        # Cargar clientes para selección
        self.clientes = []
        self.cargar_clientes()
        
        # Cliente seleccionado (default: cliente general ID 1)
        self.id_cliente_seleccionado = 1
        self.descuento_cliente = 0.0  # Porcentaje de descuento

        # Carrito: lista de dicts {id_producto, nombre, precio, cantidad, unidad_medida}
        self.carrito = []

        self.bolsa = False
        self.redondeo = False
    
    def cargar_productos(self):
        """Cargar productos desde Supabase"""
        try:
            productos_db = self.ProductoModel.listar_todos()
            self.productos = [
                {
                    'id_producto': p['id_producto'],
                    'nombre': p['nombre'],
                    'precio': float(p['costo_unitario']),
                    'stock': float(p['stock']),
                    'unidad_medida': p['unidad_medida']
                }
                for p in productos_db
            ]
        except Exception as e:
            print(f"Error cargando productos: {e}")
            # Fallback a productos por defecto
            self.productos = [
                {'id_producto': 1, 'nombre': 'Tortillas (kg)', 'precio': 25.0, 'stock': 100, 'unidad_medida': 'kg'},
                {'id_producto': 2, 'nombre': 'Tostadas (paquete)', 'precio': 15.0, 'stock': 50, 'unidad_medida': 'pz'},
                {'id_producto': 4, 'nombre': 'Tamales', 'precio': 12.0, 'stock': 25, 'unidad_medida': 'pz'},
            ]
        
        # Inicializar productos filtrados con todos los productos
        self.productos_filtrados = self.productos[:]
    
    def cargar_clientes(self):
        """Cargar clientes desde Supabase"""
        try:
            clientes_db = self.ClienteModel.listar_todos()
            self.clientes = [
                {
                    'id': c['id_cliente'],
                    'nombre': f"{c['nombre']} {c['apellido_paterno']}",
                    'descuento': float(c['descuento'])
                }
                for c in clientes_db
            ]
            print(f"✓ Cargados {len(self.clientes)} clientes")
        except Exception as e:
            print(f"Error cargando clientes: {e}")
            self.clientes = [{'id': 1, 'nombre': 'Cliente General', 'descuento': 0.0}]
    
    def set_cliente(self, id_cliente):
        """Establecer cliente seleccionado y su descuento"""
        self.id_cliente_seleccionado = id_cliente
        
        # Buscar descuento del cliente
        for cliente in self.clientes:
            if cliente['id'] == id_cliente:
                self.descuento_cliente = cliente['descuento']
                print(f"✓ Cliente seleccionado: {cliente['nombre']}, Descuento: {self.descuento_cliente}%")
                return
        
        # Si no se encuentra, usar cliente general
        self.descuento_cliente = 0.0
    
    def filtrar_productos(self, termino):
        """Filtrar productos por nombre o ID"""
        if not termino or termino.strip() == "":
            # Si no hay término, mostrar todos
            self.productos_filtrados = self.productos[:]
        else:
            termino = termino.lower().strip()
            self.productos_filtrados = []
            
            for p in self.productos:
                # Buscar por nombre
                if termino in p['nombre'].lower():
                    self.productos_filtrados.append(p)
                # Buscar por ID (convertir a string)
                elif termino in str(p['id_producto']):
                    self.productos_filtrados.append(p)
        
        print(f"✓ Filtrados {len(self.productos_filtrados)} productos")

    # --- Operaciones sobre el carrito ---
    def agregar_al_carrito(self, nombre):
        producto = self._obtener_producto(nombre)
        if producto is None:
            return
        for item in self.carrito:
            if item["nombre"] == nombre:
                item["cantidad"] += 1
                break
        else:
            self.carrito.append({
                "id_producto": producto['id_producto'],
                "nombre": producto['nombre'],
                "precio": producto['precio'],
                "cantidad": 1,
                "unidad_medida": producto['unidad_medida']
            })

    def cambiar_cantidad(self, indice, delta):
        if indice < 0 or indice >= len(self.carrito):
            return
        item = self.carrito[indice]
        item["cantidad"] += delta
        if item["cantidad"] <= 0:
            self.carrito.pop(indice)

    def eliminar_item(self, indice):
        if 0 <= indice < len(self.carrito):
            self.carrito.pop(indice)

    def limpiar_carrito(self):
        self.carrito = []

    # --- Flags de descuento / redondeo ---
    def set_bolsa(self, valor: bool):
        self.bolsa = bool(valor)

    def set_redondeo(self, valor: bool):
        self.redondeo = bool(valor)

    # --- Cálculo de totales ---
    def calcular_totales(self):
        subtotal = sum(item["precio"] * item["cantidad"] for item in self.carrito)

        # Descuento por bolsa
        descuento_bolsa = 2.0 if self.bolsa and subtotal >= 2.0 else 0.0
        
        # Descuento de cliente mayorista (porcentaje)
        descuento_cliente_monto = (subtotal * self.descuento_cliente) / 100.0
        
        # Total de descuentos
        descuento_total = descuento_bolsa + descuento_cliente_monto
        
        total = max(subtotal - descuento_total, 0.0)

        return subtotal, total, descuento_cliente_monto

    def procesar_venta(self, monto_pago=0):
        """
        Procesar y guardar la venta en Supabase
        Args:
            id_cliente: ID del cliente (default: 1 para cliente general)
            monto_pago: Monto con el que paga el cliente
        Returns: ID de venta_completa o None
        """
        if not self.carrito:
            print("Carrito vacío, no se puede procesar venta")
            return None

        # 1. Verificar stock antes de intentar la venta
        for item in self.carrito:
            producto_b = self._obtener_producto_por_id(item['id_producto'])
            if not producto_b:
                print(f"Producto {item['nombre']} no encontrado en lista local")
                continue
            
            if item['cantidad'] > producto_b['stock']:
                # Esto debería manejarse con una excepción o retorno especial para UI
                print(f"Stock insuficiente para {item['nombre']}")
                raise ValueError(f"Stock insuficiente para {item['nombre']}. Disponible: {producto_b['stock']}")
        
        try:
            id_venta = self.VentaModel.procesar_venta(
                carrito=self.carrito,
                id_cliente=self.id_cliente_seleccionado,
                descuento_bolsa=self.bolsa,
                redondeo=self.redondeo,
                monto_pago=monto_pago
            )
            
            if id_venta:
                print(f"✓ Venta procesada exitosamente: ID {id_venta}")
                self.limpiar_carrito()
                # Recargar productos para actualizar stock local
                self.cargar_productos()
                return id_venta
            else:
                print("✗ Error procesando venta")
                return None
                
        except Exception as e:
            print(f"Error en procesar_venta: {e}")
            return None

    # --- auxiliares internos ---
    def _obtener_producto(self, nombre):
        """Obtener producto completo por nombre"""
        for producto in self.productos:
            if producto['nombre'] == nombre:
                return producto
        return None

    def _obtener_producto_por_id(self, id_producto):
        for producto in self.productos:
            if producto['id_producto'] == id_producto:
                return producto
        return None
    
    def _obtener_precio(self, nombre):
        """Obtener precio de producto por nombre (legacy)"""
        producto = self._obtener_producto(nombre)
        return producto['precio'] if producto else None

    def obtener_historial_ventas(self):
        """Obtener historial completo de ventas formateado para la vista"""
        ventas = self.VentaModel.listar_ventas(limit=50) # Limit 50 for now, maybe more? User said "historial de ventas", not just today.
        
        datos_formateados = []
        for v in ventas:
            # Formatear fecha y hora
            fecha = v.get('fecha', '')
            hora = v.get('hora', '')[:5] if v.get('hora') else ''
            
            # Formatear total
            total = float(v.get('monto_total', 0))
            
            # Verificar donación
            donaciones = v.get('donacion', [])
            # Supabase might return None, [], or object. Handle list.
            if isinstance(donaciones, list) and len(donaciones) > 0:
                redondeo = "Sí"
                monto_donacion = float(donaciones[0].get('monto_redondeo', 0))
            elif isinstance(donaciones, dict): # Should not happen with 1:N but just in case
                redondeo = "Sí"
                monto_donacion = float(donaciones.get('monto_redondeo', 0))
            else:
                redondeo = "No"
                monto_donacion = 0.0
                
            datos_formateados.append((
                v['id_venta_completa'],
                fecha,
                hora,
                f"${total:.2f}",
                redondeo,
                f"${monto_donacion:.2f}"
            ))
            
        return datos_formateados

    def obtener_detalle_venta(self, id_venta):
        """Obtener detalle completo de una venta"""
        return self.VentaModel.obtener_venta_completa(id_venta)
    
    def generar_reporte_semanal(self, ruta_archivo):
        """
        Generar reporte semanal completo en PDF con gráficos y tablas
        Args:
            ruta_archivo: Ruta donde guardar el archivo PDF
        Returns: True si se generó correctamente, False en caso contrario
        """
        try:
            import pandas as pd
            from datetime import datetime, timedelta
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')
            import io
            
            # Calcular rango de la semana actual
            hoy = datetime.now().date()
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            fin_semana = inicio_semana + timedelta(days=6)
            
            # Obtener ventas
            ventas = self.VentaModel.listar_ventas(
                fecha_inicio=inicio_semana.isoformat(),
                fecha_fin=fin_semana.isoformat(),
                limit=1000
            )
            
            # Preparar datos con pandas
            ventas_data = []
            productos_data = []
            donaciones_data = []
            
            for venta in ventas:
                venta_detalle = self.VentaModel.obtener_venta_completa(venta['id_venta_completa'])
                cliente_info = venta.get('cliente', {})
                cliente_nombre = f"{cliente_info.get('nombre', 'General')} {cliente_info.get('apellido_paterno', '')}".strip()
                descuento_cliente_pct = float(cliente_info.get('descuento', 0))
                
                subtotal_items = 0.0
                if venta_detalle and venta_detalle.get('items'):
                    subtotal_items = sum(item.get('subtotal', 0) for item in venta_detalle['items'])
                
                descuento_cliente_monto = subtotal_items * descuento_cliente_pct / 100
                total_venta = float(venta.get('monto_total', 0))
                descuento_bolsa_monto = max(subtotal_items - descuento_cliente_monto - total_venta, 0)
                
                donaciones = venta.get('donacion', [])
                donacion_monto = 0.0
                if isinstance(donaciones, list) and len(donaciones) > 0:
                    donacion_monto = float(donaciones[0].get('monto_redondeo', 0))
                elif isinstance(donaciones, dict):
                    donacion_monto = float(donaciones.get('monto_redondeo', 0))
                
                ventas_data.append({
                    'ID': venta['id_venta_completa'],
                    'Fecha': venta.get('fecha', ''),
                    'Cliente': cliente_nombre,
                    'Subtotal': round(subtotal_items, 2),
                    'Total': round(total_venta, 2),
                    'Donación': round(donacion_monto, 2)
                })
                
                if venta_detalle and venta_detalle.get('items'):
                    for item in venta_detalle['items']:
                        producto = item.get('producto', {})
                        productos_data.append({
                            'Producto': producto.get('nombre', 'N/A'),
                            'Cantidad': item.get('cantidad_vendida', 0),
                            'Precio': round(item.get('subtotal', 0) / item.get('cantidad_vendida', 1), 2),
                            'Total': round(item.get('subtotal', 0), 2)
                        })
                
                if donacion_monto > 0:
                    donaciones_data.append({
                        'ID': venta['id_venta_completa'],
                        'Cliente': cliente_nombre,
                        'Monto': round(donacion_monto, 2)
                    })
            
            df_ventas = pd.DataFrame(ventas_data)
            df_productos = pd.DataFrame(productos_data)
            df_donaciones = pd.DataFrame(donaciones_data)
            
            # Crear PDF
            doc = SimpleDocTemplate(ruta_archivo, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Estilos personalizados
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2C3E50'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#34495E'),
                spaceAfter=12,
                spaceBefore=12
            )
            
            # ===== PORTADA =====
            story.append(Spacer(1, 2*inch))
            story.append(Paragraph("REPORTE SEMANAL DE VENTAS", title_style))
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph(f"Semana del {inicio_semana.strftime('%d/%m/%Y')} al {fin_semana.strftime('%d/%m/%Y')}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
            story.append(PageBreak())
            
            # ===== RESUMEN EJECUTIVO =====
            story.append(Paragraph("RESUMEN EJECUTIVO", heading_style))
            story.append(Spacer(1, 0.2*inch))
            
            metricas = [
                ['Métrica', 'Valor'],
                ['Total de Ventas', str(len(ventas))],
                ['Ingresos Totales', f"${df_ventas['Total'].sum():.2f}" if not df_ventas.empty else "$0.00"],
                ['Donaciones Recibidas', f"${df_ventas['Donación'].sum():.2f}" if not df_ventas.empty else "$0.00"],
                ['Ticket Promedio', f"${df_ventas['Total'].mean():.2f}" if not df_ventas.empty else "$0.00"],
                ['Productos Vendidos', str(len(df_productos))]
            ]
            
            t = Table(metricas, colWidths=[3*inch, 2*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(t)
            story.append(PageBreak())
            
            # ===== GRÁFICOS =====
            story.append(Paragraph("ANÁLISIS VISUAL", heading_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Gráfico 1: Ventas por Cliente
            if not df_ventas.empty:
                df_por_cliente = df_ventas.groupby('Cliente')['Total'].sum().sort_values(ascending=False).head(10)
                
                fig, ax = plt.subplots(figsize=(8, 5))
                df_por_cliente.plot(kind='barh', ax=ax, color='#3498DB')
                ax.set_xlabel('Total Vendido ($)', fontweight='bold')
                ax.set_title('Top 10 Clientes por Ventas', fontweight='bold', fontsize=14)
                ax.grid(axis='x', alpha=0.3)
                plt.tight_layout()
                
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
                img_buffer.seek(0)
                img = Image(img_buffer, width=6*inch, height=3.5*inch)
                story.append(img)
                plt.close()
                story.append(Spacer(1, 0.3*inch))
            
            # Gráfico 2: Top Productos
            if not df_productos.empty:
                df_top_prod = df_productos.groupby('Producto')['Total'].sum().sort_values(ascending=False).head(10)
                
                fig, ax = plt.subplots(figsize=(8, 5))
                df_top_prod.plot(kind='barh', ax=ax, color='#2ECC71')
                ax.set_xlabel('Ingresos ($)', fontweight='bold')
                ax.set_title('Top 10 Productos Más Vendidos', fontweight='bold', fontsize=14)
                ax.grid(axis='x', alpha=0.3)
                plt.tight_layout()
                
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
                img_buffer.seek(0)
                img = Image(img_buffer, width=6*inch, height=3.5*inch)
                story.append(img)
                plt.close()
            
            story.append(PageBreak())
            
            # Gráfico 3: Distribución
            if not df_ventas.empty:
                total_ventas_sum = df_ventas['Total'].sum()
                total_donaciones_sum = df_ventas['Donación'].sum()
                
                fig, ax = plt.subplots(figsize=(7, 5))
                sizes = [total_ventas_sum, total_donaciones_sum]
                labels = [f'Ventas\n${total_ventas_sum:.2f}', f'Donaciones\n${total_donaciones_sum:.2f}']
                colors_pie = ['#3498DB', '#F39C12']
                
                ax.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%',
                      startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
                ax.set_title('Distribución de Ingresos', fontweight='bold', fontsize=14)
                plt.tight_layout()
                
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
                img_buffer.seek(0)
                img = Image(img_buffer, width=5*inch, height=4*inch)
                story.append(img)
                plt.close()
            
            story.append(PageBreak())
            
            # ===== TABLAS DETALLADAS =====
            story.append(Paragraph("VENTAS DETALLADAS", heading_style))
            story.append(Spacer(1, 0.2*inch))
            
            if not df_ventas.empty:
                ventas_table_data = [['ID', 'Fecha', 'Cliente', 'Subtotal', 'Total', 'Donación']]
                for _, row in df_ventas.iterrows():
                    ventas_table_data.append([
                        str(row['ID']),
                        row['Fecha'],
                        row['Cliente'][:20],
                        f"${row['Subtotal']:.2f}",
                        f"${row['Total']:.2f}",
                        f"${row['Donación']:.2f}"
                    ])
                
                t = Table(ventas_table_data, colWidths=[0.6*inch, 1*inch, 2*inch, 1*inch, 1*inch, 1*inch])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ECC71')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
                ]))
                story.append(t)
            
            story.append(PageBreak())
            
            # Tabla de Productos
            story.append(Paragraph("PRODUCTOS VENDIDOS", heading_style))
            story.append(Spacer(1, 0.2*inch))
            
            if not df_productos.empty:
                prod_table_data = [['Producto', 'Cantidad', 'Precio Unit.', 'Total']]
                for _, row in df_productos.head(50).iterrows():
                    prod_table_data.append([
                        row['Producto'][:30],
                        str(row['Cantidad']),
                        f"${row['Precio']:.2f}",
                        f"${row['Total']:.2f}"
                    ])
                
                t = Table(prod_table_data, colWidths=[3*inch, 1*inch, 1.2*inch, 1.2*inch])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
                ]))
                story.append(t)
            
            # Tabla de Donaciones
            if not df_donaciones.empty:
                story.append(PageBreak())
                story.append(Paragraph("DONACIONES REGISTRADAS", heading_style))
                story.append(Spacer(1, 0.2*inch))
                
                don_table_data = [['ID Venta', 'Cliente', 'Monto Donado']]
                for _, row in df_donaciones.iterrows():
                    don_table_data.append([
                        str(row['ID']),
                        row['Cliente'][:30],
                        f"${row['Monto']:.2f}"
                    ])
                
                don_table_data.append(['', 'TOTAL:', f"${df_donaciones['Monto'].sum():.2f}"])
                
                t = Table(don_table_data, colWidths=[1*inch, 3.5*inch, 1.5*inch])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F39C12')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey]),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F39C12')),
                    ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold')
                ]))
                story.append(t)
            
            # Construir PDF
            doc.build(story)
            
            print(f"✓ Reporte PDF generado: {ruta_archivo}")
            print(f"  - {len(ventas)} ventas procesadas")
            print(f"  - {len(df_productos)} productos vendidos")
            print(f"  - {len(df_donaciones)} donaciones registradas")
            return True
            
        except Exception as e:
            print(f"Error generando reporte PDF: {e}")
            import traceback
            traceback.print_exc()
            return False

            print(f"  - {len(df_donaciones)} donaciones registradas")
            return True
            
        except Exception as e:
            print(f"Error generando reporte PDF: {e}")
            import traceback
            traceback.print_exc()
            return False
            return False
