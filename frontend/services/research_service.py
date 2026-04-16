import requests
from config import BASE_URL


def get_reports(token: str) -> list:
    try:
        response = requests.get(
            f"{BASE_URL}/research/reports",
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.json() if response.ok else []
    except Exception:
        return []


def get_report(token: str, report_id: str) -> dict:
    try:
        response = requests.get(
            f"{BASE_URL}/research/reports/{report_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.json() if response.ok else {}
    except Exception:
        return {}


def stream_research(token: str, topic: str):
    try:
        with requests.post(
            f"{BASE_URL}/research/stream",
            json={"topic": topic},
            headers={"Authorization": f"Bearer {token}"},
            stream=True,
            timeout=300
        ) as response:
            if not response.ok:
                error = response.json().get("detail", "Request failed.")
                yield ("error", error)
                return
            
            for line in response.iter_lines():
                if line:
                    decoded = line.decode("utf-8")
                    if decoded.startswith("data: "):
                        chunk = decoded[6:]
                        if chunk == "[DONE]":
                            yield ("done", "")
                        elif chunk.startswith("❌"):
                            yield ("error", chunk)
                        elif any(chunk.strip().startswith(e) for e in ["🔍", "📖", "🔬", "✍️"]):
                            yield ("status", chunk.strip())
                        else:
                            yield ("content", chunk)
    except Exception as e:
        yield ("error", str(e))