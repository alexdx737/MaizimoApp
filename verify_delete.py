import sys
import os
from unittest.mock import MagicMock, patch

# Add current directory to path
sys.path.append(os.getcwd())

from controllers.clientes_mayoristas_controller import ClientesMayoristasController
from controllers.inclusion_laboral_controller import InclusionLaboralController

def test_delete_functionality():
    print("Testing delete functionality...")
    
    # --- Test 1: Delete Client ---
    print("\n1. Testing Client Deletion...")
    # Patch where it is imported
    with patch('controllers.clientes_mayoristas_controller.ClienteModel') as mock_cliente_model:
        # Setup initial state
        mock_cliente_model.listar_todos.return_value = [
            {'id_cliente': 1, 'nombre': 'Cliente', 'apellido_paterno': 'Uno', 'descuento': 0},
            {'id_cliente': 2, 'nombre': 'Cliente', 'apellido_paterno': 'Dos', 'descuento': 10}
        ]
        mock_cliente_model.eliminar.return_value = True
        
        controller = ClientesMayoristasController()
        print(f"   Initial clients: {len(controller.clientes)}")
        assert len(controller.clientes) == 2
        
        # Simulate delete
        print("   Deleting client ID 1...")
        # Update mock to return list without ID 1 after delete
        mock_cliente_model.listar_todos.side_effect = [
            [
                {'id_cliente': 1, 'nombre': 'Cliente', 'apellido_paterno': 'Uno', 'descuento': 0},
                {'id_cliente': 2, 'nombre': 'Cliente', 'apellido_paterno': 'Dos', 'descuento': 10}
            ],
            [
                {'id_cliente': 2, 'nombre': 'Cliente', 'apellido_paterno': 'Dos', 'descuento': 10}
            ]
        ]
        
        success = controller.eliminar_cliente(1)
        assert success is True
        print(f"   Clients after delete: {len(controller.clientes)}")
        assert len(controller.clientes) == 1
        assert controller.clientes[0]['id'] == 2
        print("   ✓ Client deletion verified")

    # --- Test 2: Delete Employee ---
    print("\n2. Testing Employee Deletion...")
    with patch('controllers.inclusion_laboral_controller.EmpleadoModel') as mock_empleado_model:
        # Setup initial state
        mock_empleado_model.listar_vulnerables.return_value = [
            {'id_empleado': 1, 'nombre': 'Emp', 'apellido_paterno': 'Uno', 'vulnerable': True},
            {'id_empleado': 2, 'nombre': 'Emp', 'apellido_paterno': 'Dos', 'vulnerable': True}
        ]
        mock_empleado_model.eliminar.return_value = True
        
        controller = InclusionLaboralController()
        print(f"   Initial employees: {len(controller.trabajadores)}")
        assert len(controller.trabajadores) == 2
        
        # Simulate delete
        print("   Deleting employee ID 1...")
        # Update mock
        mock_empleado_model.listar_vulnerables.side_effect = [
            [
                {'id_empleado': 1, 'nombre': 'Emp', 'apellido_paterno': 'Uno', 'vulnerable': True},
                {'id_empleado': 2, 'nombre': 'Emp', 'apellido_paterno': 'Dos', 'vulnerable': True}
            ],
            [
                {'id_empleado': 2, 'nombre': 'Emp', 'apellido_paterno': 'Dos', 'vulnerable': True}
            ]
        ]
        
        success = controller.eliminar_trabajador(1)
        assert success is True
        print(f"   Employees after delete: {len(controller.trabajadores)}")
        assert len(controller.trabajadores) == 1
        assert controller.trabajadores[0]['id'] == 2
        print("   ✓ Employee deletion verified")

if __name__ == "__main__":
    try:
        test_delete_functionality()
        print("\nAll tests passed!")
    except AssertionError as e:
        print(f"\n✗ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
