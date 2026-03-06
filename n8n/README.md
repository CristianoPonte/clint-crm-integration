# n8n - Operacao do projeto

Estrutura n8n organizada em dois blocos:

- `workflows/`: fluxos versionados por pasta.
- `reusable/`: ativos reaproveitaveis para novos fluxos.

## Estado atual (2026-03-06)

- Workflow A (`WF A - Importacao CSV Clint (Fase 1)`) homologado em producao:
  - endpoint: `POST https://sisifo.metodovde.com.br/webhook/clint-import-csv`
  - teste real com 1 linha: `HTTP 200`, `status=success`, `sucessos=1`, `erros=0`.
- Workflow B (`WF B - Webhook Clint Won (Bootstrap)`) ativo em producao:
  - endpoint: `POST https://sisifo.metodovde.com.br/webhook/clint-won`
  - retorno atual: `status=bootstrap_ready`.

## Workflows atuais

- `n8n/workflows/wf-a-importacao-csv-clint/`
  - Workflow A (fase 1): importacao CSV -> Clint.
- `n8n/workflows/wf-b-webhook-clint-won/`
  - Workflow B (bootstrap): webhook de venda ganha.

## Reuso

- `n8n/reusable/deployment/n8n_deploy.py`
  - Deploy create/update por API n8n + baseline check.
- `n8n/reusable/templates/`
  - Templates para padronizar documentacao e criacao de novos workflows.
- `n8n/reusable/references/`
  - Referencias tecnicas reaproveitadas (mapeamentos e legado util).

## Uso rapido de deploy

Defina variaveis de ambiente com os dados em `docs/access/API_access.md`:

```bash
export N8N_BASE_URL='https://sisifo.metodovde.com.br/api/v1'
export N8N_API_KEY='SEU_TOKEN'
```

Baseline:

```bash
python3 n8n/reusable/deployment/n8n_deploy.py --check-only
```

Deploy dos workflows atuais:

```bash
python3 n8n/reusable/deployment/n8n_deploy.py \
  n8n/workflows/wf-a-importacao-csv-clint/workflow.fase1.json \
  n8n/workflows/wf-b-webhook-clint-won/workflow.bootstrap.json
```

## Aprendizados importantes da instancia atual

- `PATCH /workflows/{id}` pode retornar `405`; usar fallback para `PUT`.
- `active` nao deve ser controlado no body de create/update; ativar via endpoint dedicado (`POST /workflows/{id}/activate`).
- Para registrar webhook de producao, o node Webhook precisa de `webhookId` persistido no JSON.
- No Code node deste ambiente:
  - `fetch` nao esta disponivel;
  - usar `this.helpers.httpRequest` para chamadas HTTP.
- Evitar depender de `process.env` no Code node; passar segredos via payload/credencial.

## Operacao via Postman

Pacote inicial em `postman/`:

- `postman/Clint_n8n_Webhooks.postman_collection.json`
- `postman/Clint_n8n.postman_environment.json`
- `postman/README.md`
