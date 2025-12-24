import requests

BASE_URL = "http://127.0.0.1:8000"

def get_products():
    r = requests.get(f"{BASE_URL}/products", timeout=10)
    r.raise_for_status()
    return r.json()

def add_product(data: dict):
    r = requests.post(f"{BASE_URL}/products", json=data, timeout=10)
    r.raise_for_status()
    return r.json()