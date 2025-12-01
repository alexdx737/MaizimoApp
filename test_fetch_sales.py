from database import get_supabase_client
import json

def test_fetch_sales():
    try:
        supabase = get_supabase_client()
        
        # Try to fetch sales with donation info
        response = supabase.table('venta_completa')\
            .select('*, cliente(*), donacion(*)')\
            .order('fecha', desc=True)\
            .limit(5)\
            .execute()
            
        print("Successfully fetched sales:")
        print(json.dumps(response.data, indent=2, default=str))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_fetch_sales()
