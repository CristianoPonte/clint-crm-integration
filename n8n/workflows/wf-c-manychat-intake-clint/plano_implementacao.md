# Plano de Implementacao - WF C (Manychat -> n8n -> Clint)

## 1) Identificacao

- Workflow: `WF C - Manychat Intake Clint`
- Pasta: `n8n/workflows/wf-c-manychat-intake-clint/`
- Data do plano: `2026-03-06`
- Objetivo: receber lead do Manychat, validar/normalizar dados, evitar duplicacao de contato na Clint e criar deal novo para cada entrada.

## 2) Escopo do projeto

### Em escopo
- Receber `POST` do Manychat (inicialmente testado via Postman).
- Campos de entrada: `nome`, `email` (opcional), `whatsapp`, UTMs e `carreira_pretendida`.
- Validacao e normalizacao do payload antes de integrar com a Clint.
- Upsert de contato (sem duplicar contato).
- Adicao de tag no contato.
- Criacao de deal sempre novo (duplicacao de deal permitida).
- Registro dos campos customizados conforme padrao da automacao anterior.

### Fora de escopo (neste primeiro ciclo)
- Enriquecimento externo de dados.
- Deduplicacao fuzzy por nome.
- Regras de negocio de fechamento de deal.

## 3) Campos e mapeamento

Fonte de verdade dos campos: `docs/reference/regras_custom_fields.md`.

### 3.1 Entrada esperada do Manychat (payload canonico)
- `nome` (obrigatorio)
- `email` (opcional)
- `whatsapp` (recomendado; aceitar sem email)
- `carreira_pretendida` (opcional no payload, mas previsto para contato)
- `utm_source` (opcional)
- `utm_medium` (opcional)
- `utm_campaign` (opcional)
- `utm_term` (opcional)
- `utm_content` (opcional)

Regra minima de aceite: pelo menos um entre `email` e `whatsapp` deve estar preenchido.

### 3.2 Mapeamento para CONTACT (Clint)
- `name` <- `nome`
- `email` <- `email`
- `phone`/`ddi` <- `whatsapp` (normalizado)
- `fields.carreira_pretendida` <- `carreira_pretendida`

### 3.3 Mapeamento para DEAL (Clint)
- `fields.utm_source` <- `utm_source`
- `fields.utm_medium` <- `utm_medium`
- `fields.utm_campaign` <- `utm_campaign`
- `fields.utm_term` <- `utm_term`
- `fields.utm_content` <- `utm_content`
- `fields.lista_origem` <- `cj-ppt-webinar` (fixo)
- `fields.data_importacao` <- timestamp da execucao (gerado no workflow)
- `fields.produto` <- `VDE Carreiras Jurídicas Ciclo Prioritário` (fixo)
- `value` <- `2557` (fixo; equivalente a `R$2557`)

### 3.4 Configuracao de origem (confirmada)
- `origin_name`: `Perpétuo Webinário`
- `origin_id`: `bd1bd846-0c87-4acb-b221-d7f8d2089e68`
- `stage_id`: resolver dinamicamente o stage do tipo `BASE` dentro dessa origin.
- `list_tag_name` (tag no contato): `cj-ppt-webinar` (fixo)
- `lista_origem` (deal field): `cj-ppt-webinar` (fixo)

Observacao: campos vazios nao devem ser enviados no `fields`.

## 4) Estrategia tecnica do workflow no n8n

## 4.1 Trigger e contratos
- Webhook de teste: `POST /webhook/manychat-intake-test`
- Webhook de producao: `POST /webhook/manychat-intake`
- `responseMode`: `responseNode`
- Autenticacao no teste: `none` (sem auth/token, temporario para homologacao inicial).
- Persistir `webhookId` no JSON versionado (evitar `not registered`).

