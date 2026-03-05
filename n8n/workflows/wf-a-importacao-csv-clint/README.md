# WF A - Importacao CSV Clint

## Objetivo

Importar leads para Clint com regras de negocio da fase 1: validacao de entrada, resolve origem/stage BASE, upsert contato, tag e deal.

## Arquivos

- `workflow.fase1.json`: versao ativa da Fase 1.

## Entrada esperada

- `origin_name`
- `product_name`
- `product_value`
- `list_tag_name`
- `clint_api_token` (ou credencial no ambiente n8n)
- `rows` (array) ou `csv_text` (string CSV)

## Saida

Relatorio consolidado com:

- `sucessos`
- `erros`
- `detalhes_falhas`

## Status

- Fase 1 implementada e publicada.
- Proxima evolucao: hardening (auth webhook, retries e idempotencia).

