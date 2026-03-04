# 📋 Resumo do Projeto — Integrador CSV › Clint CRM

> Documento de referência: o que foi construído, como funciona e para onde podemos ir.

---

## O que é esse projeto?

Uma **ferramenta interna de automação** que elimina o trabalho manual de inserir leads no CRM. O operador simplesmente faz o upload de uma planilha CSV, informa qual lista/funil de destino quer usar, e o sistema cuida de tudo: higieniza os dados, deduplica contatos já existentes, cria ou atualiza o perfil de cada lead no Clint, adiciona a tag certa e abre um card de oportunidade no kanban corretamente posicionado.

**Stack:** Python 3 + FastAPI no backend, HTML/CSS/JS vanilla no frontend.

---

## O que fizemos até agora

### 🔍 TASK 0 — Exploração e Mapeamento da API

Antes de escrever uma linha de código de produção, fizemos uma investigação completa da API do Clint usando scripts Python exploratórios. Esse trabalho foi essencial para entender como a API realmente funciona (em vez de confiar só na documentação).

**Principais descobertas:**

- A autenticação é feita via header `api-token` em todas as requisições.
- O endpoint correto para campos de conta é `/account/fields` (a documentação oficial tinha um erro, indicando `/account-fields`).
- Origens e funis (kanban) são retornados juntos em `GET /origins` — cada origem já embute o array dos seus `stages`.
- O conflito de email ao criar um contato retorna um `400 Bad Request` com a mensagem `"Contact email already exists"` — esse foi o sinal usado para implementar o upsert.
- A atualização de um contato existente é feita via `POST /contacts/{id}` (não `PUT` ou `PATCH`).
- Tags precisam ser enviadas como **array de strings** (`["minha-tag"]`) — enviar uma string simples causa erro 400.
- Todos os IDs reais (origens, stages, campos personalizados) foram catalogados e persistidos no arquivo `api_mappings.md`.

---

### 🏗️ TASK 1 — Estrutura do Projeto e Frontend

Com o mapeamento em mãos, o projeto foi estruturado do zero.

**O que foi criado:**

- `requirements.txt` com todas as dependências (`fastapi`, `uvicorn`, `pandas`, `requests`, `python-dotenv`, `gspread`, `slack_sdk`, `jinja2`).
- Arquivo `.env` com as variáveis de ambiente: `CLINT_API_TOKEN`, `SLACK_BOT_TOKEN`, `GOOGLE_SHEETS_CREDENTIALS_FILE`.
- Pastas organizadas: `/templates`, `/static`, `/services`.
- `main.py` configurando o FastAPI com templates Jinja2 e rotas básicas.
- Interface web (`templates/index.html` + `static/style.css`) com um formulário limpo contendo:
  - **Input de arquivo** para o CSV.
  - **Campo de texto** para o "Nome da Origem" (busca dinâmica por nome — única, sem necessidade de ID manual).
  - **Campo de texto** para "Produto de Interesse".
  - **Campo numérico** para "Valor do Produto" (mapeado para o campo nativo `value` do Deal).
  - **Campo de texto** para "Tag da Lista" (ex: `lista-enam-vde`).
  - Botão de submit.

---

### 🔌 TASK 2 — Serviço de Integração com a Clint (`clint_service.py`)

Foram implementadas as funções isoladas que se comunicam com a API. Cada função tem uma responsabilidade única.

| Função | O que faz |
| :--- | :--- |
| `get_origin_id_by_name(name)` | Busca a origem pelo nome (normalização por `strip` + case insensitive). Retorna o `origin_id`. |
| `get_base_stage_id(origin_id)` | Faz `GET /origins` e retorna dinamicamente o ID do stage cujo tipo é `"BASE"` para aquela origem. |
| `upsert_contact(name, email, phone, custom_fields)` | Limpa o telefone (remove formatação, separa DDI `+55`). Tenta encontrar o lead por **email** e, caso não encontre, por **telefone**. Se existir → atualiza. Se não → cria. Retorna o `contact_id`. Campos vazios/nulos são removidos do payload. |
| `add_tag_to_contact(contact_id, tag_name)` | Adiciona uma tag ao contato via `POST /contacts/{id}/tags`. |
| `create_deal(contact_id, stage_id, origin_id, title, value)` | Cria o card de oportunidade no kanban. `origin_id` e `stage_id` são obrigatórios. `user_id` não é enviado (card sem dono). |

