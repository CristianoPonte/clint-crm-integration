import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

CLINT_API_TOKEN = os.getenv("CLINT_API_TOKEN")
BASE_URL = "https://api.clint.digital/v1"

HEADERS = {
    "api-token": f"{CLINT_API_TOKEN}",
    "Content-Type": "application/json"
}

def get_origin_id_by_name(origin_name: str) -> str:
    url = f"{BASE_URL}/origins?limit=250"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    result = response.json()
    origins = result.get("data", [])
    
    search_name = origin_name.strip().upper()
    for origin in origins:
        current_name = str(origin.get("name", "")).strip().upper()
        if current_name == search_name:
            return origin.get("id")
            
    raise ValueError(f"Origin '{origin_name}' not found. Disponíveis: {[o.get('name') for o in origins[:5]]}...")

def get_base_stage_id(origin_id: str) -> str:
    url = f"{BASE_URL}/origins?limit=250"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    result = response.json()
    origins = result.get("data", [])
    
    for origin in origins:
        if origin.get("id") == origin_id:
            stages = origin.get("stages", [])
            for stage in stages:
                if stage.get("type") == "BASE":
                    return stage.get("id")
            if stages:
                return stages[0].get("id")
            
    raise ValueError(f"Origin with ID '{origin_id}' not found or has no stages.")

def upsert_contact(name: str, email: str, phone_raw: str, custom_fields: dict) -> str:
    url = f"{BASE_URL}/contacts"
    
    phone_clean = re.sub(r'\D', '', str(phone_raw))
    if phone_clean.startswith("55") and len(phone_clean) > 11:
        ddi = "+55"
        phone = phone_clean[2:]
    elif len(phone_clean) >= 10:
        ddi = "+55"
        phone = phone_clean
    else:
        ddi = ""
        phone = ""
    
    fields = {k: v for k, v in custom_fields.items() if v}
    
    payload = {
        "name": name,
        "email": email,
        "fields": fields
    }
    
    if phone:
        payload["phone"] = phone
        if ddi:
            payload["ddi"] = ddi

    # Tenta encontrar contato por Email
    contact_id = None
    search_email = requests.get(url, headers=HEADERS, params={"email": email})
    if search_email.status_code == 200:
        data = search_email.json()
        if data.get("totalCount", 0) > 0 and data.get("data"):
            contact_id = data["data"][0]["id"]

    # Se não achou por Email e tem Telefone, tenta por Telefone
    if not contact_id and phone:
        search_phone = requests.get(url, headers=HEADERS, params={"phone": phone})
        if search_phone.status_code == 200:
            data = search_phone.json()
            if data.get("totalCount", 0) > 0 and data.get("data"):
                contact_id = data["data"][0]["id"]

    if contact_id:
        # Atualizar existente (Sobrescrevendo campos conforme regra)
        update_url = f"{url}/{contact_id}"
        update_resp = requests.post(update_url, headers=HEADERS, json=payload)
        update_resp.raise_for_status()
        return contact_id
    else:
        # Criar novo
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("data", {}).get("id") if result.get("data") else result.get("id")
        
    return ""

def add_tag_to_contact(contact_id: str, tag_name: str):
    url = f"{BASE_URL}/contacts/{contact_id}/tags"
    payload = [tag_name]
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()

def create_deal(contact_id: str, stage_id: str, origin_id: str, title: str, value: float, custom_fields: dict = None):
    url = f"{BASE_URL}/deals"
    payload = {
        "contact_id": contact_id,
        "stage_id": stage_id,
        "origin_id": origin_id,
        "title": title,
        "value": value
    }
    
    if custom_fields:
        payload["fields"] = {k: v for k, v in custom_fields.items() if v}

    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    result = response.json()
    return result.get("data", {}).get("id") if result.get("data") else result.get("id")
