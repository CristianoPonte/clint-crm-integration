import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("CLINT_API_TOKEN")
BASE_URL = "https://api.clint.digital/v1"

headers = {
    "api-token": TOKEN,
    "Content-Type": "application/json"
}

email_to_test = "test@test.com"
resp = requests.get(f"{BASE_URL}/contacts", headers=headers, params={"email": email_to_test})
print("GET /contacts?search=status:", resp.status_code)
if resp.status_code == 200:
    data = resp.json()
    print("Found total", data.get("totalCount"))
    if data.get("data"):
        print("First contact ID:", data["data"][0].get("id"))
else:
    print(resp.text)