## 4.2 Desenho de nodes (versao alvo)
1. `Webhook Manychat (Test)`
2. `Webhook Manychat (Prod)`
3. `Code - Normalize Input`
- Detecta variacoes de chave (`name`/`nome`, `phone`/`whatsapp`).
- Limpa strings, remove nulos e padroniza estrutura.
4. `Code - Validate Payload`
- Garante ao menos `email` ou `whatsapp`.
- Retorna erro 400 com mensagem clara se invalido.
5. `Code - Build Clint Payloads`
- Separa `contactPayload` e `dealPayload`.
- Injeta `data_importacao`.
6. `HTTP - Get Origins`
- `GET /origins?limit=250`
7. `Code - Resolve Origin + Base Stage`
- Seleciona origem por `origin_id` fixo do projeto.
- Busca stage com `type=BASE`.
8. `HTTP - Search Contact by Email`
9. `HTTP - Search Contact by Phone` (fallback)
10. `IF - Contact Exists?`
11. `HTTP - Update Contact` (quando encontrado)
12. `HTTP - Create Contact` (quando nao encontrado)
13. `HTTP - Add Tag`
14. `HTTP - Create Deal`
15. `Respond to Webhook`
- Sucesso: 200 com ids e resumo.
- Erro validacao: 400.
- Erro integracao: 502/500 com `execution_id`.

## 4.3 Regras de deduplicacao
- Prioridade 1: busca por email exato.
- Prioridade 2: busca por telefone normalizado (somente digitos).
- Se contato existir: atualizar contato existente.
- Se nao existir: criar novo contato.
- Deal: sempre criar novo deal (sem bloqueio por historico anterior).

## 4.4 Regra de telefone/whatsapp
- Remover caracteres nao numericos.
- Se iniciar com `55` e tamanho > 11, usar `ddi=+55` e remover prefixo no `phone`.
- Se tiver 10 ou 11 digitos, assumir `ddi=+55`.
- Se invalido, nao enviar `phone`.

## 5) Plano de testes (com Postman antes do Manychat real)

## 5.1 Fase T0 - Descobrir formato real de chegada
- Objetivo: capturar o shape exato do payload que o Manychat envia.
- Acao:
1. Apontar Postman para `manychat-intake-test`.
2. Enviar 3 payloads candidatos (flat JSON, nested JSON, form-urlencoded).
3. Logar no retorno o payload bruto + payload normalizado.
- Resultado esperado: definir contrato final de entrada para producao.

## 5.2 Fase T1 - Validacao de dados
Casos:
1. Sem `email` e sem `whatsapp` -> deve retornar 400.
2. Com `whatsapp` mascarado (`(85) 99999-0000`) -> deve normalizar.
3. Com UTM parcial -> deve aceitar e enviar so campos preenchidos.
4. Sem `email`, mas com `whatsapp` -> deve processar com sucesso.
5. Com `carreira_pretendida` -> deve gravar no `fields` do contato.

## 5.3 Fase T2 - Integracao Clint
Casos:
1. Contato novo -> cria contato, aplica tag, cria deal.
2. Contato existente por email -> atualiza contato, aplica tag, cria deal.
3. Contato existente por whatsapp sem email -> atualiza contato, aplica tag, cria deal.
4. Duas chamadas iguais seguidas -> contato unico, deals duplicados permitidos.

## 5.4 Fase T3 - Regressao e hardening
- Confirmar sem quebra no ambiente atual do n8n:
- Code node sem `fetch` (usar `this.helpers.httpRequest`).
- Nao usar `process.env` em Code node.
- Timeouts/retries configurados em HTTP Request.

## 5.5 Evidencia de execucao real (Manychat)
- Workflow publicado e ativo: `WF C - Manychat Intake Clint (Bootstrap)` (`id=bnjM2OPkMHkrcoZU`).
- Endpoint validado: `POST https://sisifo.metodovde.com.br/webhook/manychat-intake-test`.
- Execucao real confirmada:
  - `execution_id=16`
  - `startedAt=2026-03-06T01:52:11.787Z`
  - `status=success`
  - `normalized_payload.nome`: preenchido
  - `normalized_payload.email`: preenchido
  - `normalized_payload.whatsapp`: preenchido
  - `normalized_payload.carreira_pretendida`: vazio (aceitavel para este contato)
  - `normalized_payload.utm_*`: vazios (aceitavel para este contato)

## 6) Observabilidade, seguranca e operacao

