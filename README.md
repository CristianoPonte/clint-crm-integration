# Clint - Estrutura n8n-first

Projeto reorganizado para operar com foco em n8n, mantendo o legado Python arquivado e a base de reutilizacao separada dos workflows.

## Estrutura principal

- `n8n/workflows/`
  - Apenas workflows versionados.
  - Cada workflow tem sua propria pasta com JSON e README.
- `n8n/reusable/`
  - Ativos reutilizaveis para novos fluxos (deploy, templates e referencias).
- `docs/`
  - Documentos de apoio (acesso, historico e mapeamentos).
- `archives/`
  - Versoes antigas (FastAPI inicial e artefatos legados).
- `data/samples/`
  - Arquivos CSV de exemplo.

## Como escalar novos fluxos

1. Criar pasta em `n8n/workflows/<slug-do-workflow>/`.
2. Adicionar JSON do workflow e README seguindo template em `n8n/reusable/templates/workflow_readme_template.md`.
3. Documentar escopo usando `n8n/reusable/templates/workflow_spec_template.md`.
4. Fazer deploy com `n8n/reusable/deployment/n8n_deploy.py`.
5. Atualizar `PROGRESS.md` com status da fase.

## Arquivos canonicos mantidos na raiz

- `PRD.md`
- `PROGRESS.md`

