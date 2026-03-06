# Plano Fase 3 - Modularizacao Reutilizavel por Lista

Data: 2026-03-06
Status: Concluida
Escopo: transformar o WF C em estrutura modular para qualquer `list_key`, com separacao clara entre configuracao global, configuracao especifica e variacoes de entrada.

## Andamento rapido

- 2026-03-06: Etapa 3.1 concluida em `workflow.fase1.json`.
- 2026-03-06: Etapa 3.2 concluida em `workflow.fase1.json` (com node Code para catalogo).
- 2026-03-06: Etapa 3.3 concluida em `workflow.fase1.json` (resolucao por precedencia, merge de aliases, validacao de schema minimo e retorno `CONFIG_ERROR`).
- 2026-03-06: Etapa 3.4 concluida em `workflow.fase1.json` (normalizacao consumindo apenas `runtime_context + resolved_aliases`, sem `LIST_CONFIGS`/`GLOBAL_INPUT_ALIASES` hardcoded).
- 2026-03-06: Etapa 3.5 concluida em `workflow.fase1.json` (novo node `Build Clint Payloads` entre normalizacao e integracao).
- 2026-03-06: Etapa 3.6 concluida em `workflow.fase1.json` (node `Integrate Clint` consumindo `resolved_config`, `retry` configuravel e `dedupe_strategy` via config resolvida).
- 2026-03-06: Etapa 3.7 concluida com regressao completa, onboarding da `test_lista_nova` apenas no `Config Catalog` e deploy no n8n (`id=IDbkLRon0vF0r6ZM`), validado nos endpoints de teste e producao.

## 1) Objetivo da fase 3

Criar uma camada de configuracao dedicada, reutilizavel e previsivel, para que novas listas sejam adicionadas sem reescrever a logica principal de normalizacao e integracao.

Resultado esperado:
- o core de negocio continua em Code nodes;
- configuracao deixa de ficar espalhada dentro de um unico node;
- entrada de nova lista vira alteracao de catalogo, nao de algoritmo.

## 2) Problema atual (base fase 1/2)

Hoje a configuracao esta funcional, mas acoplada ao node `Normalize + Validate Input`:
- `DEFAULT_LIST_KEY`
- `LIST_CONFIGS`
- `GLOBAL_INPUT_ALIASES`
- `LIST_INPUT_ALIASES`

Isso dificulta reuso entre fluxos e aumenta risco de regressao quando entramos com novas listas.

## 3) Desenho alvo (fase 3)

### 3.1 Fluxo alvo de nodes

1. `Webhook Manychat Intake Test`
2. `Webhook Manychat Intake Prod`
3. `Prepare Runtime Context` (Code)
- Extrai `payload`, `headers`, `execution_id`, `received_at`.
4. `Config Catalog` (Code)
- Fonte unica de configuracao (global + listas + aliases + defaults).
5. `Resolve Config` (Code)
- Resolve `list_key` e monta `resolved_config`.
6. `Normalize + Validate Input` (Code)
- Apenas normaliza e valida payload usando `resolved_aliases`.
7. `Build Clint Payloads` (Code)
- Apenas monta payload de contato/deal.
8. `Integrate Clint (Upsert + Tag + Deal)` (Code)
- Apenas IO com Clint, sem decidir regra de lista.
9. `Respond Manychat`
10. `Fail Execution On Error Status`

### 3.2 Principio de precedencia

`overrides de runtime > config da lista > config global > defaults`

Aplicacao pratica:
- campos da lista sobrescrevem global;
- override explicito no payload (quando permitido) sobrescreve lista;
- ausencia de lista aplica fallback para `default_list_key` com flag de auditoria.

## 4) Contrato da camada de configuracao

## 4.1 Entrada minima do `Resolve Config`

```json
{
  "runtime_context": {
    "requested_list_key": "cj_ppt_webinar",
    "overrides": {}
  },
  "config_catalog": {}
}
```

## 4.2 Estrutura do `config_catalog`

