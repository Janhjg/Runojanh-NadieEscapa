import urllib.request
import json
import re

try:
    with urllib.request.urlopen("http://localhost:3000/") as response:
        print("Frontend is working:", response.getcode())
except urllib.error.HTTPError as e:
    html = e.read().decode('utf-8')
    def extract_text(html):
        try:
            text = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
            text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            return ' '.join(text.split())
        except:
            return html[:1000]
    print(f"Frontend 500 Error details:\n{extract_text(html)[:2000]}")
except Exception as e:
    print(f"Other frontend error: {e}")

try:
    print("\nTesting Full Case with ID 10304468 (first crime in subset)")
    with urllib.request.urlopen("http://localhost:8001/full-case/10304468") as response:
        print("Full Case 10304468 SUCCESS")
except urllib.error.HTTPError as e:
    print("Full Case 10304468 ERROR:", e.code, e.read().decode('utf-8'))

# Test another ID
try:
    print("\nTesting Full Case with ID 190326475")
    with urllib.request.urlopen("http://localhost:8001/full-case/190326475") as response:
        print("Full Case 190326475 SUCCESS")
except urllib.error.HTTPError as e:
    print("Full Case 190326475 ERROR:", e.code, e.read().decode('utf-8'))