---

### ⚙️ TASK 3 — Motor de Processamento do CSV

O coração do sistema: a rota `POST /upload` que processa a planilha linha a linha.

**Fluxo completo de uma importação:**

```
Upload do CSV
    ↓
Valida o "Nome da Origem" digitado no front → resolve origin_id
    ↓
Busca automaticamente o stage_id do tipo "BASE" dessa origem
    ↓
Lê o CSV com pandas (NaN substituído por "")
    ↓
Para cada linha:
    1. Extrai Nome, Email, Telefone
    2. Agrupa campos restantes em custom_fields (Contact e Deal)
    3. upsert_contact() → cria ou atualiza o contato
    4. add_tag_to_contact() → aplica a tag da lista
    5. create_deal() → abre card no kanban no estágio "Base"
    ↓
Retorna JSON com relatório: sucessos + falhas detalhadas por linha
```

**Serviço de mapeamento (`mapper_service.py`):** Traduz os headers literais/figurativos da planilha para os identificadores corretos da API do Clint, separando os dados entre campos de `Contact` e de `Deal`.

---

### 🗂️ Mapeamento de Campos Personalizados

Todos os campos personalizados foram **criados na conta do Clint** e documentados em `regras_custom_fields.md` e `api_mappings.md`.

**Campos do Contato (perfil permanente do lead):**

| Identificador | Pergunta/Label |
| :--- | :--- |
| `idade` | Idade |
| `profissao` | Você é bacharel, estudante ou advogado? |
| `tempo_de_estudo` | Há quanto tempo estuda para Concursos? |
| `foi_aluno_oab` | É ou já foi aluno VDE OAB? |
| `e_aluno_concursos` | É aluno VDE Concursos? |
| `carreira_pretendida` | Qual carreira jurídica pretende seguir? |
| `horas_por_dia` | Quantas horas livres por dia para estudar? |
| `renda_familiar` | Qual a sua renda familiar? |
| `features_desejadas` | O que mais preza em um curso preparatório? |
| `maior_dificuldade` | Maior dificuldade na preparação? |

**Campos do Deal (dados da oportunidade/importação):**

| Identificador | Descrição |
| :--- | :--- |
| `produto` | Produto desejado naquela negociação |
| `value` | Valor do produto (campo nativo do Deal) |
| `utm_source` / `utm_medium` / `utm_campaign` / `utm_term` / `utm_content` | Rastreamento de tráfego |
| `lista_origem` | Nome da lista/origem de onde o lead veio |
| `data_importacao` | Data e hora da importação pelo sistema |

---

### 🐛 Correções de Bugs Relevantes

- **Resposta da API:** A API retorna um objeto `{ "data": [...] }` e não um array direto. O código foi corrigido para acessar a chave correta.
- **Paginação de Origens:** O `GET /origins` foi configurado com `?limit=250` para garantir visibilidade de todas as listas cadastradas.
- **Campo de Nome:** A busca de contatos por nome foi corrigida de `title` para o campo correto `name`.
- **Ambiente Python:** Identificada a necessidade de usar `python3 -m uvicorn` para garantir que os módulos instalados via pip sejam carregados corretamente.

---

## O que está incluído na versão atual (v1.0)

✅ Interface web para upload de CSV  
✅ Resolução automática de origem pelo nome (sem necessidade de digitar IDs)  
✅ Automação do kanban: card sempre cai no estágio "Base" da origem correta  
✅ Higienização de telefone (remove formatação, separa DDI)  
✅ Deduplicação por email e depois por telefone (upsert inteligente)  
✅ Sobrescrita controlada: dados do perfil são atualizados, exceto email e WhatsApp  
✅ Campos vazios não são enviados à API (sem poluição de dados)  
✅ Adição automática de tag à lista  
✅ Criação do Deal com produto, valor, UTMs e data de importação  
✅ Relatório JSON detalhado ao final (sucessos vs. falhas por linha)  
✅ Documentação técnica completa (`api_mappings.md`, `regras_custom_fields.md`)

