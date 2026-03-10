# Decisoes Pendentes - WF D SLA Comercial

## Decisoes ja tomadas

1. Capturar campos de reuniao no contrato de dados (`latest_meeting_datetime`, `latest_meeting_link`).
2. Classificar fechamento por `status`:
   - `WON` => `ganho`
   - `LOST` => `perda`
3. Timezone operacional inicial: `America/Fortaleza`.
4. Destino do bucket `sem_responsavel`: `comercial-bot`.
5. Mapeamento inicial de roteamento: 8 usuarias cadastradas, todas em `comercial-bot`.

## Decisoes obrigatorias antes do go-live completo

1. Definir SLA alvo para cada transicao de stage.
2. Confirmar se o SLA sera em horas corridas ou horas uteis.
3. Confirmar se o workflow deve considerar somente uma origem ou multiplas.
4. Confirmar se o workflow vai somente notificar ou tambem escrever `sla_status` no deal.
5. Confirmar limite maximo de paginas por execucao.

## Recomendacoes objetivas

- Timezone: `America/Fortaleza`
- SLA inicial: horas corridas (MVP)
- Escrita na Clint: nao escrever no MVP (somente leitura + historico proprio)
- Banco: Postgres simples desde o inicio
