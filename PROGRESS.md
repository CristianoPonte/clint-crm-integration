# PROGRESS.md

## Progresso das Tasks do PRD

- [X] **TASK 0: Exploração, Mapeamento e Persistência de Contexto**
- [X] **TASK 1: Estrutura Inicial, Frontend e Setup do FastAPI**
- [X] **TASK 2: O Serviço de Integração com a Clint**
- [X] **TASK 3: O Motor de Processamento do CSV**
- [ ] **TASK 4: Webhook, Google Sheets e Slack**

---

## Notas Técnicas

### WF C - Manychat Intake Clint (Concluida - 2026-03-06)
- Workflow Fase 1 publicado e ativo:
  - `WF C - Manychat Intake Clint (Fase 1)` (`id=IDbkLRon0vF0r6ZM`)
  - endpoints ativos: `POST /webhook/manychat-intake-test` e `POST /webhook/manychat-intake`
- Ajuste operacional aplicado no ambiente local:
  - `.env` atualizado para `N8N_BASE_URL=https://sisifo.metodovde.com.br/api/v1` (evita falha de deploy por retorno HTML fora da rota da API).
- Workflow bootstrap do WF C desativado:
  - `WF C - Manychat Intake Clint (Bootstrap)` (`id=bnjM2OPkMHkrcoZU`)
- Integracao ponta a ponta validada:
  - upsert por telefone/whatsapp com fallback por email;
  - aplicacao da tag `cj-ppt-webinar`;
  - criacao de deal com `origin_id` fixo e `stage BASE` dinamico.
- Parsing adaptado ao payload real do Manychat:
  - telefone em `whatsapp_phone`;
  - carreira em `custom_fields.Carreira_Concursos`;
  - aliases adicionais para UTMs.
- Observabilidade ajustada:
  - o webhook responde com `http_status` correto;
  - erros de negocio agora marcam a execucao como `error` no n8n (node `Fail Execution On Error Status`).
- Fase 2 - Etapa 4 concluida:
  - helpers reutilizaveis extraidos e padronizados no core (normalizacao, limpeza, telefone, aliases e builder de payload Clint);
  - aliases centralizados em `INPUT_ALIASES`, reduzindo manutencao distribuida.
- Fase 2 - Etapa 5 concluida:
  - mapeamento de aliases evoluido para `GLOBAL_INPUT_ALIASES` + `LIST_INPUT_ALIASES`;
  - merge de aliases por `list_key` com deduplicacao, mantendo fallback de lista.
- Fase 2 - Etapa 6 concluida:
  - contrato de erro padronizado com `config_version` e bloco `audit` nas respostas de validacao/integracao;
  - resposta de sucesso enriquecida com metadados de auditoria tecnica (`received_at`, `processed_at`, `duration_ms`);
  - sanitizacao de dados sensiveis em erros (`token`, `email`, `telefone/whatsapp`) para reduzir exposicao em logs.
- Testes executados em 2026-03-06:
  - validacoes locais do code node (4 casos de normalizacao/aliases + compilacao de sintaxe dos 3 code nodes);
  - smoke endpoint `manychat-intake-test` (validacao 400 + sucesso create/update por email/telefone);
  - cenario de UTM parcial validado sem quebra e cenario de chamadas duplicadas seguidas validado (primeira `created`, segunda `updated`).
  - validacao local da etapa 6: compilacao sintatica dos code nodes + checks de contrato (erro com `config_version`/`audit` e mascaramento de token/email/telefone).
- Deploy executado em 2026-03-06:
  - workflow `WF C - Manychat Intake Clint (Fase 1)` atualizado via API (`id=IDbkLRon0vF0r6ZM`).
  - etapa 6 publicada no mesmo workflow (`id=IDbkLRon0vF0r6ZM`).
- Smoke tests da etapa 6 (endpoint `manychat-intake-test`):
  - `execution_id=37`: `validation_error` com `config_version`, `audit` e token mascarado;
  - `execution_id=38`: `integration_error` (`MISSING_CLINT_TOKEN`) com `normalized_payload` sanitizado e `duration_ms`.

### Homologacao em producao (Concluida - 2026-03-06)
- Dominio oficial consolidado para operacao externa:
  - `https://sisifo.metodovde.com.br`
- Endpoint de producao validado para Workflow A:
  - `POST /webhook/clint-import-csv`
  - teste real com 1 linha retornou `HTTP 200` com `status=success`, `sucessos=1`, `erros=0`.