❌ Webhook de vendas ganhas (TASK 4 — não implementado)  
❌ Integração com Google Sheets (TASK 4 — não implementado)  
❌ Notificação via Slack (TASK 4 — não implementado)

---

## 🚀 Possibilidades Futuras

### 1. Completar a TASK 4 — Webhook + Sheets + Slack

O próximo passo natural é implementar o lado reverso do fluxo: **rastrear quando uma venda é ganha** no Clint. Quando um Deal é movido para o estágio de fechamento, a Clint enviaria um evento (webhook) para a rota `POST /webhook/clint-won`. O sistema então:

- Buscaria os dados do contato e as tags associadas.
- Registraria a venda em uma **planilha do Google Sheets** (nome, produto, valor, origem, data).
- Enviaria um **alerta no Slack** para o canal de vendas em tempo real.

Isso fecha o ciclo: entrada do lead → saída como venda.

---

### 2. Dashboard de Acompanhamento em Tempo Real

Atualmente o resultado é apenas um JSON retornado após o processamento. Um dashboard visual poderia mostrar:

- Número de leads importados por lista/campanha ao longo do tempo.
- Taxa de contatos novos vs. atualizados (upsert).
- Quantos Deals foram criados por origem.
- Erros de importação agrupados por tipo (email inválido, telefone duplicado, etc.).

---

### 3. Agendamento e Importação Automática

Hoje, a importação é 100% manual (o operador faz o upload). Futuramente, o sistema poderia:

- **Conectar diretamente ao Google Sheets** como fonte de dados (em vez de CSV), lendo em schedules automáticos.
- **Monitorar uma pasta de Google Drive** e processar arquivos novos automaticamente.
- Usar um **scheduler** (como APScheduler ou Celery) para rodar importações em horários configurados.

---

### 4. Validação e Feedback mais Rico no Frontend

Melhorias que tornariam a ferramenta mais segura para o usuário:

- **Preview do CSV** antes de submeter: mostrar as primeiras linhas para confirmar que as colunas estão corretas.
- **Validação de headers:** avisar se uma coluna esperada não estiver presente no CSV.
- **Barra de progresso** em vez de uma tela estática de "aguardando" durante o processamento de planilhas grandes.
- **Modo de simulação ("dry run"):** processar o CSV e mostrar o que *seria* enviado sem de fato criar nada no Clint.

---

### 5. Histórico de Importações

Um log persistido (em banco de dados ou arquivo) com o registro de cada importação realizada: data/hora, nome da lista, quantidade de linhas processadas, taxa de sucesso e os erros encontrados. Isso ajudaria a auditar problemas e evitar duplicar importações acidentalmente.

---

### 6. Suporte a Múltiplos Formatos de Planilha

Hoje o sistema aceita apenas CSV. Poderia ser expandido para:

- **XLSX** (Excel) — muito comum em exportações de ferramentas de marketing.
- **Google Sheets diretamente** via URL ou ID da planilha.
- **Mapeamento dinâmico de colunas** pela interface: o usuário indica qual coluna da planilha corresponde a qual campo do Clint, sem depender de headers padronizados.

---

### 7. Controle de Acesso e Multi-usuário

Atualmente não há autenticação. Para uso em equipe:

- Adicionar login simples (ex: autenticação via Google OAuth).
- Diferentes níveis de permissão (quem pode importar, quem pode ver relatórios, quem pode configurar mapeamentos).
- Log de quem fez cada importação.

---

### 8. Deduplicação Mais Avançada

A deduplicação atual usa email ou telefone. Casos não cobertos:

- **Mesmo telefone, email diferente:** hoje seria tratado como contato diferente se o email não bater.
- **Variações de nome + telefone similar:** leads que erraram um dígito do telefone.
- **Detecção de leads "órfãos":** identificar contatos sem Deal associado e alertar o operador.

---

*Documento gerado em 26/02/2026.*
