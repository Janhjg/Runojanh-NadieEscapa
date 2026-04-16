import requests
try:
    print("Testing status...")
    r = requests.get("http://localhost:8001/status", timeout=5)
    print("Status:", r.json())
    print("Testing crimes...")
    r = requests.get("http://localhost:8001/crimes?limit=1", timeout=10)
    print("Crimes:", r.json())
except Exception as e:
    print("Error:", e)
