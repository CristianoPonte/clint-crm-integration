# WF C - Manychat Intake Clint

## Objetivo
Receber leads do Manychat via webhook, normalizar payload real, fazer upsert de contato na Clint, aplicar tag e criar deal.

## Arquivos
- `workflow.bootstrap.json`: versão bootstrap (legado da fase inicial).
- `workflow.fase1.json`: versão atual com integração ponta a ponta.
- `plano_implementacao.md`: plano e histórico técnico.

## Endpoints
- Teste: `POST https://sisifo.metodovde.com.br/webhook/manychat-intake-test`
- Produção: `POST https://sisifo.metodovde.com.br/webhook/manychat-intake`

## Regras de entrada (fase 1)
- Aceita payloads Manychat com campos em raiz e/ou `custom_fields`.
- Identidade mínima obrigatória: `email` ou telefone normalizado.
- Telefone: hoje prioriza `whatsapp_phone`, com fallback para `whatsapp`, `phone`, `telefone`, `celular`, `auth_phone`.
- Carreira: aceita `carreira_pretendida` e `carreira_concursos`/`Carreira_Concursos`.
- UTM: aceita aliases comuns (`utm_source`, `UTM_SOURCE`, etc).

## Integração Clint (fase 1)
- Resolve origem por `origin_id` fixo e stage `BASE` dinamicamente.
- Deduplicação de contato:
  - prioridade 1: busca por e-mail
  - prioridade 2: busca por telefone
- Atualização/criação:
  - update: `POST /contacts/{id}`
  - create: `POST /contacts`
- Tag no contato: `POST /contacts/{id}/tags` com `["cj-ppt-webinar"]`
- Deal: `POST /deals` com `value=2557` e fields:
  - `lista_origem=cj-ppt-webinar`
  - `data_importacao=<timestamp>`
  - `produto=VDE Carreiras Jurídicas Ciclo Prioritário`
  - UTMs quando preenchidas

## Configuração fixa
- `origin_name`: `Perpétuo Webinário`
- `origin_id`: `bd1bd846-0c87-4acb-b221-d7f8d2089e68`
- `tag_name`: `cj-ppt-webinar`
- `lista_origem`: `cj-ppt-webinar`
- `produto`: `VDE Carreiras Jurídicas Ciclo Prioritário`
- `value`: `2557`

## Observabilidade e status de execução
- O webhook responde com JSON e `http_status` coerente (200/400/5xx).
- Para erro de negócio (`validation_error`/`integration_error`), o workflow responde ao webhook e depois força falha interna no n8n via node `Fail Execution On Error Status`.
- Resultado prático: cliente recebe resposta correta e o log do n8n marca a execução como `error`.

## Status atual (2026-03-06)
- Workflow ativo: `WF C - Manychat Intake Clint (Fase 1)` (`id=IDbkLRon0vF0r6ZM`).
- Bootstrap WF C desativado: `id=bnjM2OPkMHkrcoZU`.
- Execuções de validação:
  - `id=17`: sucesso (contato criado + deal criado).
  - `id=18`: sucesso (contato atualizado + novo deal).
  - `id=22`: erro intencional de validação (aparece como `error` no n8n).
  - `id=23`: sucesso após retentativa.