- Endpoint de producao validado para Workflow B:
  - `POST /webhook/clint-won`
  - retorno `HTTP 200` com `status=bootstrap_ready`.
- Correcoes aplicadas para registrar webhooks em producao:
  - adicao de `webhookId` nos nodes de trigger de WF A e WF B.
- Correcoes aplicadas para runtime do Code node:
  - removido uso de `fetch` no WF A (na instancia atual `fetch` nao existe no sandbox);
  - substituido por `this.helpers.httpRequest` no node `Process Import Clint`;
  - removido fallback para env vars no Code node (acesso bloqueado no runtime desta instancia).
- Pacote inicial de Postman criado para operacao:
  - `postman/Clint_n8n_Webhooks.postman_collection.json`
  - `postman/Clint_n8n.postman_environment.json`
  - `postman/README.md`

### Reorganizacao estrutural (Concluida - 2026-03-05)
- Projeto reorganizado para modelo **n8n-first** com separacao clara entre:
  - workflows: `n8n/workflows/<workflow>/`
  - ativos reutilizaveis: `n8n/reusable/`
  - legado arquivado: `archives/legacy-fastapi-v1/`
- Workflows migrados para pastas dedicadas:
  - `n8n/workflows/wf-a-importacao-csv-clint/workflow.fase1.json`
  - `n8n/workflows/wf-b-webhook-clint-won/workflow.bootstrap.json`
- Script de deploy movido para:
  - `n8n/reusable/deployment/n8n_deploy.py`
- Documentacao de apoio movida para:
  - `docs/access/`
  - `docs/reference/`
  - `docs/history/`
- Base FastAPI inicial preservada em arquivo para consulta/reuso:
  - `archives/legacy-fastapi-v1/app/`
- Observacao: referencias antigas de caminho nas notas historicas abaixo (ex: `main.py`, `services/`) agora correspondem ao legado em `archives/legacy-fastapi-v1/app/`.

### Bootstrap da migração para n8n (Em andamento - 2026-03-05)
- Criado o diretório `n8n/` com workflows versionados para início da migração:
  - `n8n/workflows/wf-a-importacao-csv-clint/workflow.fase1.json`
  - `n8n/workflows/wf-b-webhook-clint-won/workflow.bootstrap.json`
- Portada para JavaScript (Code node no n8n) a lógica base de mapeamento de campos do `mapper_service.py` no Workflow A (fase inicial).
- Criado `n8n/reusable/deployment/n8n_deploy.py` para:
  - validar baseline da API (`users`, `workflows`, `credentials`, `tags`);
  - fazer create/update de workflows por nome via API n8n.
- Registrado guia de uso em `n8n/README.md`.

### Fase 1 do n8n (Concluída - 2026-03-05)
- Workflow A evoluído para execução fim-a-fim de importação Clint:
  - validação de entrada;
  - parse de `rows` ou `csv_text` com separador `,`/`;`;
  - resolução de `origin_id` por nome e `stage_id` tipo `BASE`;
  - upsert de contato por e-mail com fallback para telefone;
  - aplicação de tag no contato;
  - criação de deal com campos customizados (`lista_origem`, `data_importacao`, `produto` etc);
  - relatório final de sucessos/falhas por linha.
- Mantido deploy versionado via `n8n/reusable/deployment/n8n_deploy.py`.

### Atualizações de Definição de Campos (Concluída)
- Criado o arquivo `regras_custom_fields.md` com as definições de campos para Contact e Deal.
- Realizada a varredura da API para confirmar a criação dos campos na conta do cliente.
- Mapeado o campo `lista_origem` no Deal para capturar a origem via front-end.
- Mapeado o campo `value` (nativo) no Deal para capturar o valor da venda via front-end.
- Refatorado `services/clint_service.py` para suportar deduplicação por E-mail OU Telefone, garantindo a sobrescrita controlada dos dados do perfil.
- **Nova Regra de Negócio:** Todo Lead/Deal submetido agora cai obrigatoriamente no estágio "Base" da sua respectiva origem, simplificando a interface e o processamento.

