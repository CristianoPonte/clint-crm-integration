# PROGRESS.md

## Progresso das Tasks do PRD

- [X] **TASK 0: Exploração, Mapeamento e Persistência de Contexto**
- [X] **TASK 1: Estrutura Inicial, Frontend e Setup do FastAPI**
- [X] **TASK 2: O Serviço de Integração com a Clint**
- [X] **TASK 3: O Motor de Processamento do CSV**
- [ ] **TASK 4: Webhook, Google Sheets e Slack**

---

## Notas Técnicas

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
