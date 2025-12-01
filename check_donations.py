from database import get_supabase_client
import json

def check_donations():
    try:
        supabase = get_supabase_client()
        
        # Fetch sales with donations
        response = supabase.table('venta_completa')\
            .select('*, donacion(*)')\
            .order('fecha', desc=True)\
            .limit(5)\
            .execute()
            
        print("Sales Data:")
        for sale in response.data:
            print(f"ID: {sale['id_venta_completa']}, Total: {sale['monto_total']}")
            print(f"Donacion field: {sale.get('donacion')}, Type: {type(sale.get('donacion'))}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_donations()
