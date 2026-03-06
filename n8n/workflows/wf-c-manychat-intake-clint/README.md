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
  - prioridade 1: busca por telefone (WhatsApp normalizado)
  - prioridade 2: busca por e-mail
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
  - `id=37`: validação de contrato etapa 6 (`validation_error` com `config_version` + `audit` + payload sanitizado).
  - `id=38`: validação de contrato etapa 6 (`integration_error` com `normalized_payload` mascarado e `duration_ms`).

## Fase 2 - Andamento rápido
- Etapa 1 concluída em 2026-03-06.
- Ajuste principal: parâmetros fixos centralizados em `WORKFLOW_CONFIG` e consumo unificado via `workflow_config`.
- Aprendizado aplicado: ao editar `jsCode` dentro do JSON do workflow, validar escapes de regex antes de publicar.
- Etapa 2 concluída em 2026-03-06.
- Ajuste principal: inclusão de `list_key` com fallback e catálogo em código (`LIST_CONFIGS`) para resolução da configuração da lista.
- Observabilidade: resposta agora inclui `list_key`, `requested_list_key` e `list_key_fallback_applied`.
- Etapa 3 concluída em 2026-03-06.
- Ajuste principal: remoção de fallback de token hardcoded no node de normalização.
- Segurança: token Clint agora vem apenas de fontes explícitas (`x-clint-api-token`/`api-token`, payload explícito ou env do runtime).
- Etapa 4 concluída em 2026-03-06.
- Ajuste principal: helpers extraídos e padronizados para normalização, limpeza, telefone, seleção de aliases e builder de payload Clint.
- Manutenção: aliases de entrada centralizados em `INPUT_ALIASES`, reduzindo edição espalhada para mudanças pontuais.
- Etapa 5 concluída em 2026-03-06.
- Ajuste principal: aliases evoluídos para configuração híbrida (`GLOBAL_INPUT_ALIASES` + `LIST_INPUT_ALIASES`) com merge por `list_key`.
- Manutenção: variações de campo por campanha/lista podem ser absorvidas em configuração, sem reescrever o fluxo principal.
- Etapa 6 concluída em 2026-03-06.
- Ajuste principal: contrato de erro padronizado com `code`, `message`, `step`, `http_status`, `execution_id`, `list_key` e `config_version`.
- Observabilidade: bloco `audit` adicionado em validação, integração e sucesso final (inclui `received_at`, `processed_at` e `duration_ms`).
- Segurança de logs: payloads de erro agora passam por sanitização de campos sensíveis (token, email e telefone/whatsapp mascarados).
- Ajuste rápido pós-etapa 4 (2026-03-06): dedupe alterado para priorizar telefone/WhatsApp e usar e-mail como fallback.
- Credencial criada no n8n: `Clint API Header` (`httpHeaderAuth`), provisionada via API.
- Limitação atual: o core de integração da Clint está em Code node; para usar `credentials` de forma nativa no fluxo, será necessária refatoração para nós nativos (ex.: `HTTP Request`).
- Decisão atual: não usar `Data Tables` neste workflow, a menos que você mude de direção futuramente.
- Deploy: versão atual publicada no n8n em 2026-03-06 (`id=IDbkLRon0vF0r6ZM`).
- Deploy da etapa 5: workflow atualizado via API no dia 2026-03-06 (`id=IDbkLRon0vF0r6ZM`).
- Deploy da etapa 6: workflow atualizado via API no dia 2026-03-06 (`id=IDbkLRon0vF0r6ZM`).
- Aprendizado operacional: para deploy via API, usar `N8N_BASE_URL` com `/api/v1`.
