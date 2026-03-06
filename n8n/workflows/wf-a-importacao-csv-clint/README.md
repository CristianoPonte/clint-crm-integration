# WF A - Importacao CSV Clint

## Objetivo

Importar leads para Clint com regras de negocio da fase 1: validacao de entrada, resolve origem/stage BASE, upsert contato, tag e deal.

## Arquivos

- `workflow.fase1.json`: versao ativa da Fase 1.

## Endpoint de producao

- `POST https://sisifo.metodovde.com.br/webhook/clint-import-csv`

## Entrada esperada

- `origin_name`
- `product_name`
- `product_value`
- `list_tag_name`
- `clint_api_token`
- `rows` (array) ou `csv_text` (string CSV)

## Saida

Relatorio consolidado com:

- `status`
- `sucessos`
- `erros`
- `detalhes_falhas`

## Runtime notes (instancia atual)

- O Code node nao expoe `fetch` neste ambiente.
- Chamadas HTTP sao feitas via `this.helpers.httpRequest`.
- Nao depender de `process.env`/`$env` no Code node para segredos.

## Status

- Fase 1 implementada e homologada em producao em `2026-03-06`.
- Teste real validado com 1 linha:
  - `HTTP 200`
  - `status=success`
  - `sucessos=1`
  - `erros=0`
- Proxima evolucao: hardening (auth webhook, retries e idempotencia).
