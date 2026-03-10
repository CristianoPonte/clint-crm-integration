# Plano SLA - Fluxo Comercial Clint

Data: 2026-03-06  
Status: fase 1 implementada e validada (T1 a T5 concluidas) + T6 parcial + T7/T8 concluidas

## 1) Objetivo de negocio

Criar monitoramento diario de SLA por stage no funil comercial, com envio no Slack de uma mensagem separada por vendedora contendo apenas deals atrasados.

## 2) Contexto e base tecnica

- Origem alvo (mesma do WF C): `Perpetuo Webinario`
- `origin_id`: `bd1bd846-0c87-4acb-b221-d7f8d2089e68`
- Workflow de referencia: `wf-c-manychat-intake-clint`
- Campos de deal disponiveis e uteis para SLA: `stage_id`, `stage`, `status`, `updated_stage_at`, `created_at`, `updated_at`, `latest_meeting_datetime`, `latest_meeting_link`, `user`, `contact`, `fields`
- Filtro de API validado para performance: `origin_id`, `stage_id`, `status`, `user_id`, `page`, `limit`

## 3) Stages atuais da origem alvo

- `d34e0d52-c401-41dd-907c-80b1d27373ee` - `Lead Cadastrado` (BASE)
- `05a13438-b800-406b-b0c1-fd17a7f52fa6` - `Contato Realizado`
- `582df60d-9cb4-40e5-8a66-365d7b0e8c8a` - `Diagnostico`
- `f58d9353-9454-487a-b7db-b125814ebf97` - `Negociacao`
- `c2d8136e-5451-4294-bf43-d16eca3c52cc` - `Follow-up`
- `b12f6608-ff0a-459f-bcb5-93f1ddb37bbf` - `Fechado` (CLOSING)

## 4) Mapa de SLA (modelo)

Modelo de configuracao por transicao:

- `Lead Cadastrado -> Contato Realizado = 24h`
- `Contato Realizado -> Diagnostico = Xh`
- `Diagnostico -> Negociacao = Xh`
- `Negociacao -> Follow-up = Xh`
- `Follow-up -> Fechado = Xh`

Observacao: apenas a primeira regra esta definida hoje. As demais precisam de decisao.

## 5) Regra de calculo de atraso

1. Considerar apenas deals com `status=OPEN`.
2. Para cada regra `A -> B`, avaliar deals atualmente no stage `A`.
3. `reference_ts = updated_stage_at` (fallback `created_at` se necessario).
4. `age_minutes = now - reference_ts`.
5. `overdue_minutes = age_minutes - target_minutes`.
6. Deal atrasado quando `overdue_minutes > 0`.
7. Stage de fechamento nao entra em atraso operacional.

## 6) Requisitos funcionais

- RF01: executar diariamente as 09:00 no timezone de operacao.
- RF02: buscar deals da origem alvo com paginacao.
- RF03: calcular atraso por regra de transicao do mapa SLA.
- RF04: agrupar atrasados por `user.id` (vendedora).
- RF05: enviar 1 mensagem Slack por vendedora com seus atrasados.
- RF06: tratar deals sem dona em bucket `sem_responsavel`.
- RF07: persistir snapshot diario para analise historica.
- RF08: logar resumo da execucao (`total_open`, `total_overdue`, `messages_sent`, `messages_failed`).

## 7) Requisitos nao funcionais

- RNF01: idempotencia por execucao (nao duplicar notificacao no mesmo run).
- RNF02: resiliencia por destinataria (falha em 1 envio nao quebra o restante).
- RNF03: tempo de execucao previsivel com paginacao controlada.
- RNF04: mascaramento de PII em logs tecnicos.
- RNF05: parametros de SLA editaveis sem reescrever algoritmo.

## 8) Arquitetura proposta (n8n)

Workflow: `WF D - SLA Comercial Diario`

1. `Schedule Trigger` (09:00 diario).
2. `Code - Load Config` (origem, regras SLA, rotas Slack).
3. `HTTP Request - List Deals` (status OPEN + origin_id, paginado).
4. `Code - Compute SLA` (calculo por stage/regra).
5. `Code - Group by Seller` (inclui bucket sem responsavel).
6. `Code - Build Slack Payload`.
7. `Slack - Send Message` (1 por grupo).
8. `DB Insert - sla_runs`.
9. `DB Insert - sla_overdue_snapshots`.
10. `Code - Final Summary`.

