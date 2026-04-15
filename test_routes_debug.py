import urllib.request
import sys

try:
    with urllib.request.urlopen("http://localhost:8001/crimes?limit=2") as response:
        print("CRIMES:", response.read().decode()[0:500])
except Exception as e:
    print("CRIMES HTTP ERROR:", e)

try:
    with urllib.request.urlopen("http://localhost:8001/classify/125") as response:
        print("CLASSIFY:", response.read().decode()[0:500])
except Exception as e:
    import urllib.error
    if isinstance(e, urllib.error.HTTPError):
        print("CLASSIFY HTTP ERROR:", e.code, e.read().decode())
    else:
        print("CLASSIFY ERROR:", e)

try:
    with urllib.request.urlopen("http://localhost:8001/narrate/125") as response:
        print("NARRATE:", response.read().decode()[0:500])
except Exception as e:
    import urllib.error
    if isinstance(e, urllib.error.HTTPError):
        print("NARRATE HTTP ERROR:", e.code, e.read().decode())
    else:
        print("NARRATE ERROR:", e)