```json
{
  "version": "wf-c-manychat-intake-clint@fase3-v1",
  "defaults": {
    "list_key": "cj_ppt_webinar",
    "dedupe_strategy": "phone_then_email",
    "retry": { "max_attempts": 3, "base_delay_ms": 300 }
  },
  "global": {
    "clint_base_url": "https://api.clint.digital/v1",
    "source": "manychat_webhook"
  },
  "lists": {
    "cj_ppt_webinar": {
      "origin_name": "Perpetuo Webinario",
      "origin_id": "bd1bd846-0c87-4acb-b221-d7f8d2089e68",
      "tag_name": "cj-ppt-webinar",
      "lista_origem": "cj-ppt-webinar",
      "produto": "VDE Carreiras Juridicas Ciclo Prioritario",
      "value": 2557
    }
  },
  "aliases": {
    "global": {
      "list_key": ["list_key", "lista_key", "origem_lista"],
      "nome": ["nome", "name", "full_name"],
      "email": ["email", "e-mail", "email_address"],
      "whatsapp": ["whatsapp", "whatsapp_phone", "phone", "telefone"]
    },
    "by_list": {
      "cj_ppt_webinar": {
        "carreira_pretendida": ["carreira_concursos", "carreira concursos"]
      }
    }
  }
}
```

## 4.3 Saida obrigatoria do `Resolve Config`

```json
{
  "config_resolution": {
    "config_version": "wf-c-manychat-intake-clint@fase3-v1",
    "requested_list_key": "cj_ppt_webinar",
    "list_key": "cj_ppt_webinar",
    "list_key_fallback_applied": false
  },
  "resolved_config": {
    "origin_id": "...",
    "origin_name": "...",
    "tag_name": "...",
    "lista_origem": "...",
    "produto": "...",
    "value": 2557,
    "clint_base_url": "https://api.clint.digital/v1",
    "dedupe_strategy": "phone_then_email",
    "retry": { "max_attempts": 3, "base_delay_ms": 300 }
  },
  "resolved_aliases": {
    "nome": ["..."],
    "email": ["..."],
    "whatsapp": ["..."],
    "carreira_pretendida": ["..."]
  }
}
```

## 5) Regras de modularizacao (obrigatorias)

1. `Prepare Runtime Context` nao pode conhecer regra de negocio de lista.
2. `Resolve Config` nao pode chamar API externa.
3. `Normalize + Validate Input` nao pode conter `LIST_CONFIGS` hardcoded.
4. `Build Clint Payloads` nao pode ler headers nem decidir token.
5. `Integrate Clint` nao pode conter aliases de entrada.
6. Qualquer nova lista deve ser adicionada apenas no `Config Catalog`.

## 6) Plano de implementacao executavel (seguivel por mim)

## Etapa 3.1 - Criar camada de contexto de runtime
Status: concluida (2026-03-06)

Acoes:
1. Criar node `Prepare Runtime Context` antes de qualquer normalizacao.
2. Extrair `payload`, `headers`, `execution_id`, `received_at`.
3. Encaminhar objeto limpo para os proximos nodes.

Criterio de aceite:
- nenhum node posterior precisa acessar diretamente `$json.body` bruto.

## Etapa 3.2 - Criar node dedicado de catalogo
Status: concluida (2026-03-06)

Acoes:
1. Adicionar `Config Catalog` (Code node) com bloco JSON unico.
2. Mover para esse node: defaults, global, lists, aliases.
3. Remover esses blocos do node de normalizacao.

Criterio de aceite:
- existe um unico ponto de edicao para cadastrar lista nova.

## Etapa 3.3 - Implementar `Resolve Config`
Status: concluida (2026-03-06)

Acoes:
1. Criar node Code para resolver `list_key` e aplicar precedencia.
2. Fazer merge de aliases com deduplicacao.
3. Validar schema minimo (`origin_id`, `value`, `clint_base_url`).
4. Retornar erro de contrato (`CONFIG_ERROR`) quando faltar requisito.

Criterio de aceite:
- payload invalido de configuracao falha antes de chamar Clint.

## Etapa 3.4 - Refatorar normalizacao para consumir apenas `resolved_aliases`
Status: concluida (2026-03-06)

