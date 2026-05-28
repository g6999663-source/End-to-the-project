import requests
import json

url = "https://httpbin.org/delay/10"

try:
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    data = r.json()
    print("ok:", data["url"])
    
except requests.exceptions.Timeout:
    print("[ERROR] Запрос превысил время ожидания (timeout)")
except requests.exceptions.ConnectionError:
    print("[ERROR] Ошибка соединения")
except requests.exceptions.HTTPError as e:
    print(f"[ERROR] HTTP ошибка: {e.response.status_code}")
except json.JSONDecodeError:
    print("[ERROR] Ответ не является JSON")
except Exception as e:
    print(f"[ERROR] Ошибка: {e}")
