import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def fetch_active_orders():
    """Retrieves all active orders from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/orders/")
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return []

def update_order(order_id: int, status: str, delay_reason: str):
    """Sends a PUT request to update an order's status."""
    payload = {
        "status": status,
        "delay_reason": delay_reason if delay_reason else None
    }
    try:
        response = requests.put(f"{BACKEND_URL}/orders/{order_id}/status", json=payload)
        return response.status_code == 200
    except Exception:
        return False