Acoes:
1. Ajustar `Normalize + Validate Input` para depender de `runtime_context + resolved_aliases`.
2. Manter validacao de identidade (`email` ou telefone).
3. Preservar sanitizacao e contrato de erro atual.

Criterio de aceite:
- node nao referencia mais `LIST_CONFIGS` ou `GLOBAL_INPUT_ALIASES`.

## Etapa 3.5 - Separar builder de payload Clint
Status: concluida (2026-03-06)

Acoes:
1. Criar `Build Clint Payloads` (Code).
2. Mover construcao de `contactPayload` e `dealPayloadBase` para esse node.
3. Node de integracao passa a consumir payload pronto.

Criterio de aceite:
- integracao fica focada em chamadas HTTP e tratamento de erro.

## Etapa 3.6 - Ajustar integracao para parametros resolvidos
Status: concluida (2026-03-06)

Acoes:
1. Trocar consumo de config antiga por `resolved_config`.
2. Reaproveitar retry, auditoria e dedupe via chaves de config.
3. Manter compatibilidade com `Respond` e `Fail Execution`.

Criterio de aceite:
- comportamento funcional igual ao atual para `cj_ppt_webinar`.

## Etapa 3.7 - Testes de regressao e onboarding de lista
Status: concluida (2026-03-06)

Acoes:
1. Rodar smoke test de sucesso.
2. Rodar caso de validacao sem identidade.
3. Rodar caso de config invalida (lista inexistente + sem default).
4. Cadastrar lista fake (`test_lista_nova`) apenas no catalogo.
5. Validar que fluxo processa nova lista sem editar algoritmo.

Execucoes validadas:
- `id=41` (`manychat-intake-test`): smoke de sucesso (`status=success`, `config_version=wf-c-manychat-intake-clint@fase3-etapa37-2026-03-06`).
- `id=42` (`manychat-intake-test`): validacao sem identidade (`status=validation_error`, `step=validate_payload`, `http_status=400`).
- teste local do node `Resolve Config`: `CONFIG_ERROR` com `step=resolve_config` para lista inexistente sem default valido no catalogo.
- `id=43` (`manychat-intake-test`): onboarding `test_lista_nova` funcionando sem editar algoritmo (`list_key=test_lista_nova`, `tag_name=test-lista-nova`).
- `id=44` (`manychat-intake` - producao): smoke de sucesso apos deploy (`status=success`).

Criterio de aceite:
- nova lista sobe apenas por catalogo e passa no fluxo.

## 7) Checklist de Definition of Done (Fase 3)

- [x] Existe node dedicado para `Config Catalog`.
- [x] Existe node dedicado para `Resolve Config`.
- [x] Normalizacao nao possui configuracao embutida de lista.
- [x] Integracao Clint nao possui alias de entrada.
- [x] Contrato de erro inclui `CONFIG_ERROR` com `step` explicito.
- [x] Inclusao de nova lista exige apenas editar catalogo.
- [x] `workflow.fase1.json` atualizado e documentado no `README.md`.

## 8) Estrategia de rollout

1. Publicar primeiro em endpoint de teste (`manychat-intake-test`).
2. Validar 3 execucoes reais sem regressao.
3. Publicar em producao (`manychat-intake`).
4. Monitorar 24h com foco em:
- `list_key_fallback_applied`
- `CONFIG_ERROR`
- `MISSING_CLINT_TOKEN`
- tempo medio `duration_ms`.

## 9) Riscos e mitigacoes

Risco: erro no merge de aliases altera campo mapeado.
Mitigacao: fixture de payload por lista e snapshot do `normalized_payload`.

Risco: catalogo crescer e ficar dificil manter no Set node.
Mitigacao: proxima evolucao opcional: extrair `Resolve Config` para subworkflow compartilhado.

Risco: override de runtime virar vetor de inconsistencias.
Mitigacao: whitelist de chaves permitidas para override.

## 10) Proxima evolucao (fase 3.1 opcional)

Extrair `Resolve Config` para subworkflow `WF Shared - Config Resolver` e usar `Execute Workflow`, permitindo reaproveitamento em outros workflows de intake sem duplicar codigo.
