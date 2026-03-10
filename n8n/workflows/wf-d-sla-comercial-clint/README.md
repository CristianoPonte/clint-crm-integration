# WF D - SLA Comercial Clint

## Objetivo

Monitorar SLA de permanencia por stage no funil comercial da Clint, rodando em batch diario as 09:00, e enviar alertas no Slack separados por vendedora com os deals atrasados.

## Arquivos

- `plano_SLA.md`: PRD detalhado com escopo, regras, backlog e aceite.
- `workflow_spec.md`: especificacao tecnica do workflow n8n.
- `workflow.fase1.json`: implementacao da fase 1 com T1/T2/T3/T4/T5 concluidas + T7/T8.
- `slack_app_manifest.yaml`: manifest do Slack App usado na integracao.
- `config_sla.example.json`: modelo de configuracao de SLA/stages/roteamento.
- `config_sla.json`: configuracao oficial inicial do workflow (T1 concluida).
- `sql_schema.sql`: schema minimo recomendado para historico e analise.
- `runbook_execucao.md`: sequencia operacional para construir e publicar.
- `decisoes_pendentes.md`: decisoes de produto/operacao necessarias.
- `evidencias_t8_e2e.json`: saida consolidada dos testes E2E de readiness (dry-run + real controlado).

## Escopo da pasta

- Planejamento, implementacao incremental e preparacao de execucao.
- Workflow com T1 a T5 implementadas: coleta paginada, engine de SLA, agrupamento por vendedora e payload/envio Slack.

## Status

- Fase atual: fase 1 pronta para operacao (T1 a T5 + T7/T8 concluidas).
- Canal Slack operacional atual: `comercial-bot` (credencial `Slack account`).
- Roteamento atual: 8 vendedoras cadastradas, todas apontando para `comercial-bot`.
- Autenticacao Clint no workflow: credencial nativa `Clint API Header` (sem dependencia de env no n8n).
- Entregue ate agora:
  - T1: configuracao central de SLA (`config_sla.json`).
  - T2: coleta paginada Clint com `HTTP Request` nativo + validacao `total coletado == totalCount`.
  - T3: engine de calculo de SLA com validacao de cenarios.
  - T4: agrupamento por `user.id` com fallback `sem_responsavel` e validacao de unicidade.
  - T5: payload por grupo e envio via node nativo `Slack - Send Message`.
  - T6 (parcial): persistencia de `sla_overdue_snapshots` via `Data Table` nativo.
  - T7: observabilidade/falha controlada com `Code - Final Summary` (`log_summary` + `slack_stats.messages_sent/messages_failed`).
  - T8: validacao E2E concluida com:
    - `execution_id=66` (dry-run fake controlado);
    - `execution_id=67` (real fake controlado, `messages_sent=2`, `messages_failed=0`, `inserted_rows=4`).
- Runs monitorados em 2026-03-06 (America/Fortaleza):
  - execucao `51` (19:47): teste fake inicial com `success`.
  - execucao `54` (20:04): validacao de formato com `success`.
  - execucao `55` (20:14): teste fake com 2 vendedoras e 2 leads cada (`success`).
  - execucao `56` (20:21): validacao final de formato (`success`).
- Proxima fase: concluir T6 (persistencia historica completa no banco, incluindo `sla_runs`).
  - Estado atual de persistencia:
    - Data Table nome: `sla_overdue`
    - Data Table ID: `VGz5nDwPyfm29faJ`
    - Node: `Data Table - Insert Overdue Snapshots` (modo `insert`)
    - Pendente: persistencia de `sla_runs`.

## Implementacao Slack (resumo final)

- Integracao implementada com node nativo `n8n-nodes-base.slack` (`Slack - Send Message`).
- Credencial utilizada no n8n: `Slack account` (tipo `slackApi`, autenticacao `accessToken` no node).
- App Slack criado por manifest e bot convidado no canal `comercial-bot`.
- Roteamento:
  - fallback `sem_responsavel` -> `comercial-bot`
  - 8 vendedoras cadastradas -> `comercial-bot`
- Formato da mensagem:
  - 1 mensagem por grupo
  - titulo em inline code: `` `SLA Diario | Deals atrasados de <vendedora>` ``
  - total de atrasados em negrito
  - leads em bullet points (`•`)
  - cada lead com: nome do deal, fase atual, proxima fase e atraso
  - linha separadora apenas ao final da mensagem de cada vendedora
- Opcao anti-rodape no node Slack:
  - `otherOptions.appendAttribution = false`
  - `otherOptions.includeLinkToWorkflow = false`
