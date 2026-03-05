# Plano n8n - Migração do Integrador CSV -> Clint

## 1. Contexto
Hoje o fluxo está em Python/FastAPI e faz:
- Upload de CSV via formulário.
- Resolução dinâmica de `origin_id` por nome.
- Descoberta de `stage_id` tipo `BASE`.
- Upsert de contato por e-mail e fallback por telefone.
- Aplicação de tag.
- Criação de deal com campos nativos e customizados.
- Registro de histórico de execução.

Objetivo: migrar esse fluxo para n8n com foco em automação, mantendo rastreabilidade e reduzindo acoplamento com backend custom.

---

## 2. Decisão Técnica (JS no n8n vs Python)

### Recomendação principal
Usar **n8n + JavaScript (Code node)** como base.

### Motivos
- Melhor integração com o runtime do n8n (expressions + itens JSON).
- Menor complexidade operacional (sem serviço Python adicional).
- Manutenção mais rápida no próprio editor de workflow.
- Menor custo de observabilidade (logs e execuções centralizadas no n8n).

### Quando manter Python
Somente se houver necessidade real de:
- Transformações pesadas de dados (pandas avançado).
- Algoritmos específicos não triviais em JS.
- Reuso obrigatório de bibliotecas legadas.

Conclusão: para o fluxo atual, **JS no n8n cobre 100%** sem perda funcional.

---

## 3. Objetivos do Produto
- Automatizar importação de leads (CSV -> Clint) com controle por execução.
- Padronizar deduplicação e criação de oportunidades.
- Garantir consistência com regras do PRD atual.
- Preparar execução automática (agendada e/ou por webhook).
- Habilitar auditoria e troubleshooting por execução.

---

## 4. Escopo

### Em escopo (MVP n8n)
- Workflow de ingestão de CSV.
- Workflow de webhook `clint-won`.
- Mapeamento de campos (contato/deal) equivalente ao `mapper_service.py`.
- Relatório final com sucessos/falhas por linha.
- Persistência de histórico em destino definido (Google Sheets, DB ou storage).

### Fora de escopo inicial
- UI custom avançada fora do n8n.
- Deduplicação fuzzy avançada.
- Regras de enriquecimento externo.

---

## 5. Arquitetura Alvo (n8n)

## 5.1 Workflow A - Importação CSV para Clint
1. Trigger:
- `Webhook` (multipart) ou `Form Trigger` n8n.
2. Parse:
- `Extract From File` (CSV -> itens JSON).
3. Preparação:
- `Code` node para normalizar headers, limpar valores e separar `contact_fields` / `deal_fields`.
4. Contexto de origem:
- `HTTP Request` -> `GET /origins?limit=250`.
- `Code` node para encontrar `origin_id` por nome e `stage_id` tipo `BASE`.
5. Loop por linha:
- `Loop Over Items` (ou `Split in Batches`).
- `HTTP Request` buscar contato por e-mail.
- Se não achar e houver telefone, buscar por telefone.
- `HTTP Request` criar/atualizar contato.
- `HTTP Request` adicionar tag.
- `HTTP Request` criar deal.
6. Consolidação:
- `Code` node para somar sucesso/falha e montar payload final.
7. Resposta:
- `Respond to Webhook` com relatório.

## 5.2 Workflow B - Webhook de Deal Ganha
1. Trigger `Webhook` (`/webhook/clint-won`).
2. Extrair `contact_id`, `deal_id`, valor e produto.
3. Buscar contato/tags na Clint.
4. Persistir linha no Google Sheets.
5. Enviar alerta no Slack.
6. Retornar `200`.

## 5.3 Workflow C - Automação sem intervenção manual
Opções:
- `Schedule Trigger` + leitura de CSV no Google Drive/S3.
- `Webhook` chamado por sistema externo.

---

## 6. Requisitos Funcionais
- RF01: importar CSV com separador `,` ou `;`.
- RF02: aceitar campos de entrada: `origin_name`, `product_name`, `product_value`, `list_tag_name`.
- RF03: mapear headers figurativos para identificadores da Clint.
- RF04: ignorar campos vazios no envio de `fields`.
- RF05: upsert por e-mail e fallback por telefone.
- RF06: criar deal no stage `BASE` da origem correta.
- RF07: aplicar tag no contato.
- RF08: registrar `lista_origem` e `data_importacao` no deal.
- RF09: responder com relatório completo por execução.
- RF10: suportar webhook de venda ganha para Sheets e Slack.

---

