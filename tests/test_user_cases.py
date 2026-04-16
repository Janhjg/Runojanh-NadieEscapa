import urllib.request
import json
import urllib.parse
from pprint import pprint

# 1. Create a User Case by mimicking a POST to /predict/new
payload = {
    "DATE OCC": "04/14/2026 12:00:00 AM",
    "TIME OCC": 1500,
    "AREA NAME": "Central",
    "Rpt Dist No": 12,
    "Part 1-2": 1,
    "Crm Cd Desc": "HOMICIDE",
    "Vict Age": 44,
    "Vict Sex": "M",
    "Vict Descent": "H",
    "Premis Desc": "STREET",
    "Weapon Desc": "PISTOL",
    "Status Desc": "Investigating"
}

req = urllib.request.Request(
    "http://localhost:8001/predict/new",
    data=json.dumps(payload).encode('utf-8'),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as response:
        print("--- POST /predict/new ---")
        print(response.read().decode())
except Exception as e:
    print("Error POST /predict/new:", e)

# 2. Fetch User Cases
try:
    with urllib.request.urlopen("http://localhost:8001/user-cases") as response:
        print("\n--- GET /user-cases ---")
        res = json.loads(response.read().decode())
        print("Total User Cases:", res.get("total"))
        # Get the ID of the first one
        if res.get("cases"):
            user_case_id = res["cases"][0]["user_case_id"]
            print("First User Case ID:", user_case_id)
            
            # 3. Test classify_by_id with user case ID
            try:
                print(f"\n--- GET /classify/{user_case_id} ---")
                with urllib.request.urlopen(f"http://localhost:8001/classify/{user_case_id}") as r2:
                    d2 = json.loads(r2.read().decode())
                    print("Classify Output (snippet):", {k: v for k, v in d2.items() if k != "todas_etiquetas"})
            except Exception as e:
                import urllib.error
                if isinstance(e, urllib.error.HTTPError):
                    print("Error /classify:", e.code, e.read().decode())
                else:
                    print("Error /classify:", e)
except Exception as e:
    print("Error GET /user-cases:", e)
