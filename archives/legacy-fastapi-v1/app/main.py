from fastapi import FastAPI, Request, File, Form, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import io
import json
import uuid
from datetime import datetime
from pathlib import Path
from services import clint_service, mapper_service

HISTORICO_PATH = Path("historico.json")

def salvar_historico(entrada: dict):
    historico = []
    if HISTORICO_PATH.exists():
        try:
            historico = json.loads(HISTORICO_PATH.read_text(encoding="utf-8"))
        except Exception:
            historico = []
    historico.insert(0, entrada)  # mais recente primeiro
    HISTORICO_PATH.write_text(json.dumps(historico, indent=2, ensure_ascii=False), encoding="utf-8")

app = FastAPI(title="Integrador CSV > Clint API")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_leads(
    csv_file: UploadFile = File(...),
    origin_name: str = Form(...),
    product_name: str = Form(...),
    product_value: float = Form(...),
    list_tag_name: str = Form(...)
):
    try:
        origin_id = clint_service.get_origin_id_by_name(origin_name)
        stage_id = clint_service.get_base_stage_id(origin_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao identificar Destino: {str(e)}")

    try:
        content = await csv_file.read()
        # Better separator detection: check first line for ';'
        first_line = content.decode('utf-8', errors='ignore').split('\n')[0]
        separator = ';' if ';' in first_line else ','
        
        df = pd.read_csv(io.BytesIO(content), sep=separator)
        print(f"DEBUG: CSV loaded with {len(df)} rows using separator '{separator}'. Columns: {df.columns.tolist()}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler CSV: {str(e)}")

    df = df.fillna("")
    
    success_count = 0
    failures = []

    for index, row in df.iterrows():
        try:
            row_dict = row.to_dict()
            print(f"DEBUG: Processing row {index+2}: {row_dict}")
            
            # Find the correct column names (case-insensitive)
            name_col = next((c for c in df.columns if str(c).lower() == "nome"), "Nome")
            email_col = next((c for c in df.columns if str(c).lower() == "email"), "Email")
            phone_col = next((c for c in df.columns if str(c).lower() == "telefone"), "Telefone")

            name = str(row_dict.get(name_col, "")).strip()
            email = str(row_dict.get(email_col, "")).strip()
            phone_raw = str(row_dict.get(phone_col, "")).strip()

            if not name and email:
                name = email.split("@")[0].capitalize()

            print(f"DEBUG: Extracted -> Name: {name}, Email: {email}, Phone: {phone_raw}")
            
            if not email and not phone_raw:
                raise ValueError("Linha sem e-mail ou telefone. Pulando.")
            # Use Mapper Service to split fields between Contact and Deal
            contact_fields, deal_fields = mapper_service.map_fields(row_dict)
            
            # Additional Deal Fields from Form
            deal_fields["lista_origem"] = origin_name
            deal_fields["data_importacao"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Map product name to the 'produto' field if not present in CSV
            if product_name and "produto" not in deal_fields:
                deal_fields["produto"] = product_name

            contact_id = clint_service.upsert_contact(name, email, phone_raw, contact_fields)
            
            if list_tag_name:
                clint_service.add_tag_to_contact(contact_id, list_tag_name)
                
            deal_title = f"{name} - {product_name}"
            clint_service.create_deal(contact_id, stage_id, origin_id, deal_title, product_value, deal_fields)
            
            success_count += 1
        except Exception as e:
            failures.append({
                "linha": index + 2,
                "email": email if 'email' in locals() else "",
                "erro": str(e)
            })

    salvar_historico({
        "id": str(uuid.uuid4()),
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome_da_origem": origin_name,
        "produto": product_name,
        "valor": product_value,
        "tag_da_lista": list_tag_name,
        "total_linhas": len(df),
        "sucesso": success_count,
        "falhas": len(failures),
        "detalhes_falhas": failures
    })

    return {
        "status": "success",
        "message": "Processamento concluído",
        "sucessos": success_count,
        "erros": len(failures),
        "detalhes_falhas": failures
    }

@app.get("/historico")
def ver_historico(request: Request):
    historico = []
    if HISTORICO_PATH.exists():
        try:
            historico = json.loads(HISTORICO_PATH.read_text(encoding="utf-8"))
        except Exception:
            historico = []
    return templates.TemplateResponse("historico.html", {"request": request, "historico": historico})

@app.post("/webhook/clint-won")
async def clint_won_webhook(request: Request):
    return {"status": "success", "message": "Webhook recebido"}
