# n8n - Operacao do projeto

Estrutura n8n organizada em dois blocos:

- `workflows/`: fluxos versionados por pasta.
- `reusable/`: ativos reaproveitaveis para novos fluxos.

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
export N8N_BASE_URL='http://SEU-N8N/api/v1'
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