### Atualizações da TASK 3 (Concluída - V1 OK)
- O motor de processamento do CSV foi implementado no endpoint POST `/upload` em `main.py`.
- **Evolução da Lógica de Seleção:** Implementada a busca por "Nome da Origem" com normalização (strip + case insensitive) para resolver IDs em tempo de execução.
- **Automação de Kanban:** O `stage_id` não é mais fixo nem digitado; o sistema identifica o estágio do tipo `"BASE"` dentro da origem selecionada via API.
- **Mapeamento de Campos Inteligente:** Lançada a versão 1.0 do `mapper_service.py`, que traduz labels literais/figurativos das planilhas para Identificadores da API e separa dados entre Contato e Negócio.
- **Persistência de Jornada:** UTMs e campos de importação agora são salvos no Deal, preservando o histórico do contato.
- **Relatório Detalhado:** A resposta JSON consolidada fornece feedback visual de sucessos vs falhas por linha.
- **Status Geral:** Sistema 100% funcional para ingestão, deduplicação (E-mail/Telefone) e criação de oportunidades.

### Correções de Bugs e Melhorias de Estabilidade
- **JSON Object Issue:** Corrigido erro onde o código tratava a resposta da API como lista, quando na verdade é um objeto com a chave `"data"`.
- **Visibilidade de Listas:** Aumentado o limit de fetch de origens para `250` para garantir que listas novas/recentes não sejam perdidas pela paginação.
- **Campo de Nome:** Corrigido o mapeamento de busca de `title` para o campo correto `name`.
- **Ambiente:** Identificada a necessidade de rodar `python3 -m uvicorn` para garantir a execução correta dos módulos instalados via pip.

### Atualizações da TASK 2 (Concluída)
- Implementado `services/clint_service.py` com funções isoladas.
- Configurada a base URL e headers lendo `CLINT_API_TOKEN` e usando `requests`.
- `get_base_stage_id`: Nova função que fecta as origens e retorna dinamicamente o ID do estágio do tipo "BASE" para a origem selecionada.
- `upsert_contact`: Adicionada lógica de extração do telefone ignorando caracteres não-numéricos e separando DDI (+55). Mapeamento dos campos null/empty fields filtrados das requisições.
- **Nova Lógica de Upsert:** Agora realiza busca prévia por E-mail e, secundariamente, por Telefone antes de decidir por criar ou atualizar o contato.
- `add_tag_to_contact`: Endpoint configurado enviando tag em formato array.
- `create_deal`: Implementado com requisições exigindo `origin_id`, garantindo que não se envie card dono.

### Atualizações da TASK 1 (Concluída / Revisada)
- O arquivo `.env` foi criado contendo as três variáveis de ambiente necessárias.
- Backend FastAPI configurado com arquivo `main.py` possuindo o setup de templates, rotas básicas (GET `/`, POST `/upload`, POST `/webhook/clint-won`) e os `print`s mockados.
- Criada a interface frontend (arquivos `templates/index.html` e `static/style.css`).
- **Revisão efetuada pós Task 0:** A prova de conceito inicial utilizava UUIDs fictícios como `id_base_enam` no select field do Front-End. O formulário HTML foi atualizado em `templates/index.html` e agora injeta nos options do Input Dropdown "Destino (Kanban/Stage)" os **IDs reais corretos** já mapeados pela API, como o ID `336fbee2...` (OAB ANUAL).

### Atualizações da TASK 0 (Concluída)
- Realizado mapeamento completo da API da Clint (via scripts Python exploratórios).
- Criado o arquivo `api_mappings.md` para persistir dados valiosos para as Tasks 2 e 3 (incluindo mapeamento dos IDs de Custom Fields para entidades Deal e Contact, IDs das Origens criadas e IDs de seus Stages atrelados).
- Foi descoberto que a Clint lida com as Origens e Pipelines juntos: um `GET /origins` retorna as origens e embute os arrays de seus stages.
- O endpoint correto da documentação para account fields é `/account/fields` e não `/account-fields` como estava na wiki oficial.
- Payload de inserção de contatos foi testado e aceito com sucesso (Status 201).
- Para lidar com *Upsert* (leads já existentes): detectado que o erro retornado pelo conflito de email é um `400 Bad Request` com a string `"Contact email already exists"`. Além disso, a atualização do lead ocorre com sucesso via `POST /contacts/{id}` com formato body tradicional JSON.
- O envio de tags ( `POST /contacts/{id}/tags` ) requer obrigatoriamente um **array de strings** (ex: `["minha-tag"]`) no body da requisição (se não fizer isso, retorna erro 400).
- Todos os IDs e nomes necessários já estão devidamente registrados em `api_mappings.md`.
