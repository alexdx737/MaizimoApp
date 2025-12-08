# Bitácora de Pruebas del Sistema Maizimo App

### 1. Pruebas de Conexión y Autenticación

| ID | Funcionalidad | Descripción | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado | Fechas |
|:---:|:---:|:---|:---|:---|:---|:---:|:---:|
| **AUTH-01** | Conexión BD | Verificar conexión a Supabase | Credenciales de entorno `.env` | Cliente Supabase creado exitosamente | Cliente creado exitosamente | **Éxito** | 06/12/2025 |
| **AUTH-02** | Login Exitoso | Validar credenciales correctas | Usuario: `1`<br>Password: `admin123` | Login exitoso, retorno de datos de usuario y rol | Login exitoso, datos correctos recuperados | **Éxito** | 06/12/2025 |
| **AUTH-03** | Login Fallido | Validar rechazo de credenciales incorrectas | Usuario: `999`<br>Password: `wrongpass` | Login fallido, retorno `None` o error | Login fallido, acceso denegado correctamente | **Éxito** | 06/12/2025 |
| **AUTH-04** | Datos Empleado | Verificar carga de datos de empleado al login | Usuario: `1` (Empleado vinculado) | Datos de nombre, CURP y rol cargados | Datos de empleado cargados correctamente | **Éxito** | 06/12/2025 |

### 2. Pruebas de Gestión de Inventario (CRUD)

| ID | Funcionalidad | Descripción | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado | Fechas |
|:---:|:---:|:---|:---|:---|:---|:---:|:---:|
| **INV-01** | Listar Productos | Obtener lista inicial de productos | N/A | Lista de productos > 0 o vacía (sin errores) | Lista obtenida correctamente (ej. 5 productos) | **Éxito** | 06/12/2025 |
| **INV-02** | Agregar Producto | Insertar un nuevo producto | Nombre: `Producto Test`<br>Stock: `100`<br>Precio: `50.0` | Producto insertado en BD, retorna `True` | Producto agregado correctamente | **Éxito** | 06/12/2025 |
| **INV-03** | Verificar Agregado | Confirmar existencia del nuevo producto | Búsqueda por nombre `Producto Test` | Producto encontrado en el inventario recargado | Producto encontrado en índice correcto | **Éxito** | 06/12/2025 |
| **INV-04** | Actualizar Producto | Modificar datos de producto existente | Nuevo Nombre: `Producto Test EDITADO`<br>Stock: `150` | Actualización exitosa en BD | Producto actualizado correctamente | **Éxito** | 06/12/2025 |
| **INV-05** | Verificar Edición | Confirmar persistencia de cambios | Búsqueda por nuevo nombre | Datos (Nombre/Stock) reflejan los cambios | Cambios de nombre y stock verificados | **Éxito** | 06/12/2025 |
| **INV-06** | Eliminar Producto | Borrar producto del inventario | ID de `Producto Test EDITADO` | Eliminación exitosa, retorna `True` | Producto eliminado correctamente | **Éxito** | 06/12/2025 |
| **INV-07** | Verificar Eliminación | Confirmar desaparición del registro | Búsqueda por nombre eliminado | Producto no encontrado en inventario | Producto ya no existe en el sistema | **Éxito** | 06/12/2025 |

### 3. Pruebas de Ventas y Donaciones

| ID | Funcionalidad | Descripción | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado | Fechas |
|:---:|:---:|:---|:---|:---|:---|:---:|:---:|
| **VTA-01** | Historial Ventas | Obtener historial completo de ventas | N/A | Lista de registros con fecha, total, redondeo, donación | Lista recuperada (ej. `N` registros) | **Éxito** | 06/12/2025 |
| **VTA-02** | Formato Historial | Validar estructura de registros de venta | Registro de venta | Tupla/Objeto con 5 campos (`fecha`, `hora`, `total`, `redondeo`, `donacion`) | Formato validado correctamente | **Éxito** | 06/12/2025 |
| **VTA-03** | Donación Cambio | Verificar cálculo de donación completa | Pago: `$100`<br>Total: `$95.50`<br>Opción: `Donar Cambio` | Donación: `$4.50`<br>Cambio Cliente: `$0.00` | Cálculo correcto, donación registrada | **Éxito** | 01/12/2025 |
| **VTA-04** | Redondeo Simple | Verificar redondeo normal (centavos) | Total: `$15.60` | Redondeo a: `$16.00`<br>Donación: `$0.40` | Redondeo aplicado correctamente | **Éxito** | 01/12/2025 |

### 4. Pruebas de Gestión de Usuarios (Clientes/Empleados)

| ID | Funcionalidad | Descripción | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado | Fechas |
|:---:|:---:|:---|:---|:---|:---|:---:|:---:|
| **USR-01** | Eliminar Cliente | Borrar registro de cliente mayorista | ID Cliente existente | Registro eliminado de BD | Cliente eliminado (verificado con Mock/BD) | **Éxito** | 06/12/2025 |
| **USR-02** | Eliminar Empleado | Borrar registro de empleado (inclusión) | ID Empleado existente | Registro eliminado de BD | Empleado eliminado (verificado con Mock/BD) | **Éxito** | 06/12/2025 |
| **USR-03** | Listar Vulnerables | Listar empleados en programa de inclusión | N/A | Lista de empleados con flag `vulnerable=True` | Lista filtrada correctamente | **Éxito** | 06/12/2025 |
