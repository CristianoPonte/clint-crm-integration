# Product Requirements Document (PRD) - Integrador CSV > Clint API

Não altere esse documentoi a não ser que eu peça expressamente.

## 1. Visão Geral do Produto
Ferramenta interna para automatizar a ingestão de leads provenientes de planilhas CSV para o CRM Clint, garantindo a higienização dos dados, deduplicação de contatos (upsert) e a criação automática de oportunidades (Deals). Também inclui um webhook para rastrear vendas (Deals Ganhos) e notificar via Google Sheets e Slack.

## 2. Stack Tecnológica
*   **Backend:** Python 3.10+ com FastAPI.
*   **Frontend:** HTML5, CSS3, Vanilla JS (Renderizado via Jinja2Templates no FastAPI).
*   **Manipulação de Dados:** pandas (para ler o CSV).
*   **Integrações:** requests (API Clint), gspread (Google Sheets), slack_sdk (Slack).
*   **Ambiente:** Variáveis geridas por python-dotenv.

## 3. Regras de Negócio Core
*   **Telefones:** Devem ser limpos. O CSV envia (11) 99999-9999. A API da Clint exige o envio separado: "ddi": "+55" e "phone": "11999999999".
*   **Deduplicação (Upsert):** Ao enviar um lead para a Clint, se ele já existir (conflito de email OU telefone), o sistema deve atualizar os dados. A busca por duplicatas deve ser feita tanto pelo e-mail quanto pelo telefone (removendo formatação).
*   **Sobrescrita estratégica:** Todos os campos do contato podem (e devem) ser sobrescritos pelas informações mais recentes do CSV, garantindo a atualização do perfil, EXCETO o e-mail e o número de WhatsApp, que servem como chaves de identidade.
*   **Campos Personalizados:** Seguir rigorosamente o mapeamento definido em `regras_custom_fields.md`.
*   **Custom Fields vazios:** Se uma célula do CSV estiver vazia (NaN ou ""), a chave correspondente NÃO deve ser enviada no payload de fields da API.
*   **Obrigatoriedade e Posicionamento:** A criação de um Deal (POST /deals) exige obrigatoriamente o envio do `origin_id` (resolvido automaticamente via busca de Nome no front-end) e do `stage_id`. Todo card deve cair obrigatoriamente no estágio de tipo "BASE" da sua respectiva origem. O `user_id` não deve ser enviado (cards sem dono).

## 4. O Comportamento da API da Clint (Referência para o Código)
- **Base URL:** https://api.clint.digital/v1
- **Auth:** Header obrigatório em todas as requisições: `{"api-token": "SEU_TOKEN"}`
- **Endpoints utilizados:**
    *   GET /origins (Busca com `?limit=250` para garantir visibilidade de todas as listas).
    *   POST /contacts e POST /contacts/{id} (Criação e Atualização/Upsert).
    *   POST /contacts/{id}/tags (Adição de tags via array de strings).
    *   POST /deals (Criação do Card no Kanban).
    *   GET /contacts (Busca de contato por email ou phone para deduplicação).

## 5. PLANO DE AÇÃO E TASKS (Executar sob demanda)

### 🚀 TASK 1: Estrutura Inicial, Frontend e Setup do FastAPI
*Objetivo:* Criar o esqueleto do projeto e a interface visual. Sem lógica complexa de API ainda.

**Ações exigidas:**
*   Crie o requirements.txt com todas as bibliotecas citadas na seção 2.
*   Crie o arquivo .env com as variáveis: CLINT_API_TOKEN, SLACK_BOT_TOKEN, GOOGLE_SHEETS_CREDENTIALS_FILE.
*   Crie a estrutura de pastas: /templates, /static, /services.
*   Crie o templates/index.html e static/style.css. O HTML deve ter um formulário limpo e moderno (enctype="multipart/form-data") contendo:
    *   Input File (CSV).
    *   Input Text para "Nome da Origem".
    *   Input Text para "Produto de Interesse".
    *   Input Number para "Valor do Produto" (Sera mapeado para o campo 'value' nativo do Deal).
    *   Input Text para "Tag da Lista" (Ex: lista-enam-vde).
    *   Botão de Submit.
*   Crie o main.py. Configure o FastAPI, os arquivos estáticos e o Jinja2. Crie a rota GET / renderizando o index.html. Crie a rota POST /upload vazia (apenas recebendo o form e printando no console) e a rota POST /webhook/clint-won vazia. Crie arquivos vazios na pasta /services (clint_service.py, sheets_service.py, slack_service.py).

### 🚀 TASK 2: O Serviço de Integração com a Clint
*Objetivo:* Implementar as funções isoladas que farão as requisições HTTP para a Clint.

**Ações exigidas:**
*   No arquivo services/clint_service.py, configure a URL base e os headers lendo do .env.
*   Implemente get_base_stage_id(origin_id: str) -> str: Faz GET /origins e retorna o ID do estágio cujo campo "type" seja "BASE" para aquela origem.
*   Implemente upsert_contact(name, email, phone_raw, custom_fields: dict) -> str: Limpe o phone_raw deixando apenas números, separe DDI "+55" e o Telefone. Remova chaves com valores nulos/vazios do dict custom_fields. A lógica de busca deve tentar encontrar o lead pelo **Email** e, caso não encontre, tentar pelo **Telefone**. Se o lead existir, atualize os campos (sobrescrevendo); se não, crie um novo. Retorne o contact_id.
*   Implemente add_tag_to_contact(contact_id: str, tag_name: str): Faz POST /contacts/{id}/tags passando a tag.
*   Implemente create_deal(contact_id: str, stage_id: str, origin_id: str, title: str, value: float): Faz POST /deals. Lembre-se que origin_id e stage_id são obrigatórios. Não envie user_id.

