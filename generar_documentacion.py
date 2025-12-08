"""
Generador Mejorado de Documentación Técnica - Maizimo App
Genera documentación profesional, clara y bien organizada en PDF
"""

import os
import ast
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak, 
                                Table, TableStyle, ListFlowable, ListItem)
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

class MejoradoDocumentationGenerator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.content = []
        self.toc_entries = []
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Estadísticas
        self.stats = {
            'total_files': 0,
            'total_classes': 0,
            'total_functions': 0,
            'total_methods': 0,
            'total_constants': 0,
            'files_by_category': {}
        }
        
        # Mapa de dependencias
        self.file_dependencies = {}
        
        # Descripciones detalladas de archivos
        self.file_purposes = {
            # Archivos Core
            'login_view.py': {
                'purpose': 'Pantalla de inicio de sesión del sistema',
                'functionality': 'Valida credenciales del usuario y permite acceso al sistema principal. Incluye validación de campos, autenticación contra base de datos, y transición a la aplicación principal.',
                'key_features': ['Validación de credenciales', 'Interfaz gráfica de login', 'Carga de logo', 'Redirección a registro']
            },
            'main_view.py': {
                'purpose': 'Ventana principal de la aplicación con sistema de navegación',
                'functionality': 'Gestiona la navegación entre diferentes módulos del sistema. Muestra la barra de navegación, información del usuario, y carga dinámicamente las vistas según la selección.',
                'key_features': ['Sistema de navegación', 'Menú de perfil de usuario', 'Gestión de sesión', 'Carga dinámica de vistas']
            },
            'registro_view.py': {
                'purpose': 'Formulario de registro de nuevos usuarios y empleados',
                'functionality': 'Permite crear nuevos usuarios en el sistema. Valida todos los campos requeridos, crea primero el empleado y luego el usuario asociado en la base de datos.',
                'key_features': ['Validación de formulario', 'Creación de empleado', 'Creación de usuario', 'Scroll para formulario largo']
            },
            'database.py': {
                'purpose': 'Gestión centralizada de conexión a Supabase',
                'functionality': 'Implementa patrón singleton para mantener una única conexión a la base de datos. Carga credenciales y proporciona cliente de Supabase a todo el sistema.',
                'key_features': ['Patrón Singleton', 'Conexión a Supabase', 'Gestión de credenciales']
            },
            'config.py': {
                'purpose': 'Carga y gestión de variables de configuración',
                'functionality': 'Lee variables de entorno desde archivo .env y las proporciona al sistema. Valida que las variables críticas estén presentes.',
                'key_features': ['Carga de .env', 'Validación de configuración', 'Acceso a credenciales']
            },
            # Modelos
            'producto_model.py': {
                'purpose': 'Modelo de datos para productos del inventario',
                'functionality': 'Gestiona operaciones CRUD de productos. Interactúa con la tabla "producto" en Supabase para crear, leer, actualizar y eliminar productos.',
                'key_features': ['CRUD de productos', 'Consultas a Supabase', 'Validación de datos']
            },
            'venta_model.py': {
                'purpose': 'Modelo de datos para ventas y transacciones',
                'functionality': 'Registra ventas completas incluyendo items vendidos y donaciones. Maneja transacciones complejas con múltiples tablas relacionadas.',
                'key_features': ['Registro de ventas', 'Gestión de items', 'Cálculo de totales']
            },
            'cliente_model.py': {
                'purpose': 'Modelo de datos para clientes mayoristas',
                'functionality': 'Gestiona información de clientes con descuentos especiales. Permite consultar, crear y actualizar datos de clientes.',
                'key_features': ['CRUD de clientes', 'Gestión de descuentos', 'Consultas personalizadas']
            },
            'donacion_model.py': {
                'purpose': 'Modelo de datos para donaciones de redondeo',
                'functionality': 'Registra y consulta donaciones acumuladas del programa social. Calcula totales y proporciona estadísticas.',
                'key_features': ['Registro de donaciones', 'Cálculo de totales', 'Consultas de estadísticas']
            },
            'empleado_model.py': {
                'purpose': 'Modelo de datos para empleados',
                'functionality': 'Gestiona información de empleados del sistema, incluyendo empleados vulnerables del programa de inclusión laboral.',
                'key_features': ['CRUD de empleados', 'Gestión de vulnerabilidad', 'Datos de contratación']
            },
            'usuario_model.py': {
                'purpose': 'Modelo de datos para autenticación de usuarios',
                'functionality': 'Maneja autenticación y autorización. Valida credenciales y gestiona roles de usuario (trabajador/administrador).',
                'key_features': ['Validación de credenciales', 'Gestión de roles', 'Hash de contraseñas']
            },
            # Vistas
            'punto_venta_view.py': {
                'purpose': 'Interfaz de punto de venta para transacciones',
                'functionality': 'Vista principal para realizar ventas. Muestra productos, carrito, historial, y permite completar ventas con donaciones opcionales.',
                'key_features': ['Catálogo de productos', 'Carrito de compras', 'Procesamiento de ventas', 'Historial de ventas']
            },
            'gestion_operativa_view.py': {
                'purpose': 'Interfaz de gestión de inventario',
                'functionality': 'Permite administrar el catálogo de productos. Incluye funcionalidad para agregar, editar y eliminar productos.',
                'key_features': ['Tabla de productos', 'CRUD de productos', 'Búsqueda y filtros']
            },
            'clientes_mayoristas_view.py': {
                'purpose': 'Interfaz de gestión de clientes',
                'functionality': 'Administra base de datos de clientes mayoristas y sus descuentos. Permite crear y editar información de clientes.',
                'key_features': ['Tabla de clientes', 'CRUD de clientes', 'Gestión de descuentos']
            },
            'responsabilidad_social_view.py': {
                'purpose': 'Interfaz del programa social de donaciones',
                'functionality': 'Muestra estadísticas del programa de donaciones y permite actualizar datos. Calcula el equivalente en tortillas.',
                'key_features': ['Estadísticas de donaciones', 'Cálculo de equivalencias', 'Actualización de datos']
            },
            'inclusion_laboral_view.py': {
                'purpose': 'Interfaz del programa de inclusión laboral',
                'functionality': 'Gestiona información de empleados vulnerables. Muestra estadísticas y permite administrar el programa social.',
                'key_features': ['Tabla de empleados vulnerables', 'Estadísticas del programa', 'Gestión de ciclos']
            },
            # Controladores
            'punto_venta_controller.py': {
                'purpose': 'Lógica de negocio para punto de venta',
                'functionality': 'Coordina entre la vista de POS y los modelos. Procesa lógica de ventas, cálculos y actualización de inventario.',
                'key_features': ['Procesamiento de ventas', 'Validaciones de negocio', 'Coordinación modelo-vista']
            },
            'gestion_operativa_controller.py': {
                'purpose': 'Lógica de negocio para gestión de inventario',
                'functionality': 'Maneja operaciones de inventario. Valida datos de productos y coordina con el modelo.',
                'key_features': ['Validación de productos', 'Lógica de inventario', 'Coordinación CRUD']
            },
            'clientes_mayoristas_controller.py': {
                'purpose': 'Lógica de negocio para gestión de clientes',
                'functionality': 'Procesa operaciones relacionadas con clientes. Valida descuentos y coordina actualizaciones.',
                'key_features': ['Validación de clientes', 'Procesamiento de descuentos', 'Coordinación modelo-vista']
            },
            'responsabilidad_social_controller.py': {
                'purpose': 'Lógica de negocio para programa social',
                'functionality': 'Calcula estadísticas y equivalencias del programa de donaciones. Coordina consultas y actualizaciones.',
                'key_features': ['Cálculos de equivalencias', 'Estadísticas sociales', 'Coordinación de datos']
            },
            'inclusion_laboral_controller.py': {
                'purpose': 'Lógica de negocio para inclusión laboral',
                'functionality': 'Gestiona lógica del programa de empleados vulnerables. Procesa estadísticas y actualizaciones de ciclos.',
                'key_features': ['Gestión de ciclos', 'Estadísticas de empleados', 'Coordinación del programa']
            }
        }
        
        # Descripciones de propósito por categoría
        self.category_descriptions = {
            'core': 'Archivos fundamentales que inician y configuran la aplicación',
            'models': 'Modelos de datos que interactúan con la base de datos Supabase',
            'views': 'Interfaces de usuario construidas con Tkinter',
            'controllers': 'Lógica de negocio que conecta modelos y vistas'
        }
    
    def _setup_custom_styles(self):
        """Configurar estilos profesionales"""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#2C1810'),
            spaceAfter=20,
            spaceBefore=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Título de sección principal
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#FDB813'),
            spaceAfter=15,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Subsección (archivos individuales)
        self.styles.add(ParagraphStyle(
            name='FileTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#333333'),
            spaceAfter=10,
            spaceBefore=15,
            leftIndent=10,
            fontName='Helvetica-Bold'
        ))
        
        # Título de componente (clase, función)
        self.styles.add(ParagraphStyle(
            name='ComponentTitle',
            parent=self.styles['Heading3'],
            fontSize=13,
            textColor=colors.HexColor('#0066CC'),
            spaceAfter=8,
            leftIndent=20,
            fontName='Helvetica-Bold'
        ))
        
        # Descripción
        self.styles.add(ParagraphStyle(
            name='Description',
            parent=self.styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            leftIndent=30,
            rightIndent=20,
            spaceAfter=8,
            alignment=TA_JUSTIFY
        ))
        
        # Lista de items
        self.styles.add(ParagraphStyle(
            name='ListItem',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor('#555555'),
            leftIndent=40,
            spaceAfter=4
        ))
        
        # Código/parámetros
        self.styles.add(ParagraphStyle(
            name='CodeStyle',
            parent=self.styles['BodyText'],
            fontSize=10,
            fontName='Courier',
            textColor=colors.HexColor('#0066CC'),
            leftIndent=40,
            backColor=colors.HexColor('#F8F8F8'),
            spaceAfter=6
        ))
        
        # Nota/advertencia
        self.styles.add(ParagraphStyle(
            name='Note',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor('#666666'),
            leftIndent=30,
            fontName='Helvetica-Oblique',
            spaceAfter=10
        ))
    
    def analyze_file(self, filepath):
        """Analiza un archivo Python en detalle"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source)
            info = {
                'filepath': filepath,
                'filename': os.path.basename(filepath),
                'classes': [],
                'functions': [],
                'constants': [],
                'imports': [],
                'module_docstring': ast.get_docstring(tree)
            }
            
            # Analizar nodos
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = self._analyze_class(node)
                    info['classes'].append(class_info)
                
                elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                    func_info = self._analyze_function(node)
                    info['functions'].append(func_info)
                
                elif isinstance(node, ast.Assign) and node.col_offset == 0:
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id.isupper():
                            # Intentar obtener el valor
                            try:
                                value = ast.literal_eval(node.value)
                                info['constants'].append({
                                    'name': target.id,
                                    'value': value
                                })
                            except:
                                info['constants'].append({'name': target.id, 'value': None})
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            info['imports'].append(alias.name)
                    elif node.module:
                        info['imports'].append(node.module)
            
            return info
        except Exception as e:
            print(f"Error analizando {filepath}: {e}")
            return None
    
    def _analyze_class(self, node):
        """Analiza una clase en detalle"""
        class_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node),
            'methods': [],
            'class_attributes': []
        }
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._analyze_function(item)
                class_info['methods'].append(method_info)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        class_info['class_attributes'].append(target.id)
        
        return class_info
    
    def _analyze_function(self, node):
        """Analiza una función o método"""
        return {
            'name': node.name,
            'args': [arg.arg for arg in node.args.args],
            'docstring': ast.get_docstring(node),
            'is_property': any(isinstance(d, ast.Name) and d.id == 'property' 
                             for d in node.decorator_list) if hasattr(node, 'decorator_list') else False
        }
    
    def add_cover_page(self):
        """Página de portada profesional"""
        self.content.append(Spacer(1, 2*inch))
        
        # Título
        self.content.append(Paragraph(
            "Documentación Técnica Completa",
            self.styles['MainTitle']
        ))
        self.content.append(Spacer(1, 0.3*inch))
        
        # Subtítulo
        self.content.append(Paragraph(
            "Maizimo App",
            ParagraphStyle(
                'Subtitle',
                parent=self.styles['MainTitle'],
                fontSize=20,
                textColor=colors.HexColor('#FDB813')
            )
        ))
        self.content.append(Spacer(1, 0.5*inch))
        
        # Descripción del sistema
        self.content.append(Paragraph(
            "Sistema Integral de Gestión para Tortillería",
            self.styles['Heading3']
        ))
        self.content.append(Spacer(1, 0.3*inch))
        
        descripcion = """
        Este documento contiene la documentación técnica completa del sistema Maizimo App,
        incluyendo descripción detallada de todos los componentes, funciones, clases y 
        variables del proyecto. El sistema está construido con Python, Tkinter y Supabase,
        siguiendo el patrón arquitectónico MVC (Modelo-Vista-Controlador).
        """
        self.content.append(Paragraph(descripcion, self.styles['Description']))
        
        self.content.append(PageBreak())
    
    def add_architecture_overview(self):
        """Descripción de la arquitectura del sistema"""
        self.content.append(Paragraph(
            "1. Arquitectura del Sistema",
            self.styles['SectionTitle']
        ))
        self.content.append(Spacer(1, 0.2*inch))
        
        # Patrón MVC
        self.content.append(Paragraph(
            "Patrón MVC (Modelo-Vista-Controlador)",
            self.styles['ComponentTitle']
        ))
        
        mvc_desc = """
        El sistema utiliza el patrón arquitectónico MVC para separar responsabilidades:
        """
        self.content.append(Paragraph(mvc_desc, self.styles['Description']))
        
        # Tabla de componentes MVC
        mvc_data = [
            ['Componente', 'Ubicación', 'Responsabilidad'],
            ['Modelos', 'models/', 'Gestión de datos y acceso a base de datos Supabase'],
            ['Vistas', 'views/', 'Interfaz de usuario construida con Tkinter'],
            ['Controladores', 'controllers/', 'Lógica de negocio y flujo de la aplicación']
        ]
        
        mvc_table = Table(mvc_data, colWidths=[1.5*inch, 1.5*inch, 3.5*inch])
        mvc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FDB813')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F8F8')])
        ]))
        
        self.content.append(mvc_table)
        self.content.append(Spacer(1, 0.3*inch))
        
        # Stack tecnológico
        self.content.append(Paragraph(
            "Stack Tecnológico",
            self.styles['ComponentTitle']
        ))
        
        tech_items = [
            "<b>Python 3.11+</b>: Lenguaje de programación principal",
            "<b>Tkinter</b>: Framework para interfaces gráficas de usuario",
            "<b>Supabase</b>: Base de datos PostgreSQL en la nube",
            "<b>Pillow (PIL)</b>: Procesamiento y manejo de imágenes",
            "<b>python-dotenv</b>: Gestión segura de variables de entorno",
            "<b>ReportLab</b>: Generación de documentos PDF"
        ]
        
        for item in tech_items:
            self.content.append(Paragraph(f"• {item}", self.styles['ListItem']))
        
        self.content.append(PageBreak())
    
    def add_file_section(self, category, files_info, description):
        """Agrega una sección completa de archivos"""
        # Título de sección
        section_number = len([k for k in self.stats['files_by_category'].keys()]) + 2
        self.content.append(Paragraph(
            f"{section_number}. {category.title()}",
            self.styles['SectionTitle']
        ))
        self.content.append(Spacer(1, 0.15*inch))
        
        # Descripción de la categoría
        self.content.append(Paragraph(
            f"<i>{description}</i>",
            self.styles['Description']
        ))
        self.content.append(Spacer(1, 0.2*inch))
        
        # Documentar cada archivo
        for file_info in files_info:
            if file_info:
                self._document_file(file_info)
        
        self.content.append(PageBreak())
    
    def _document_file(self, file_info):
        """Documenta un archivo individual con detalle"""
        # Actualizar estadísticas
        self.stats['total_files'] += 1
        self.stats['total_constants'] += len(file_info['constants'])
        self.stats['total_functions'] += len(file_info['functions'])
        
        for cls in file_info['classes']:
            self.stats['total_classes'] += 1
            self.stats['total_methods'] += len(cls['methods'])
        
        filename = file_info['filename']
        
        # Título del archivo
        self.content.append(Paragraph(
            f"📄 {filename}",
            self.styles['FileTitle']
        ))
        
        # Ruta relativa
        rel_path = os.path.relpath(file_info['filepath'], self.project_root)
        self.content.append(Paragraph(
            f"<i>Ubicación: {rel_path}</i>",
            self.styles['Note']
        ))
        self.content.append(Spacer(1, 0.1*inch))
        
        # Información detallada del propósito si existe
        if filename in self.file_purposes:
            file_desc = self.file_purposes[filename]
            
            # Propósito
            self.content.append(Paragraph(
                "🎯 <b>Propósito:</b>",
                self.styles['ComponentTitle']
            ))
            self.content.append(Paragraph(
                file_desc['purpose'],
                self.styles['Description']
            ))
            self.content.append(Spacer(1, 0.05*inch))
            
            # Cómo funciona
            self.content.append(Paragraph(
                "⚙️ <b>Cómo Funciona:</b>",
                self.styles['ComponentTitle']
            ))
            self.content.append(Paragraph(
                file_desc['functionality'],
                self.styles['Description']
            ))
            self.content.append(Spacer(1, 0.05*inch))
            
            # Características clave
            self.content.append(Paragraph(
                "✨ <b>Características Clave:</b>",
                self.styles['ComponentTitle']
            ))
            for feature in file_desc['key_features']:
                self.content.append(Paragraph(
                    f"• {feature}",
                    self.styles['ListItem']
                ))
            self.content.append(Spacer(1, 0.1*inch))
        
        # Dependencias (imports) - Con qué se conecta
        if file_info['imports']:
            self.content.append(Paragraph(
                "🔗 <b>Dependencias (Archivos con los que se conecta):</b>",
                self.styles['ComponentTitle']
            ))
            
            # Organizar imports
            internal_imports = []
            external_imports = []
            
            for imp in file_info['imports']:
                if any(x in imp.lower() for x in ['models', 'views', 'controllers', 'database', 'config']):
                    internal_imports.append(imp)
                else:
                    external_imports.append(imp)
            
            if internal_imports:
                self.content.append(Paragraph(
                    "<b>Módulos internos del sistema:</b>",
                    self.styles['ListItem']
                ))
                for imp in internal_imports:
                    self.content.append(Paragraph(
                        f"  → {imp}",
                        self.styles['ListItem']
                    ))
            
            if external_imports:
                self.content.append(Paragraph(
                    "<b>Librerías externas:</b>",
                    self.styles['ListItem']
                ))
                for imp in external_imports[:10]:  # Limitar a 10 para no saturar
                    self.content.append(Paragraph(
                        f"  → {imp}",
                        self.styles['ListItem']
                    ))
            
            self.content.append(Spacer(1, 0.1*inch))
        
        # Constantes globales
        if file_info['constants']:
            self.content.append(Paragraph(
                "⚙️ <b>Constantes Globales</b>",
                self.styles['ComponentTitle']
            ))
            self.content.append(Paragraph(
                "Variables de configuración definidas en este archivo:",
                self.styles['Description']
            ))
            
            for const in file_info['constants']:
                const_text = f"<b>{const['name']}</b>"
                if const['value'] is not None:
                    const_text += f" = {repr(const['value'])}"
                self.content.append(Paragraph(f"• {const_text}", self.styles['ListItem']))
            
            self.content.append(Spacer(1, 0.1*inch))
        
        # Funciones de nivel superior
        if file_info['functions']:
            self.content.append(Paragraph(
                "🔧 <b>Funciones</b>",
                self.styles['ComponentTitle']
            ))
            self.content.append(Paragraph(
                "Funciones principales que este archivo proporciona:",
                self.styles['Description']
            ))
            
            for func in file_info['functions']:
                self._document_function(func)
        
        # Clases
        if file_info['classes']:
            self.content.append(Paragraph(
                "📦 <b>Clases</b>",
                self.styles['ComponentTitle']
            ))
            self.content.append(Paragraph(
                "Clases definidas en este archivo y su funcionalidad:",
                self.styles['Description']
            ))
            
            for cls in file_info['classes']:
                self._document_class(cls)
        
        self.content.append(Spacer(1, 0.25*inch))
    
    def _document_function(self, func_info):
        """Documenta una función con detalle"""
        args_str = ', '.join(func_info['args'])
        signature = f"{func_info['name']}({args_str})"
        
        self.content.append(Paragraph(
            f"<b>def {signature}</b>",
            self.styles['CodeStyle']
        ))
        
        if func_info['docstring']:
            self.content.append(Paragraph(
                f"→ {func_info['docstring']}",
                self.styles['Description']
            ))
        
        if func_info['args']:
            self.content.append(Paragraph(
                f"Parámetros: {', '.join(f'<i>{arg}</i>' for arg in func_info['args'])}",
                self.styles['ListItem']
            ))
        
        self.content.append(Spacer(1, 0.08*inch))
    
    def _document_class(self, class_info):
        """Documenta una clase con detalle"""
        self.content.append(Paragraph(
            f"<b>class {class_info['name']}</b>",
            self.styles['CodeStyle']
        ))
        
        if class_info['docstring']:
            self.content.append(Paragraph(
                f"→ {class_info['docstring']}",
                self.styles['Description']
            ))
        
        # Atributos de clase
        if class_info['class_attributes']:
            self.content.append(Paragraph(
                f"<b>Atributos de clase:</b> {', '.join(class_info['class_attributes'])}",
                self.styles['ListItem']
            ))
        
        # Métodos
        if class_info['methods']:
            self.content.append(Paragraph(
                "<b>Métodos:</b>",
                self.styles['ListItem']
            ))
            
            for method in class_info['methods']:
                args_str = ', '.join(method['args'])
                method_sig = f"{method['name']}({args_str})"
                
                method_text = f"  • <b>{method_sig}</b>"
                if method['docstring']:
                    method_text += f" - {method['docstring']}"
                
                self.content.append(Paragraph(method_text, self.styles['ListItem']))
        
        self.content.append(Spacer(1, 0.1*inch))
    
    def add_statistics_summary(self):
        """Resumen estadístico final"""
        self.content.append(Paragraph(
            "Resumen Estadístico del Sistema",
            self.styles['SectionTitle']
        ))
        self.content.append(Spacer(1, 0.3*inch))
        
        total_funcs_methods = self.stats['total_functions'] + self.stats['total_methods']
        
        # Tabla de estadísticas
        data = [
            ['Métrica', 'Cantidad', 'Descripción'],
            ['Archivos', str(self.stats['total_files']), 'Total de archivos Python documentados'],
            ['Clases', str(self.stats['total_classes']), 'Clases definidas en el sistema'],
            ['Funciones', str(self.stats['total_functions']), 'Funciones de nivel superior'],
            ['Métodos', str(self.stats['total_methods']), 'Métodos dentro de clases'],
            ['', '', ''],
            ['TOTAL FUNCIONES + MÉTODOS', str(total_funcs_methods), 'Total de funcionalidades ejecutables'],
            ['TOTAL VARIABLES', str(self.stats['total_constants']), 'Constantes y variables globales'],
        ]
        
        stats_table = Table(data, colWidths=[2*inch, 1.5*inch, 3*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FDB813')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 6), (-1, 7), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 6), (-1, 7), 14),
            ('TEXTCOLOR', (0, 6), (-1, 7), colors.HexColor('#2C1810')),
            ('BACKGROUND', (0, 6), (-1, 7), colors.HexColor('#FFF8E1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, 5), [colors.white, colors.HexColor('#F8F8F8')])
        ]))
        
        self.content.append(stats_table)
        self.content.append(Spacer(1, 0.3*inch))
        
        # Conclusión
        conclusion = f"""
        <b>Conclusión:</b> El sistema Maizimo App cuenta con un total de <b>{total_funcs_methods} funciones y métodos</b>, 
        organizados en <b>{self.stats['total_classes']} clases</b> distribuidas en <b>{self.stats['total_files']} archivos</b>. 
        Esto representa una base de código robusta y bien estructurada siguiendo principios de programación orientada a objetos 
        y el patrón MVC.
        """
        self.content.append(Paragraph(conclusion, self.styles['Description']))
    
    def generate(self, output_file):
        """Genera el PDF completo"""
        doc = SimpleDocTemplate(
            str(output_file),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=inch,
            bottomMargin=0.75*inch
        )
        
        # Construir contenido
        self.add_cover_page()
        self.add_architecture_overview()
        
        # Agregar estadísticas finales
        self.add_statistics_summary()
        
        # Generar PDF
        doc.build(self.content)
        print(f"✓ Documentación generada: {output_file}")


def main():
    """Función principal"""
    project_root = Path(__file__).parent
    output_file = project_root / "DOCUMENTACION_COMPLETA.pdf"
    
    print("=" * 60)
    print("GENERADOR DE DOCUMENTACIÓN TÉCNICA - MAIZIMO APP")
    print("=" * 60)
    
    gen = MejoradoDocumentationGenerator(project_root)
    
    # Categorías de archivos
    categories = {
        'Archivos Core': {
            'files': ['login_view.py', 'main_view.py', 'registro_view.py', 
                     'database.py', 'config.py'],
            'description': gen.category_descriptions['core']
        },
        'Modelos de Datos': {
            'folder': 'models',
            'description': gen.category_descriptions['models']
        },
        'Vistas de Usuario': {
            'folder': 'views',
            'description': gen.category_descriptions['views']
        },
        'Controladores': {
            'folder': 'controllers',
            'description': gen.category_descriptions['controllers']
        }
    }
    
    # Procesar categorías
    for category_name, category_info in categories.items():
        print(f"\n📁 {category_name}...")
        files_info = []
        
        if 'files' in category_info:
            # Archivos específicos
            for filename in category_info['files']:
                filepath = project_root / filename
                if filepath.exists():
                    print(f"  ✓ {filename}")
                    info = gen.analyze_file(filepath)
                    files_info.append(info)
        
        elif 'folder' in category_info:
            # Carpeta completa
            folder_path = project_root / category_info['folder']
            if folder_path.exists():
                for py_file in sorted(folder_path.glob('*.py')):
                    if py_file.name != '__init__.py':
                        print(f"  ✓ {py_file.name}")
                        info = gen.analyze_file(py_file)
                        files_info.append(info)
        
        # Agregar sección al PDF
        gen.add_file_section(category_name, files_info, category_info['description'])
        gen.stats['files_by_category'][category_name] = len(files_info)
    
    # Generar PDF
    print("\n" + "=" * 60)
    gen.generate(output_file)
    print("=" * 60)
    print(f"\n📊 ESTADÍSTICAS FINALES:")
    print(f"   • Archivos documentados: {gen.stats['total_files']}")
    print(f"   • Clases: {gen.stats['total_classes']}")
    print(f"   • Funciones: {gen.stats['total_functions']}")
    print(f"   • Métodos: {gen.stats['total_methods']}")
    print(f"   • Variables/Constantes: {gen.stats['total_constants']}")
    print(f"\n✅ Documentación completa generada exitosamente!")
    print(f"📄 Archivo: {output_file}\n")


if __name__ == "__main__":
    main()
