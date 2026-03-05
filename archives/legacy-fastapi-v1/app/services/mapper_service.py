
# Mapping between CSV labels and Clint API identifiers
# This includes both Contact and Deal fields

# Full list of identifiers from API Query:
# CONTACT: idade, notes, historico, profissao, turma_da_oab, foi_aluno_oab, 
#          horas_por_dia, renda_familiar, estuda_para_oab, tempo_de_estudo, 
#          e_aluno_concursos, maior_dificuldade, features_desejadas, 
#          carreira_pretendida, disciplina_segunda_f, produto_de_interesse, 
#          quantas_horas_por_di, quantas_vezes_voce_j, sentimento_de_aprova
# DEAL: produto, utm_term, utm_medium, utm_source, utm_content, lista_origem, 
#       utm_campaign, data_importacao

CONTACT_FIELDS_MAP = {
    "idade": "idade",
    "profissao": "profissao",
    "profissão": "profissao",
    "qual sua profissão": "profissao",
    "você é bacharel estudante ou advogado": "profissao",
    "historico": "historico",
    "histórico": "historico",
    "foi aluno oab": "foi_aluno_oab",
    "é ou já foi aluno vde oab": "foi_aluno_oab",
    "e aluno concursos": "e_aluno_concursos",
    "é aluno vde concursos carreiras jurídicas": "e_aluno_concursos",
    "carreira pretendida": "carreira_pretendida",
    "qual carreira jurídica pretende seguir": "carreira_pretendida",
    "horas por dia": "horas_por_dia",
    "quantas horas livres por dia você tem em média para estudar": "horas_por_dia",
    "renda familiar": "renda_familiar",
    "qual a sua renda familiar": "renda_familiar",
    "features desejadas": "features_desejadas",
    "o que você mais preza em um curso preparatório para o enam": "features_desejadas",
    "maior dificuldade": "maior_dificuldade",
    "qual a sua maior dificuldade na sua preparação para o enam": "maior_dificuldade",
    "tempo de estudo": "tempo_de_estudo",
    "há quanto tempo estuda pra concursos": "tempo_de_estudo",
    "turma da oab": "turma_da_oab",
    "turma da oab de interesse": "turma_da_oab",
    "estuda para oab": "estuda_para_oab",
    "disciplina segunda fase": "disciplina_segunda_f",
    "produto de interesse": "produto_de_interesse",
    "quantas horas por dia você estuda em média": "quantas_horas_por_di",
    "quantas vezes você já fez a prova da oab": "quantas_vezes_voce_j",
    "sentimento de aprovação atual": "sentimento_de_aprova",
    "notas": "notes",
    "notas do contato": "notes"
}

DEAL_FIELDS_MAP = {
    "utm source": "utm_source",
    "utm medium": "utm_medium",
    "utm campaign": "utm_campaign",
    "utm term": "utm_term",
    "utm content": "utm_content",
    "produto": "produto",
    "item combo": "produto",
    "item": "produto",
    "lista origem": "lista_origem",
    "data importação": "data_importacao",
    "data de importação": "data_importacao"
}

def normalize_key(key: str) -> str:
    # Remove common punctuation and ignore case
    k = str(key).strip().lower()
    # Remove special punctuation that might vary
    for char in "?!:;,.()[]\"'":
        k = k.replace(char, "")
    # Standardize separators to spaces
    k = k.replace("-", " ").replace("_", " ").replace("/", " ")
    # Re-normalize spaces to single
    k = " ".join(k.split())
    return k

def map_fields(row_dict: dict):
    contact_fields = {}
    deal_fields = {}
    
    for k, v in row_dict.items():
        if not v or str(v).strip() == "":
            continue
            
        nk = normalize_key(k)
        raw_key_norm = str(k).strip().lower()
        
        # Skip native fields handled separately
        if raw_key_norm in ["nome", "email", "telefone", "phone", "name"]:
            continue
            
        # Try to map to Contact
        # Check both normalized (with spaces) and raw-norm (underscores)
        mapped = False
        
        # Priority 1: Exact mapping from Label/Common Name
        if nk in CONTACT_FIELDS_MAP:
            contact_fields[CONTACT_FIELDS_MAP[nk]] = v
            mapped = True
        elif raw_key_norm in CONTACT_FIELDS_MAP:
            contact_fields[CONTACT_FIELDS_MAP[raw_key_norm]] = v
            mapped = True
        elif nk in DEAL_FIELDS_MAP:
            deal_fields[DEAL_FIELDS_MAP[nk]] = v
            mapped = True
        elif raw_key_norm in DEAL_FIELDS_MAP:
            deal_fields[DEAL_FIELDS_MAP[raw_key_norm]] = v
            mapped = True
            
        # Priority 2: Fallback to identifier match if no spaces
        if not mapped:
            # If the header IS already the identifier (lowercase, no spaces)
            if raw_key_norm in CONTACT_FIELDS_MAP.values():
                contact_fields[raw_key_norm] = v
            elif raw_key_norm in DEAL_FIELDS_MAP.values():
                deal_fields[raw_key_norm] = v
                
    return contact_fields, deal_fields
