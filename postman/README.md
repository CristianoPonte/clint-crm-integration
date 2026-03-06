# Postman - Inicio Rapido

Arquivos para importar:

- `Clint_n8n_Webhooks.postman_collection.json`
- `Clint_n8n.postman_environment.json`

## Como usar

1. No Postman, importe os dois arquivos.
2. Selecione o environment **Clint n8n - Sisifo**.
3. Preencha as variaveis secretas:
   - `n8n_api_key`
   - `clint_api_token`
4. Execute na ordem:
   - `0 - Health / Home - GET`
   - `1 - WF A (Importacao CSV) / WF A - Import 1 Row (Success)`
   - `2 - WF B (Webhook Clint Won) / WF B - Success`
   - `3 - Admin n8n API / List Workflows`
   - `4 - Clint API / Clint - List Origins (All)`
   - `5 - WF C (Manychat Intake) / WF C - Bootstrap Test`

## Consulta de Origins (Clint)

Para listar todas as origins da conta:

1. Preencha `clint_api_token` no environment.
2. Rode `4 - Clint API / Clint - List Origins (All)`.

Para encontrar um origin ID por nome:

1. Defina `origin_search_name` (exemplo: `Perpétuo Webinário`).
2. Rode `4 - Clint API / Clint - Find Origin ID by Name`.
3. O resultado sera salvo automaticamente em `origin_id_found`.

## Observacoes

- Os requests de sucesso usam scripts de pre-request para gerar dados unicos (`unique_email`, `unique_name`, `deal_suffix`).
- A colecao inclui requests de erro intencional para validar regras de payload:
  - `WF A - Validation Error (Missing Required)`
  - `WF B - Validation Error (Missing deal_id)`
- IDs atuais dos workflows no environment:
  - `wf_a_id = PZVcheWyos7ewnp0`
  - `wf_b_id = LU1JwbgCgIpJLCnM`
