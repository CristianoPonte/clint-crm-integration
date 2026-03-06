# Workflows n8n

Cada workflow fica isolado em sua propria pasta para facilitar evolucao por fase, testes e rollback.

## Convencao

- Pasta: `wf-<codigo>-<nome-curto>/`
- JSONs: `workflow.<fase-ou-versao>.json`
- README local: objetivo, entrada, saida, status e plano da proxima fase.

## Workflows existentes

- `wf-a-importacao-csv-clint` (fase1 operacional)
- `wf-b-webhook-clint-won` (bootstrap)
- `wf-c-manychat-intake-clint` (fase1 operacional)
