# Plano Fase 2 - WF C (Manychat -> n8n -> Clint)

Data: 2026-03-06
Status: Em andamento
Premissa desta fase: manter o core da regra em **Code nodes** (portável para fora do n8n), evitando quebrar a lógica em muitos nós nativos de baixo nível.

## Andamento

- 2026-03-06: Etapa 1 concluída em `workflow.fase1.json`.
- Mudança aplicada: centralização dos parâmetros fixos em `WORKFLOW_CONFIG` no node de normalização.
- Mudança aplicada: node de integração passou a consumir `workflow_config` como fonte única para `origin_id`, `origin_name`, `tag_name`, `produto`, `value` e `clint_base_url`.
- Resultado: redução de hardcode espalhado e base pronta para introduzir `list_key` na etapa 2.
- 2026-03-06: Etapa 2 concluída em `workflow.fase1.json`.
- Mudança aplicada: criação do catálogo `LIST_CONFIGS` e `DEFAULT_LIST_KEY` no node de normalização.
- Mudança aplicada: resolução de `workflow_config` por `list_key`, com fallback compatível (`cj_ppt_webinar`).
- Mudança aplicada: retorno de `list_key`, `requested_list_key` e `list_key_fallback_applied` para rastreabilidade operacional.
- 2026-03-06: Etapa 3 concluída em `workflow.fase1.json`.
- Mudança aplicada: remoção do `tokenFallback` hardcoded no node de normalização.
- Mudança aplicada: `clint_api_token` agora é resolvido apenas por fontes explícitas e seguras (`header`, payload explícito ou variáveis de ambiente).
- 2026-03-06: Etapa 4 concluída em `workflow.fase1.json`.
- Mudança aplicada: extração e padronização de helpers no node de normalização (`normalizeKey`, `normalizeValue`, `normalizeListKey`, `cleanObject`, `normalizePhone`, `createAliasPicker`, `buildClintPayloads`).
- Mudança aplicada: aliases de entrada centralizados em `INPUT_ALIASES` para manutenção pontual por helper.
- Mudança aplicada: node de integração reorganizado com helpers reutilizáveis (`buildErrorPayload`, `buildDealPayload`, `findContactIdByEmail`, `findContactIdByPhone`), mantendo o comportamento atual.
- 2026-03-06: Etapa 5 concluída em `workflow.fase1.json`.
- Mudança aplicada: separação de aliases em `GLOBAL_INPUT_ALIASES` e `LIST_INPUT_ALIASES`.
- Mudança aplicada: merge com deduplicação de aliases por `list_key`, sem alterar a lógica principal de normalização.
- 2026-03-06: Etapa 6 concluída em `workflow.fase1.json`.
- Mudança aplicada: contrato de erro padronizado com `config_version` e metadados de auditoria (`audit`) em validação e integração.
- Mudança aplicada: sanitização de dados sensíveis (`token`, email, telefone/whatsapp) em payloads de erro e detalhes técnicos.
- Mudança aplicada: respostas de sucesso da integração enriquecidas com auditoria mínima (`received_at`, `processed_at`, `duration_ms`, estratégia de dedupe e resolução de origem).
- 2026-03-06: deploy da Etapa 6 realizado no n8n (workflow `id=IDbkLRon0vF0r6ZM`).
- 2026-03-06: smoke tests da Etapa 6 no endpoint `manychat-intake-test`:
  - `execution_id=37`: `validation_error` com `config_version` + `audit` e token mascarado no `raw_payload`.
  - `execution_id=38`: `integration_error` (`MISSING_CLINT_TOKEN`) com contrato completo e `normalized_payload` sanitizado.
- 2026-03-06: deploy da Etapa 5 realizado no n8n (workflow `id=IDbkLRon0vF0r6ZM`).
- 2026-03-06: ajuste rápido de dedupe aplicado em `workflow.fase1.json`.
- Mudança aplicada: prioridade de deduplicação alterada para `telefone/whatsapp -> email`.
- 2026-03-06: credencial `Clint API Header` criada no n8n via API (`httpHeaderAuth`), sem refatoração do fluxo.
- Limitação registrada: para consumir `credentials` de forma nativa no WF C atual, é necessário refatorar o core de integração (hoje em Code node) para nós nativos do n8n (ex.: `HTTP Request`).
- Decisão registrada: não usar `Data Tables` neste workflow neste momento; só reavaliar se você mudar de ideia futuramente.
- 2026-03-06: deploy da versão atual da Fase 1 realizado no n8n (workflow `id=IDbkLRon0vF0r6ZM`).

## Aprendizados

- Edição automática de `jsCode` serializado em JSON exige cuidado com escapes de regex (`\\D`, `\\s`, `\\/$`).
- Para manter velocidade e segurança, vale atualizar `jsCode` via conteúdo literal e só depois serializar o workflow.
- Manter a lógica em Code nodes funciona bem para portabilidade, desde que a configuração seja única e explícita no payload interno.
- Para manter compatibilidade na migração para catálogo por lista, o fallback de `list_key` deve preservar exatamente a lista atual de produção.
- Expor `requested_list_key` e flag de fallback ajuda a detectar payloads mal configurados sem interromper a operação.
- O deploy por API exige `N8N_BASE_URL` com sufixo `/api/v1`; sem isso a resposta vem HTML e o script falha no parse JSON.

## Objetivo da fase 2
Evoluir o workflow para ficar mais reaproveitável para novas listas/campanhas, com menos hardcode e melhor governança, sem perder a estratégia atual baseada em código.

## Ordem de implementação (do mais fácil ao mais difícil)

