import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from controllers.punto_venta_controller import PuntoVentaController
from unittest.mock import MagicMock, patch

def test_refresh_clients():
    print("Testing client refresh mechanism...")
    
    # Mock dependencies
    with patch('models.producto_model.ProductoModel') as mock_prod_model, \
         patch('models.venta_model.VentaModel') as mock_venta_model, \
         patch('models.cliente_model.ClienteModel') as mock_cliente_model:
        
        # Setup initial state
        mock_prod_model.listar_todos.return_value = []
        mock_cliente_model.listar_todos.return_value = [
            {'id_cliente': 1, 'nombre': 'Cliente', 'apellido_paterno': 'Uno', 'descuento': 0}
        ]
        
        # Initialize controller
        controller = PuntoVentaController()
        print(f"Initial clients: {len(controller.clientes)}")
        assert len(controller.clientes) == 1
        assert controller.clientes[0]['nombre'] == "Cliente Uno"
        
        # Simulate database update (add a new client)
        print("Simulating database update...")
        mock_cliente_model.listar_todos.return_value = [
            {'id_cliente': 1, 'nombre': 'Cliente', 'apellido_paterno': 'Uno', 'descuento': 0},
            {'id_cliente': 2, 'nombre': 'Cliente', 'apellido_paterno': 'Dos', 'descuento': 10}
        ]
        
        # Call reload (this is what the view does now)
        print("Calling cargar_clientes()...")
        controller.cargar_clientes()
        
        # Verify update
        print(f"Clients after reload: {len(controller.clientes)}")
        assert len(controller.clientes) == 2
        assert controller.clientes[1]['nombre'] == "Cliente Dos"
        print("✓ Verification successful: Client list updated correctly.")

if __name__ == "__main__":
    try:
        test_refresh_clients()
    except AssertionError as e:
        print(f"✗ Verification failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ An error occurred: {e}")
        sys.exit(1)