## 7. Requisitos Não Funcionais
- RNF01: idempotência básica por execução (evitar retrabalho acidental).
- RNF02: logs por execução com correlação (`execution_id`).
- RNF03: tolerância a falha por item (erro em uma linha não para lote inteiro).
- RNF04: timeout/retry controlados em chamadas HTTP.
- RNF05: segurança de credenciais via n8n Credentials.
- RNF06: limite de throughput para evitar rate limit da Clint.

---

## 8. Requisitos de Segurança
- Guardrail: não usar `DELETE` na Clint.
- Credenciais em variáveis/credentials do n8n, nunca hardcoded.
- Rotacionar token de API após implantação.
- Sanitizar logs (não expor PII completa nem tokens).
- Segregar ambiente `sandbox` e `produção`.

---

## 9. Mapeamento de Componentes Python -> n8n
- `main.py /upload` -> Workflow A (`Webhook/Form` + pipeline).
- `mapper_service.py` -> `Code` node de mapeamento.
- `clint_service.py` -> nós `HTTP Request`.
- `historico.json` -> armazenamento de execução (Sheets/DB/Data Store n8n).
- `main.py /webhook/clint-won` -> Workflow B.

---

## 10. PRD (Produto n8n)

## 10.1 Visão do Produto
Migrar o integrador atual para n8n para centralizar automações, reduzir manutenção de código backend e permitir operação automática com menor esforço.

## 10.2 Usuários
- Operação comercial/marketing.
- Time de dados/automação.

## 10.3 Problema
Processo atual depende de app dedicado e operação manual; pouca flexibilidade para escalar automações e governança no fluxo.

## 10.4 Solução
Workflows n8n modulares para ingestão, processamento, integração Clint, notificações e histórico.

## 10.5 Métricas de Sucesso
- Taxa de sucesso de importação >= 98%.
- Tempo de processamento por 1.000 linhas dentro do SLO acordado.
- Redução de intervenção manual em >= 80%.
- Zero regressão de regras de negócio do PRD atual.

## 10.6 Critérios de Aceite
- CA01: mesmas regras de negócio validadas do fluxo Python.
- CA02: relatório final com linhas de erro detalhadas.
- CA03: webhook de venda ganha funcionando com Sheets + Slack.
- CA04: workflow versionado e implantável por API.
- CA05: execução automática por agendamento validada.

---

## 11. Plano de Implementação (após acesso VPN)

### Fase 0 - Acesso e baseline
- Validar conexão VPN.
- Validar acesso n8n API `/api/v1/workflows`.
- Criar credenciais no n8n (Clint, Slack, Google).

### Fase 1 - MVP Importação
- Criar Workflow A.
- Portar lógica de mapeamento.
- Implementar upsert + tag + deal.
- Testar com CSV de amostra.

### Fase 2 - Webhook de vendas
- Criar Workflow B.
- Integrar Sheets e Slack.
- Testar com payload real/simulado.

### Fase 3 - Operação automática
- Criar Workflow C (Schedule ou ingestão por Drive/S3).
- Definir política de retry/alertas.
- Ajustar monitoramento.

### Fase 4 - Hardening
- Rate limiting.
- Idempotência por hash de linha.
- Runbook de incidente.

---

## 12. Automação de Deploy via API n8n
- Estratégia:
1. Exportar workflow JSON versionado no repositório.
2. Script de deploy:
   - busca por nome (`GET /workflows`),
   - cria (`POST`) se não existir,
   - atualiza (`PATCH`) se existir,
   - ativa workflow.
3. Executar smoke test pós-deploy.

---

## 13. Dependências e Pré-requisitos
- Acesso VPN funcional.
- n8n API key válida.
- Credenciais Clint/Slack/Google com permissões corretas.
- Ambiente de teste com dados fictícios.
- Definição de destino para histórico (Sheets/DB).

---

## 14. Riscos e Mitigações
- Risco: rate limit da Clint.
  - Mitigação: lotes pequenos + retry exponencial.
- Risco: divergência de mapeamento de colunas.
  - Mitigação: tabela de mapeamento central e testes de regressão.
- Risco: duplicação de deals em reprocesso.
  - Mitigação: chave de idempotência por execução/linha.
- Risco: quebra por mudança em payload da Clint.
  - Mitigação: validação de schema e monitoramento de falhas.

---

## 15. Checklist Operacional (Go-Live)
- [ ] VPN conectada e estável.
- [ ] API n8n respondendo.
- [ ] Workflows importados e ativados.
- [ ] Credenciais validadas.
- [ ] Teste fim-a-fim aprovado.
- [ ] Alertas e logs configurados.
- [ ] Plano de rollback documentado.

