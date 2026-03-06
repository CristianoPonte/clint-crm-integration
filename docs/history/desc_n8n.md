# Documentacao Unificada - Migracao para n8n

## 1) Contexto e objetivo

Este documento consolida o estado real da migracao CSV -> Clint para n8n apos homologacao em producao.

Objetivo principal:
- reduzir dependencia operacional do backend FastAPI legado;
- centralizar automacao e rastreabilidade no n8n;
- preservar regras de negocio de importacao (upsert, tag, deal em stage BASE, relatorio final).

---

## 2) Estado atual validado (2026-03-06)

- Dominio oficial:
  - `https://sisifo.metodovde.com.br`
- API n8n:
  - `https://sisifo.metodovde.com.br/api/v1`
- Workflows principais:
  - `WF A - Importacao CSV Clint (Fase 1)` (`id=PZVcheWyos7ewnp0`) ativo e homologado.
  - `WF B - Webhook Clint Won (Bootstrap)` (`id=LU1JwbgCgIpJLCnM`) ativo e respondendo.

Resultados de validacao:
- WF A (`POST /webhook/clint-import-csv`):
  - teste real com 1 linha retornou `HTTP 200`;
  - payload de retorno com `status=success`, `sucessos=1`, `erros=0`.
- WF B (`POST /webhook/clint-won`):
  - retorno `HTTP 200` com `status=bootstrap_ready`.

---

## 3) Incidentes encontrados e correcoes aplicadas

1. Webhook de producao retornando `not registered` mesmo com workflow ativo
- causa: node Webhook sem `webhookId` persistido no JSON versionado.
- correcao: adicao de `webhookId` nos workflows A e B + ciclo deactivate/activate.

2. Erro `process is not defined` no Code node do WF A
- causa: tentativa de acesso a env var via `process.env` no runtime do Code node.
- correcao: remover dependencia de `process.env` e exigir `clint_api_token` no payload.

3. Erro `fetch is not defined` no Code node do WF A
- causa: runtime da instancia nao expoe `fetch` no sandbox do Code node.
- correcao: substituir chamadas HTTP por `this.helpers.httpRequest`.

4. `PATCH /workflows/{id}` com `405`
- causa: comportamento da instancia/API.
- correcao: manter fallback de update para `PUT` no script de deploy.

5. Ativacao de workflow
- observacao: nao depender de `active` no body de create/update.
- pratica adotada: usar `POST /workflows/{id}/activate`.

---

## 4) Workflows e responsabilidades

## 4.1 Workflow A - Importacao CSV Clint (Fase 1)

Entrada:
- `origin_name`, `product_name`, `product_value`, `list_tag_name`, `clint_api_token`;
- `rows` (array) ou `csv_text`.

Processamento:
- validacao de obrigatorios;
- parse CSV opcional;
- resolve origem por nome (case-insensitive) e stage `BASE`;
- upsert de contato por e-mail com fallback telefone;
- aplica tag;
- cria deal;
- retorna relatorio de sucesso/falha por linha.

Saida:
- `status`, `sucessos`, `erros`, `detalhes_falhas`, ids de origem/stage.

## 4.2 Workflow B - Webhook Clint Won (Bootstrap)

Entrada:
- `contact_id`, `deal_id` (obrigatorios)
- `product_name`, `product_value` (opcionais)

Saida:
- `status=bootstrap_ready` + eco dos campos recebidos.

Observacao:
- fase atual ainda bootstrap; integracoes Sheets/Slack seguem pendentes.

---

## 5) Operacao e teste rapido

Variaveis para script de deploy:
- `N8N_BASE_URL=https://sisifo.metodovde.com.br/api/v1`
- `N8N_API_KEY=<token>`

Comandos:
- baseline:
  - `python3 n8n/reusable/deployment/n8n_deploy.py --check-only`
- deploy:
  - `python3 n8n/reusable/deployment/n8n_deploy.py n8n/workflows/wf-a-importacao-csv-clint/workflow.fase1.json n8n/workflows/wf-b-webhook-clint-won/workflow.bootstrap.json`

Postman:
- pacote inicial pronto em `postman/`:
  - `Clint_n8n_Webhooks.postman_collection.json`
  - `Clint_n8n.postman_environment.json`
  - `README.md`

---

## 6) Pendencias atuais

- TASK 4 (Google Sheets + Slack no fluxo de venda ganha) ainda nao concluida.
- Hardening recomendado:
  - autenticar webhooks (`Authentication: none` nao recomendado em producao);
  - politicas de retry e idempotencia;
  - observabilidade (alerta para execucoes em erro).
