# Workflow Spec - WF D SLA Comercial Diario

## 1) Identificacao

- Nome do workflow: `WF D - SLA Comercial Diario`
- Slug de pasta: `wf-d-sla-comercial-clint`
- Versao/fase: `fase1` + T6 parcial + T7/T8 concluidas
- Responsavel: Automacao/RevOps
- Ultima atualizacao: `2026-03-06` (21:24 America/Fortaleza)

## 2) Objetivo de negocio

- Problema: falta de visibilidade diaria de deals atrasados por etapa e por vendedora.
- Resultado esperado: notificacoes objetivas no Slack + historico para analise.

## 3) Contrato de entrada

- Trigger principal: `Schedule` diario as `09:00`.
- Trigger opcional: `Manual Trigger` para dry-run.
- Campos obrigatorios de configuracao:
  - `origin_id`
  - `stage_sla_rules[]`
  - `seller_routes[]`
- Campos opcionais:
  - `timezone`
  - `dry_run`
  - `max_pages`

## 4) Regras de negocio

- Processar somente deals `OPEN`.
- Computar atraso por stage atual usando `updated_stage_at`.
- Agrupar por dona (`user.id`); sem dona vai para fallback.
- Enviar uma mensagem por grupo no Slack.
- Formatar mensagem com titulo em inline code, bullets por lead e separador apenas ao final do bloco da vendedora.
- Persistir snapshot de atraso por run.

## 5) Desenho tecnico (nodes)

Implementado na fase atual:

1. `Manual Trigger`
2. `Schedule Trigger`
3. `Code - Load Config`
4. `HTTP Request - List Deals` (paginado, nativo do n8n, credencial `Clint API Header`)
5. `Aggregate - Combine Pages`
6. `Code - Flatten Deals Pages`
7. `Code - Compute SLA`
8. `Code - Group by Seller`
9. `Code - Build Slack Payload`
10. `Code - Expand Slack Messages`
11. `Slack - Send Message`
12. `Code - Expand Overdue Snapshots`
13. `Data Table - Insert Overdue Snapshots` (ID `VGz5nDwPyfm29faJ`)
14. `Code - Trigger Final Summary (No Slack Dispatch)`
15. `Code - Final Summary`

Backlog da fase 1 (proximas tarefas):

1. `Persist Run`

## 6) Integracoes e credenciais

- APIs:
  - Clint API (`https://api.clint.digital/v1`)
  - Slack API
- Credenciais n8n:
  - `Clint API Header` (httpHeaderAuth no node `HTTP Request - List Deals`)
  - `Slack account` (tipo `slackApi` no node `Slack - Send Message` com `authentication=accessToken`)
  - credencial DB (Postgres recomendado)
- Variaveis de ambiente:
  - `SLA_TIMEZONE` (default: `America/Fortaleza`)
  - `SLA_DRY_RUN` (opcional)

## 7) Contrato de saida

- Sucesso:
  - `status=success`
  - `run_id`
  - `sla_stats` (`computed_count`, `overdue_count`, `invalid_reference_count`)
  - `grouped_stats` (`total_groups`, `total_overdue`, `sem_responsavel_count`)
  - `slack_stats` (`messages_ready`, `messages_sent`, `messages_failed`, `channels_ready`, `dry_run`)
  - `snapshot_stats` (`planned_rows`, `inserted_rows`)
- Erro parcial:
  - `status=partial_success`
  - detalhes de destinatarios com falha
- Erro total:
  - `status=error`
  - `step`
  - `message`

## 8) Observabilidade e resiliencia

- Logs minimos:
  - inicio/fim do run
  - total de deals lidos
  - total atrasados
  - tempo total
- Retry:
  - Clint API: retry para 429/5xx
  - Slack: retry curto com backoff
- Timeout:
  - HTTP Clint: 20s
  - Slack: 15s
- Idempotencia:
  - chave por `run_date + origin_id + seller_id`

## 9) Testes

- Caso feliz:
  - deals atrasados e mensagens enviadas.
- Caso de validacao:
  - config incompleta deve falhar antes de chamar integracoes.
- Caso de validacao T3:
  - cenarios sinteticos validam atraso, nao atraso e fallback de timestamp.
- Caso de validacao T4:
  - cada deal atrasado deve aparecer em apenas um grupo.
- Caso de falha parcial:
  - 1 envio Slack falha e o restante conclui.
- Caso de envio real validado:
  - execucao `51` com dado fake controlado e `Slack - Send Message` com `ok=true`.
  - execucao `55` com 2 vendedoras e 2 leads fake por vendedora (`ok=true`).
  - execucao `56` com validacao final de formato (`titulo inline code + bullets + separador no fim`).
  - execucao `66` (dry-run fake controlado): `acceptance_t8.passed=true`.
  - execucao `67` (real fake controlado): `messages_sent=2`, `messages_failed=0`, `inserted_rows=4`.

## 10) Deploy

- Arquivo JSON alvo: `workflow.fase1.json` (criado).
- Deploy por API n8n via script existente em `n8n/reusable/deployment/n8n_deploy.py`.
- Checklist pos-deploy:
  - trigger ativo
  - dry-run aprovado
  - run de 09:00 monitorado no primeiro dia
