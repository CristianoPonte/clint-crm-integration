import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("CLINT_API_TOKEN")

headers = {
    "api-token": TOKEN,
    "Content-Type": "application/json"
}

resp = requests.get("https://api.clint.digital/v1/account/fields", headers=headers)
if resp.status_code == 200:
    import json
    print(json.dumps(resp.json(), indent=2))
else:
    print("Error:", resp.status_code, resp.text)
