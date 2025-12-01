from controllers.punto_venta_controller import PuntoVentaController
import tkinter as tk

# Mock MainApp and View for Controller init if needed, but Controller seems independent
# Controller init imports models.
# Let's try to instantiate Controller directly.

def verify_controller():
    try:
        controller = PuntoVentaController()
        print("Controller instantiated.")
        
        history = controller.obtener_historial_ventas()
        print(f"Fetched {len(history)} records.")
        
        if len(history) > 0:
            print("First record sample:")
            print(history[0])
            # Check format: (fecha, hora, total, redondeo, donacion)
            assert len(history[0]) == 5
            print("Format check passed.")
        else:
            print("No history found, but method executed without error.")
            
    except Exception as e:
        print(f"Verification failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_controller()