## 9) Banco de dados (recomendacao)

Recomendacao: **sim, usar banco simples desde o inicio** para viabilizar analise historica.

Justificativa:

- sem banco, voce tem apenas fotografia do dia;
- com banco, voce mede tendencia por stage, vendedora e origem;
- facilita auditoria e melhoria continua de SLA.

Estrutura minima: ver arquivo `sql_schema.sql`.

## 10) Plano de implementacao executavel (tarefas do agente)

### T1 - Criar configuracao central de SLA

Entregavel: `config_sla.json` baseado no `config_sla.example.json`  
Criterio de aceite: schema valido e todas as regras mapeadas por IDs de stage.
Status: concluido.

### T2 - Implementar coleta paginada da Clint

Entregavel: nodes HTTP + loop paginado  
Criterio de aceite: `total coletado == totalCount` da API para a consulta.
Status: concluido em `workflow.fase1.json` com validacao de contagem.

### T3 - Implementar engine de calculo

Entregavel: code node de SLA  
Criterio de aceite: cenarios de teste marcam corretamente atraso e nao atraso.
Status: concluido em `workflow.fase1.json` com validacao de cenarios embutida no node `Code - Compute SLA`.

### T4 - Implementar agrupamento por vendedora

Entregavel: agrupamento por `user.id` com fallback  
Criterio de aceite: cada deal atrasado aparece em apenas 1 grupo.
Status: concluido em `workflow.fase1.json` com node `Code - Group by Seller` e validacao de unicidade.

### T5 - Implementar mensagens Slack

Entregavel: payload de mensagem por grupo  
Criterio de aceite: mensagem contem nome do deal, fase atual, proxima fase e atraso.
Status: concluido em `workflow.fase1.json` com node `Code - Build Slack Payload` e validacao `acceptance_t5`.
Formato final validado: titulo em inline code, bullets por lead e separador apenas ao final da mensagem por vendedora.

### T6 - Persistir historico no banco

Entregavel: escrita em `sla_runs` e `sla_overdue_snapshots`  
Criterio de aceite: 1 execucao gera 1 run + N snapshots atrasados.
Status: parcial. `sla_overdue_snapshots` ativo via Data Table `sla_overdue` (ID `VGz5nDwPyfm29faJ`); `sla_runs` pendente.

### T7 - Observabilidade e falha controlada

Entregavel: log final e status da execucao  
Criterio de aceite: falha parcial de envio nao interrompe run completo.
Status: concluido em `workflow.fase1.json` com node `Code - Final Summary`, retry em Clint/Slack e envio Slack com `continueOnFail`.

### T8 - Validacao E2E e readiness

Entregavel: teste com dry-run e run real controlado  
Criterio de aceite: mensagens corretas por vendedora e persistencia confirmada.
Status: concluido com evidencias em `evidencias_t8_e2e.json`:
- `execution_id=66` (dry-run): `acceptance_t8.passed=true`.
- `execution_id=67` (real controlado): `messages_sent=2`, `messages_failed=0`, `snapshot_stats.inserted_rows=4`.

## 11) Definition of Done

- [x] Config de SLA oficial preenchida e validada
- [x] Workflow criado e versionado na pasta `wf-d-sla-comercial-clint`
- [x] Envio Slack por vendedora funcionando (node nativo Slack configurado e run monitorado)
- [x] Bucket `sem_responsavel` definido e ativo
- [ ] Persistencia historica ativa (parcial: snapshots ativos em Data Table; `sla_runs` pendente)
- [x] Logs e resumo de execucao padronizados
- [x] Smoke test concluido (incluindo validacao de formato final no Slack)

## 12) Decisoes pendentes

Ver arquivo `decisoes_pendentes.md`.

## 13) Acoes manuais do time

- Definir SLA alvo para todas as transicoes (alem de 24h no primeiro salto).
- Manter atualizado o mapeamento `user_id -> destino Slack` (estado atual: 8 usuarias mapeadas para `comercial-bot`).
- Canal fallback para deals sem dona definido em `comercial-bot`.
- Confirmar timezone oficial do batch.
- Provisionar credenciais de DB e Slack no n8n.