## 1) Centralizar constantes fixas em um único objeto de configuração
Dificuldade: Muito baixa
Status: Concluída (2026-03-06)

- Remover constantes espalhadas e manter um bloco único de configuração por execução.
- Incluir todos os parâmetros hoje fixos:
  - `origin_id`, `origin_name`, `tag_name`, `lista_origem`, `produto`, `value`, `clint_base_url`.
- Garantir que todos os pontos do fluxo consumam apenas esse objeto.

Critério de pronto:
- Não existe mais valor fixo duplicado em mais de um trecho de código.

## 2) Introduzir `list_key` e resolução de configuração por chave
Dificuldade: Baixa
Status: Concluída (2026-03-06)

- Adicionar `list_key` no payload de entrada (com fallback para um default compatível com a fase 1).
- Estruturar um catálogo em código, por exemplo:
  - `LIST_CONFIGS.cj_ppt_webinar = { ... }`
  - `LIST_CONFIGS.outra_lista = { ... }`
- Resolver a configuração ativa com base no `list_key`.

Critério de pronto:
- Trocar lista deixa de exigir alteração de regras de integração; basta trocar `list_key` ou cadastrar nova chave.

## 3) Blindar segurança: remover token fallback hardcoded
Dificuldade: Baixa
Status: Concluída (2026-03-06)

- Eliminar token fixo em código.
- Priorizar token vindo de credencial/configuração segura do ambiente n8n.
- Manter fallback apenas para fontes seguras e explícitas (sem segredo embutido no workflow versionado).

Critério de pronto:
- Nenhum segredo sensível fica versionado no JSON do workflow.

## 4) Extrair helpers reutilizáveis dentro do próprio código
Dificuldade: Média
Status: Concluída (2026-03-06)

- Padronizar helpers de uso comum:
  - normalização de chaves/valores
  - limpeza de objeto
  - normalização de telefone
  - seleção de aliases
  - builder de payload Clint
- Organizar em seções claras no Code node (ou em dois Code nodes: `normalize` e `integrate`, mantendo portabilidade).

Critério de pronto:
- Mudanças de regra pontual (ex.: telefone, alias UTM) exigem edição em um único helper.

## 5) Tornar mapeamento de aliases configurável por lista
Dificuldade: Média
Status: Concluída (2026-03-06)

- Em vez de aliases totalmente fixos, suportar:
  - aliases globais
  - aliases por `list_key`
- Exemplo: `carreira_pretendida` pode variar entre listas sem alterar lógica principal.

Critério de pronto:
- Nova variação de campo é absorvida via configuração, sem reescrever o fluxo inteiro.

## 6) Melhorar contrato de erro e observabilidade técnica
Dificuldade: Média
Status: Concluída (2026-03-06)

- Padronizar resposta de erro com:
  - `code`, `message`, `step`, `http_status`, `execution_id`, `list_key`, `config_version`.
- Incluir metadados mínimos de auditoria no sucesso também.
- Sanitizar campos sensíveis em logs de erro.

Critério de pronto:
- Toda falha relevante aponta passo exato e contexto mínimo para debug.

## 7) Adicionar cache de origem/stage em memória de execução do workflow
Dificuldade: Média para alta

- Evitar `GET /origins` em toda execução quando possível.
- Implementar cache leve (com TTL) para `origin_id -> stage_id BASE`.
- Manter fallback automático para recarregar quando cache expirar ou falhar.

Critério de pronto:
- Redução de chamadas repetitivas sem quebrar robustez quando a origem mudar.

## 8) Parametrizar estratégia de deduplicação por lista
Dificuldade: Alta

- Permitir configuração por `list_key` de ordem de dedupe:
  - email primeiro / telefone primeiro / ambos obrigatórios / etc.
- Manter comportamento atual como default (telefone -> email).

Critério de pronto:
- Estratégia pode mudar por lista sem alterar o algoritmo central.

## 9) Criar modo multi-tenant (opcional) para múltiplas contas Clint
Dificuldade: Alta

- Suportar múltiplas contas/projetos no mesmo core:
  - base URL por tenant
  - token por tenant
  - catálogo de listas por tenant
- Resolver tenant por `tenant_key` + `list_key`.

Critério de pronto:
- O mesmo fluxo atende operações distintas com isolamento de configuração.

## 10) Empacotar o core para portabilidade fora do n8n
Dificuldade: Muito alta

- Organizar lógica do Code node em formato próximo de biblioteca (funções puras + camada de IO).
- Documentar interface de entrada/saída para rodar em outro orquestrador no futuro.
- Manter n8n como adaptador de trigger/response.

Critério de pronto:
- Migração para outro runtime exige trocar apenas camada de integração, não regra de negócio.

## Sequência recomendada de entregas

1. Entrega A (rápida): itens 1, 2 e 3.
2. Entrega B (base de manutenção): itens 4, 5 e 6.
3. Entrega C (escala/performance): item 7.
4. Entrega D (flexibilidade avançada): itens 8 e 9.
5. Entrega E (portabilidade máxima): item 10.

## Riscos e cuidados

- Quanto mais configuração por lista, maior a necessidade de validação automática da configuração.
- Cache de stage pode mascarar mudanças de pipeline se TTL for longo demais.
- Multi-tenant exige governança forte para evitar mistura de credenciais.

## Definição de sucesso da Fase 2

- Nova lista entra com mínimo de alteração de código.
- Nenhum segredo sensível hardcoded.
- Erros ficam mais rastreáveis e auditáveis.
- Core continua orientado a código e reaproveitável fora do n8n.
