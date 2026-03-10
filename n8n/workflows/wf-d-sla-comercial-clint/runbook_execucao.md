# Runbook de Execucao - WF D SLA Comercial

## 1) Pre-requisitos

- Acesso ao n8n (`N8N_BASE_URL` + `N8N_API_KEY`)
- Credencial `Clint API Header` ativa no n8n
- Credencial `Slack account` (tipo `slackApi`) ativa no n8n
  - Importante: autorizar com o app bot (`Clint SLA Alerts`) e nao com token pessoal de usuario.
- Data Table `sla_overdue` criada no n8n (ID: `VGz5nDwPyfm29faJ`)
- Configuracao preenchida com regras SLA reais

## 2) Preparacao

1. Revisar e ajustar `config_sla.json` (arquivo oficial ja criado).
2. Preencher `target_minutes` de todas as transicoes ativas.
3. Preencher `routing.sellers` com `user_id -> slack_channel` (canal atual padrao: `comercial-bot`).
4. Definir `dry_run=true` para primeiro teste.
5. Confirmar mapeamento de fechamento por status (`WON` => ganho, `LOST` => perda).

## 3) Persistencia

1. Persistencia ativa atual: `Data Table - Insert Overdue Snapshots`.
2. Confirmar no node:
   - `operation = insert`
   - `dataTableId = VGz5nDwPyfm29faJ`
3. Estrutura da tabela: usar `sla_overdue_snapshots_import.csv` como referencia de colunas.
4. Opcional/futuro: migrar para Postgres completo com `sql_schema.sql` quando entrar `sla_runs`.

## 4) Implementacao no n8n

1. Importar `workflow.fase1.json` no n8n.
2. Conectar credenciais Clint e Slack (`Slack account`).
3. Configurar `Schedule` para 09:00 diario.
4. Garantir que o bot Slack esteja convidado no canal `comercial-bot`.
5. Se a mensagem aparecer como contato pessoal, recriar/reconectar a credencial `Slack account` usando o bot do app.
6. Validar T2 em execucao manual:
   - node `HTTP Request - List Deals` paginando corretamente;
   - `Code - Flatten Deals Pages` com `collected_count == total_count`.
7. Validar T3/T4/T5 em execucao manual:
   - `Code - Compute SLA` com testes internos aprovados;
   - `Code - Group by Seller` com `acceptance_t4.passed = true`.
   - `Code - Build Slack Payload` com `acceptance_t5.passed = true`.
   - `Slack - Send Message` com:
     - `otherOptions.appendAttribution = false`
     - `otherOptions.includeLinkToWorkflow = false`
8. Validar T7:
   - `Code - Final Summary` com `log_summary.total_open`, `log_summary.total_overdue`, `log_summary.messages_sent`, `log_summary.messages_failed`.
   - `status` deve ser `success` ou `partial_success` (nunca quebrar o run por falha isolada de destinataria).

## 5) Testes

1. Rodar manual com `dry_run=true`.
2. Validar:
   - contagem de deals open
   - `collected_count == total_count`
   - lista de atrasados por grupo (incluindo bucket `sem_responsavel`)
   - `acceptance_t3.passed == true`
   - `acceptance_t4.passed == true`
   - inserts em `sla_overdue` (Data Table) para deals atrasados
3. Trocar para `dry_run=false` (ou definir `SLA_DRY_RUN=false` no ambiente).
4. Rodar manual novamente e validar envio Slack.

## 6) Teste de envio fake (controlado)

Objetivo: validar entrega no Slack mesmo sem deals atrasados reais.

1. Habilitar flag temporaria no `Code - Load Config`:
   - `force_fake_overdue_test: true`
2. Executar 1 run e monitorar `Slack - Send Message` em `Executions`.
3. Confirmar:
   - `messages_ready >= 1`
   - `Slack - Send Message` com `ok=true`
   - Formato final da mensagem:
     - titulo em inline code
     - bullets por lead
     - separador apenas ao final da mensagem de cada vendedora
4. Reverter imediatamente:
   - `force_fake_overdue_test: false`
   - cron original `0 9 * * *`

## 6.1) Evidencia E2E consolidada (executada)

- Arquivo: `evidencias_t8_e2e.json`
- Dry-run controlado: `execution_id=66` (`acceptance_t8.passed=true`)
- Run real controlado: `execution_id=67` (`messages_sent=2`, `messages_failed=0`, `inserted_rows=4`)

## 7) Go-live

1. Ativar trigger agendado.
2. Monitorar 3 primeiras execucoes de 09:00.
3. Ajustar thresholds/paginacao se necessario.

## 8) Operacao continua

- Acompanhar `messages_failed > 0`
- Revisar semanalmente SLA por stage
- Revisar rotas de vendedoras quando houver mudancas de equipe
- Troubleshooting critico:
  - erro `CLINT_API_TOKEN nao definido` no run: usar credencial nativa `Clint API Header` no node HTTP (nao depender de env no n8n remoto).
  - se o texto `Automated with this n8n workflow` ainda aparecer mesmo com os dois flags em `false`, tratar como limitacao da instancia/plano e considerar envio via `HTTP Request` direto na Slack API.
