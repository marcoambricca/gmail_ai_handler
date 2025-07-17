from dotenv import load_dotenv
import os
import requests

load_dotenv()
print(os.getenv('STORE_ACCESS_TOKEN'))

def ProductosInfo():
    url = f"https://api.tiendanube.com/2025-03/{os.getenv('STORE_ID')}/products"
    headers = {
        "Authentication": f"bearer {os.getenv('STORE_ACCESS_TOKEN')}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("API error:", e)
        return {"error": "No se pudo obtener la información del producto."}

def EstadoCompra(id_order):
    url = f"https://api.tiendanube.com/2025-03/{os.getenv('STORE_ID')}/orders?number={id_order}"
    headers = {
            "Authentication": f"bearer {os.getenv('STORE_ACCESS_TOKEN')}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        orders = response.json()
        if not orders:
            return {"error": "No se encontró la orden."}

        order = orders[0]
        return {
            "shipping_status": order.get("shipping_status"),
            "tracking_code": order.get("fulfillments", [{}])[0].get("tracking_info", {}).get("code")
        }
    except Exception as e:
        print("API error:", e)
        return {"error": "No se pudo obtener el estado de la compra."}

available_functions = {
    "ProductosInfo": ProductosInfo,
    "EstadoCompra": EstadoCompra,
}

function_specs = [
    {
        "name": "ProductosInfo",
        "description": "Devuelve información de los productos de la tienda Tiendanube.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "EstadoCompra",
        "description": "Devuelve el estado y código de seguimiento de una compra específica.",
        "parameters": {
            "type": "object",
            "properties": {
                "id_order": {
                    "type": "integer",
                    "description": "Número de la orden a consultar"
                }
            },
            "required": ["id_order"]
        }
    }
]

