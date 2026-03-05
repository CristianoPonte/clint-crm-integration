# Documentacao Unificada - Migracao para n8n

## 1) Contexto e objetivo

Este documento consolida tudo o que foi definido e executado sobre a migracao do integrador CSV -> Clint para n8n.

Objetivo principal:
- Tirar a dependencia do backend FastAPI para a operacao de importacao.
- Centralizar automacao, rastreabilidade e manutencao dentro do n8n.
- Manter as regras de negocio existentes (upsert, tag, deal, stage BASE, relatorio).

---

## 2) Decisoes tecnicas tomadas

- Stack da automacao: **n8n + JavaScript (Code node)**.
- Motivo: menor acoplamento operacional e manutencao mais rapida no proprio workflow.
- Python continua util como referencia de regra de negocio (legacy), mas o runtime principal agora e n8n.

---

## 3) O que foi implementado de fato

## 3.1 Estrutura criada no repositorio

- `n8n/workflows/workflow_a_importacao_bootstrap.json`
- `n8n/workflows/workflow_b_clint_won_bootstrap.json`
- `scripts/n8n_deploy.py`
- `n8n/README.md`
- Atualizacao de `PROGRESS.md`

## 3.2 Deploy por API n8n

Foi criado um script de deploy versionado com capacidades de:
- baseline check da API (`users`, `workflows`, `credentials`, `tags`);
- create/update de workflows por nome;
- fallback de compatibilidade de update (`PATCH` -> `PUT`) por comportamento da instancia.

Observacao importante aprendida:
- Em algumas chamadas de workflow, `PATCH` retornou `405`.
- A solucao foi implementar fallback para `PUT`.

## 3.3 Workflows publicados

Estado observado na instancia:
- `PZVcheWyos7ewnp0` | active=`true` | `WF A - Importacao CSV Clint (Fase 1)`
- `LU1JwbgCgIpJLCnM` | active=`false` | `WF B - Webhook Clint Won (Bootstrap)`
- `YUU63AqCfvXmQ7pe` | active=`false` | `WF A - Importacao CSV Clint (Bootstrap)` (versao antiga)

---

## 4) Fase 1 - Workflow A (status: concluida em codigo/deploy)

Nome publicado:
- `WF A - Importacao CSV Clint (Fase 1)`

Fluxo implementado:
1. Webhook recebe payload JSON.
2. Valida campos obrigatorios:
   - `origin_name`
   - `product_name`
   - `product_value`
   - `list_tag_name`
3. Aceita entrada em dois formatos:
   - `rows` (array de objetos), ou
   - `csv_text` (CSV string, delimitador `,` ou `;`).
4. Resolve origem Clint por nome (case-insensitive).
5. Resolve stage da origem (prioridade `type == BASE`).
6. Para cada linha:
   - normaliza headers e valores;
   - aplica mapeamento para `contact_fields` e `deal_fields`;
   - executa upsert de contato por e-mail com fallback por telefone;
   - aplica tag no contato;
   - cria deal com campos adicionais (`lista_origem`, `data_importacao`, `produto`, etc.).
7. Retorna relatorio consolidado:
   - `sucessos`
   - `erros`
   - `detalhes_falhas`

Regras de negocio preservadas do legado:
- deduplicacao por e-mail/telefone;
- envio de tags em array;
- criacao em stage BASE;
- ignorar campos vazios nos payloads.

---

## 5) Workflow B (status atual)

Nome:
- `WF B - Webhook Clint Won (Bootstrap)`

Estado:
- bootstrap pronto (valida payload basico e responde padrao);
- ainda pendente de Fase 2 (Google Sheets + Slack).

---

## 6) Aprendizados e incidentes tecnicos

1. Campo `active` no body de create/update de workflow:
- a API retornou erro de campo somente leitura em certas chamadas.
- abordagem segura: nao depender de `active` no body de create/update.
- ativacao feita por endpoint de ativacao.

2. Update de workflow:
- `PATCH` nao foi aceito na instancia para alguns casos.
- fallback para `PUT` resolveu.

3. Webhook URL de producao aparecendo como localhost:
- no editor foi exibido: `http://localhost:5678/webhook/clint-import-csv`.
- isso indica configuracao de URL publica do n8n nao ajustada para ambiente externo.
- consequencia: teste externo pode falhar/ficar inconsistente.

4. Authentication do webhook em `none`:
- endpoint fica publico sem protecao.
- risco operacional para um fluxo que cria/atualiza contato e deal.

---

## 7) Status de validacao

Validado:
- acesso API n8n;
- deploy/update de workflows;
- ativacao do workflow A por API.

Pendente:
- validacao HTTP externa ponta a ponta no endpoint de webhook de producao, dependente de configuracao de URL publica correta da instancia.

---

## 8) Configuracoes iniciais recomendadas

## 8.1 Variaveis para operar via API (local/script)

Definidas conforme `API_access.md`:
- `N8N_BASE_URL`
- `N8N_API_KEY`

Uso:
- `python3 scripts/n8n_deploy.py --check-only`
- `python3 scripts/n8n_deploy.py n8n/workflows/workflow_a_importacao_bootstrap.json n8n/workflows/workflow_b_clint_won_bootstrap.json`

## 8.2 Configuracoes de infraestrutura da instancia n8n (importante)

Para corrigir URL de producao do webhook (evitar localhost), ajustar no servidor/container do n8n:
- `WEBHOOK_URL` (preferencial)
- e, se necessario: `N8N_HOST`, `N8N_PROTOCOL`, `N8N_PORT`, `N8N_PATH`

Depois reiniciar o n8n.

## 8.3 Seguranca do webhook

Recomendado imediatamente:
- deixar de usar `Authentication: none` para esse endpoint;
- exigir token/header de autenticacao no webhook;
- usar HTTPS;
- opcionalmente restringir origem por IP/proxy/firewall.

---

## 9) Payload esperado no Workflow A

Exemplo minimo (JSON):

```json
{
  "origin_name": "NOME DA ORIGEM",
  "product_name": "NOME DO PRODUTO",
  "product_value": 197.0,
  "list_tag_name": "tag-da-importacao",
  "clint_api_token": "TOKEN_CLINT",
  "rows": [
    {
      "Nome": "Fulano",
      "Email": "fulano@email.com",
      "Telefone": "11999999999",
      "utm source": "meta",
      "utm campaign": "campanha-x"
    }
  ]
}
```

Alternativa de entrada:
- `csv_text` no lugar de `rows`.

---

## 10) Proximos passos recomendados (curto prazo)

1. Ajustar URL publica de webhook na infraestrutura n8n.
2. Proteger webhook (auth/token).
3. Rodar teste externo ponta a ponta com payload de amostra.
4. Avancar para Fase 2:
   - completar Workflow B com gravacao em Google Sheets;
   - notificacao Slack;
   - validacao com payload real/simulado.

---

## 11) Resumo executivo

- A base da migracao foi implantada com sucesso.
- Fase 1 do Workflow A esta pronta em codigo e publicada.
- Principal bloqueio atual nao e regra de negocio, e sim configuracao de exposicao/autenticacao do webhook em producao.