### 🚀 TASK 3: O Motor de Processamento do CSV
*Objetivo:* Conectar o formulário do Frontend com o serviço da Clint, processando a planilha linha a linha e garantindo a queda no estágio Base.

**Ações exigidas:**
*   No main.py, atualize a rota POST /upload.
    *   Receba os dados do formulário e o arquivo CSV.
    *   Chame clint_service.get_origin_id_by_name() passando a origem digitada no front. Se não existir, retorne erro 400 avisando o usuário.
    *   Use o pandas para ler o CSV em memória. Substitua NaN por strings vazias.
    *   Itere sobre as linhas (iterrows). Para cada linha:
        *   Isole Nome, Email e Telefone.
        *   Agrupe as demais colunas num dicionário custom_fields.
        *   Envolva o processamento da linha em um bloco try/except.
        *   Chame sequencialmente: upsert_contact(), depois add_tag_to_contact(), depois create_deal() (montando o título dinamicamente, ex: "Nome do Lead - Produto").
    *   Acumule os sucessos e erros (com a mensagem da exceção). Ao final do loop, retorne um JSON com o relatório da operação (quantos foram com sucesso e quais linhas/emails falharam).

### 🚀 TASK 4: Webhook, Google Sheets e Slack
*Objetivo:* Escutar as vendas ganhas na Clint e notificar os canais externos.

**Ações exigidas:**
*   No services/sheets_service.py, implemente a conexão com o Google Sheets usando gspread e as credenciais do .env. Crie uma função append_sale_row(data_list) para adicionar uma nova linha na planilha.
*   No services/slack_service.py, configure o slack_sdk e crie a função send_sales_alert(message).
*   No main.py, atualize a rota POST /webhook/clint-won. Essa rota receberá um JSON da Clint quando um negócio for ganho.
    *   Extraia o contact_id desse payload. Use o clint_service para fazer um GET /contacts/{id} e descobrir as Tags atreladas àquele cliente.
    *   Monte a mensagem formatada (Ex: "Nova venda! Produto: X, Valor: Y, Origem da Tag: Z").
    *   Chame a função do Sheets para salvar a linha e a função do Slack para enviar o alerta. Retorne status 200.

## 5. REGRA GLOBAL DE EXECUÇÃO E SEGURANÇA (Guardrails)

Para garantir a integridade dos dados na conta da Clint e manter o contexto do projeto, você (Agente IA) está ESTRITAMENTE submetido às seguintes regras globais. O não cumprimento dessas regras é considerado uma falha crítica.

### Guardrails de Segurança (API e Sandbox):
1. **PROIBIÇÃO DE DELETE:** Você está TERMINANTEMENTE PROIBIDO de fazer qualquer requisição com o método `DELETE` para a API da Clint. Em nenhuma hipótese apague contatos, deals, tags ou origens.
2. **REGRA DO DADO FALSO (Safe Testing):** Durante testes autônomos no Sandbox (como a TASK 0), se você precisar testar um método `POST` (como criar um contato), você SÓ PODE usar dados fictícios com a tag `[TESTE-AGENTE]`.    - Exemplo obrigatório: `email: teste_agente_01@email.com`, `name: "Bot Teste 01"`, `phone: "11900000000"`. Nunca crie mais do que 1 (um) registro por teste.
    - **TAG DE TESTE:** Em qualquer teste de criação/escrita, você DEVE obrigatoriamente adicionar a tag `teste-integracao`.
    - **DOMÍNIO DE TESTE:** Você SÓ PODE manipular ou atualizar contatos que foram criados por você durante as sessões de teste (identificados pelos emails `teste_agente_XX`). Nunca altere dados de contatos reais do cliente.
3. **CONSENTIMENTO EXPLÍCITO:** Antes de executar qualquer script no seu terminal/sandbox que faça requisições `POST`, `PUT` ou `PATCH` contra a API da Clint, você DEVE parar, me mostrar o código do script e me perguntar: *"Posso executar este teste de escrita na Clint?"*. Só prossiga após o meu "Sim". Requisições `GET` (apenas leitura) estão liberadas para você fazer sem pedir permissão.
4. **CAMPO PRODUTO E VALOR:** Siga rigorosamente o mapeamento de `regras_custom_fields.md`. Os headers das planilhas são figurativos; o que vale é a lógica de mapeamento por Identificador.

### Controle de Estado (O Diário de Bordo):
4. **Antes de iniciar qualquer Task:** Leia o arquivo `PROGRESS.md` para entender o que já foi feito.
5. **Ao finalizar qualquer Task:** Crie ou atualize o arquivo `PROGRESS.md`. Ele deve conter uma checklist das Tasks (`[ ]`, `[~]`, `[X]`) e Notas Técnicas do que foi implementado, além do arquivo `api_mappings.md` como base de consulta de IDs.