- Credenciais Clint via n8n Credentials (nao trafegar token no payload).
- Sanitizar logs para nao expor PII completa.
- Retornar `execution_id` nas respostas para auditoria.
- Criar padrao de erro:
- `code`, `message`, `step`, `execution_id`.
- Implementar `continueOnFail=false` para falhas criticas.
- Ativar autenticao do webhook (header token compartilhado com Manychat) no go-live.

## 7) Entregaveis

1. `workflow.fase1.json` (WF C com teste + producao).
2. README local do workflow com entrada/saida/status.
3. Atualizacao do pacote Postman com requests de teste do WF C.
4. Atualizacao do `PROGRESS.md` apos homologacao.

## 8) Sequencia de implementacao proposta

1. Implementar endpoint de teste e node de normalizacao.
2. Validar formato com Postman e congelar contrato final.
3. Implementar integracao Clint (upsert + tag + deal) usando configuracoes fixas ja definidas (`origin_id`, `tag`, `lista_origem`, `produto`, `value`).
4. Validar cenarios T1/T2.
5. Publicar endpoint de producao.
6. Rodar smoke test final e preparar handoff.

## 9) Dados pendentes para executar a implementacao

Sem pendencias bloqueantes para iniciar a fase 2.
Decisao atual: manter sem auth/token apenas durante homologacao inicial; endurecer seguranca no go-live.

## 10) Exemplo de payload de teste inicial (Postman)

```json
{
  "nome": "Lead Teste",
  "whatsapp": "+55 (85) 99999-0000",
  "carreira_pretendida": "Defensoria Publica",
  "utm_source": "facebook",
  "utm_medium": "cpc",
  "utm_campaign": "campanha_manychat_marco",
  "utm_term": "juridico",
  "utm_content": "anuncio_a"
}
```

## 11) Proximo passo claro (concluido)

Implementado o `workflow.fase1.json` do WF C com integracao Clint ponta a ponta:
- Upsert de contato por email (quando houver) com fallback por whatsapp.
- Aplicacao da tag `cj-ppt-webinar`.
- Criacao de deal em `Perpétuo Webinário` (stage `BASE`) com:
  - `fields.lista_origem = cj-ppt-webinar`
  - `fields.data_importacao = timestamp da execucao`
  - `fields.produto = VDE Carreiras Jurídicas Ciclo Prioritário`
  - `value = 2557`

## 12) Status real da implementacao (executado em 2026-03-06)

### 12.1 Workflow publicado
- Workflow ativo: `WF C - Manychat Intake Clint (Fase 1)` (`id=IDbkLRon0vF0r6ZM`).
- Workflow bootstrap desativado para evitar conflito de webhook:
  - `WF C - Manychat Intake Clint (Bootstrap)` (`id=bnjM2OPkMHkrcoZU`).

### 12.2 Ajustes aplicados apos testes reais
- Parsing expandido para payload real do Manychat:
  - telefone em `whatsapp_phone` (com fallbacks adicionais);
  - carreira em `custom_fields.Carreira_Concursos`;
  - leitura de aliases de UTM em caixa alta/baixa.
- Fallback de token Clint aplicado para homologacao quando Manychat nao envia header.
- Node adicional `Fail Execution On Error Status` apos `Respond to Webhook` para marcar execucoes com erro no log do n8n.

### 12.3 Evidencias de execucao
- `execution_id=17` (`2026-03-06T02:07:27Z`): sucesso (contato criado + deal criado).
- `execution_id=18` (`2026-03-06T02:07:49Z`): sucesso (contato atualizado + novo deal).
- `execution_id=19` (`2026-03-06T02:13:32Z`): payload real detectado com `whatsapp_phone`; validacao falhou antes do ajuste de aliases.
- `execution_id=21` (`2026-03-06T02:20:25Z`): sucesso com shape real do Manychat apos correcao.
- `execution_id=22` (`2026-03-06T02:26:42Z`): erro de validacao proposital; execucao marcada como `error` no n8n.
- `execution_id=23` (`2026-03-06T02:28:04Z`): retentativa com sucesso.
