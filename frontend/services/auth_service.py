import requests
from config import BASE_URL


def login(email: str, password: str) -> dict:
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )
        return response.json() if response.ok else {"error": response.json().get("detail", "Login failed.")}
    except Exception as e:
        return {"error": str(e)}


def register(email: str, password: str) -> dict:
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json={"email": email, "password": password}
        )
        return response.json() if response.ok else {"error": response.json().get("detail", "Registration failed.")}
    except Exception as e:
        return {"error": str(e)}