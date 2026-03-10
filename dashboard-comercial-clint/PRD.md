# Product Requirements Document (PRD) - Dashboard Comercial Clint

Status: Planejamento aprovado para detalhamento tecnico
Data: 2026-03-07
Owner sugerido: RevOps / Comercial / Produto Interno
Stakeholders principais: Comercial, RevOps, Gestao, BI, Engenharia

## 1. Visao Geral

Construir uma aplicacao propria e isolada para monitoramento operacional e analitico do funil comercial da Clint, com backend em Python e frontend web dedicado, capaz de consolidar dados da Clint, calcular metricas de SLA e funil, e apresentar um dashboard gerencial com filtros, tendencias, alertas e drill-downs.

O produto nao rodara no n8n. O n8n permanece apenas como referencia de regra de negocio, mapeamento inicial de campos e aprendizado operacional.

## 2. Contexto

Hoje ja existe uma trilha de automacao que monitora SLA operacional por etapa do funil comercial da origem `Perpetuo Webinario`, com regras por transicao, agrupamento por vendedora e snapshots de deals atrasados. Essa solucao atende notificacao diaria, mas nao atende analise historica completa de funil, conversao, perdas, reunioes e performance gerencial de ponta a ponta.

A oportunidade deste produto e transformar um monitor operacional de atraso em uma plataforma interna de inteligencia comercial.

## 3. Problema

O time comercial hoje nao possui uma visao consolidada, historica e confiavel para responder, de forma continua, perguntas como:

- Em quais etapas o funil trava mais.
- Quais listas, origens e campanhas geram leads com melhor qualidade.
- Quais vendedores convertem melhor e onde perdem mais deals.
- Quais motivos de perda mais impactam o resultado.
- Qual o tempo real de passagem entre etapas.
- Qual o backlog operacional por SLA e por responsavel.
- Quantas reunioes estao sendo marcadas e quanto elas influenciam a conversao.

Sem uma aplicacao propria com historico estruturado, a operacao fica dependente de consultas manuais, snapshots incompletos e leitura fragmentada do CRM.

## 4. Objetivo do Produto

Criar um dashboard comercial que una operacao e gestao, permitindo:

- acompanhar SLA de atendimento e permanencia por etapa;
- medir conversao do funil por etapa, origem, lista, campanha, produto e vendedor;
- analisar perdas, reunioes e resultado por responsavel;
- gerar uma base historica confiavel para comparacoes e tendencias;
- suportar futuras evolucoes como alertas, relatorios automatizados e insights assistidos.

## 5. Objetivos de Negocio

- Reduzir o volume de deals atrasados nas etapas criticas.
- Aumentar a velocidade de passagem entre etapas.
- Melhorar taxa de conversao por origem/lista.
- Melhorar visibilidade de performance por vendedor.
- Tornar motivos de perda analisaveis e acionaveis.
- Criar uma camada de dados propria para o comercial, sem dependencia de consultas manuais no CRM.

## 6. Metas de Sucesso

### 6.1 Metas de adocao

- Pelo menos 80% das liderancas comerciais usando o dashboard semanalmente apos 30 dias do go-live.
- Pelo menos 60% do time comercial consultando o dashboard ou relatorio automatizado pelo menos 3 vezes por semana.

### 6.2 Metas de qualidade de dados

- 95% ou mais dos deals sincronizados com sucesso nas janelas programadas.
- 99% ou mais dos registros com `stage_id`, `status`, `created_at` e `updated_stage_at` validos quando disponiveis na origem.
- Menos de 5% dos deals classificados em buckets `desconhecido` para campos obrigatorios de analise, apos fase de estabilizacao.

### 6.3 Metas operacionais e de negocio

- Reducao de pelo menos 20% no volume medio de deals fora do SLA em 60 dias apos uso operacional.
- Queda de pelo menos 15% no tempo mediano da etapa mais critica em 90 dias.
- Capacidade de explicar ao menos 80% das perdas por motivo estruturado, apos padronizacao do processo.

## 7. Nao Objetivos

Ficam fora do escopo inicial:

- editar deals diretamente na Clint;
- substituir o CRM da Clint;
- automacoes de notificacao no MVP;
- previsao de vendas baseada em machine learning no MVP;
- gestao financeira completa ou comissionamento;
- criacao de um builder generico de dashboards.

## 8. Usuarios e Perfis

### 8.1 Lider comercial

Necessita enxergar gargalos, desempenho por vendedor, risco de SLA e tendencia de conversao.

### 8.2 RevOps / BI

Necessita confiabilidade de dados, rastreabilidade, visao por origem/lista/campanha e capacidade de auditar definicoes.

### 8.3 Vendedor / closer

Necessita visibilidade operacional do proprio backlog, deals sem avancar, reunioes pendentes e carteira por etapa.

### 8.4 Gestao executiva

Necessita leitura simples de volume, conversao, perdas, resultado por canal e saude da operacao.

## 9. Jobs To Be Done

- Quando a lideranca abrir o dashboard, ela quer entender rapidamente onde o funil esta travando para priorizar cobranca e suporte.
- Quando o RevOps analisar uma campanha, ele quer saber se o volume gerado virou reuniao, avancou no funil e se transformou em venda.
- Quando um gestor avaliar o time, ele quer separar problema de volume de problema de processo.
- Quando o time comercial revisar perdas, ele quer encontrar os principais motivos, em que etapa ocorrem e em quais segmentos aparecem mais.

## 10. Estado Atual do Dominio

### 10.1 Origem principal mapeada

- Origem alvo atual: `Perpetuo Webinario`
- `origin_id`: `bd1bd846-0c87-4acb-b221-d7f8d2089e68`

### 10.2 Etapas atualmente mapeadas

- `Lead Cadastrado`
- `Contato Realizado`
- `Diagnostico`
- `Negociacao`
- `Follow-up`
- `Fechado`

### 10.3 Regras de negocio ja identificadas

- O monitoramento operacional considera apenas deals `OPEN` para atraso.
- O tempo de referencia de permanencia usa `updated_stage_at` com fallback para `created_at`.
- Deals em etapa de fechamento nao entram em atraso operacional.
- Agrupamento operacional atual e por `user.id`, com bucket `sem_responsavel`.
- Ha classificacao de fechamento por `status`: `WON` e `LOST`.
- Apenas a regra `Lead Cadastrado -> Contato Realizado = 24h` esta oficialmente ativa neste momento; as demais ainda dependem de definicao de negocio.

### 10.4 Campos ja conhecidos no deal

- Nativos e operacionais:
  - `id`
  - `origin_id`
  - `stage_id`
  - `stage`
  - `status`
  - `created_at`
  - `updated_at`
  - `updated_stage_at`
  - `latest_meeting_datetime`
  - `latest_meeting_link`
  - `user`
  - `contact`
  - `fields`

- Campos customizados de deal ja documentados:
  - `produto`
  - `utm_source`
  - `utm_medium`
  - `utm_campaign`
  - `utm_term`
  - `utm_content`
  - `lista_origem`
  - `data_importacao`
  - `sla_status`

### 10.5 Campos complementares do contato, uteis para segmentacao

- `carreira_pretendida`
- `profissao`
- `tempo_de_estudo`
- `renda_familiar`
- `maior_dificuldade`
- `features_desejadas`
- outros campos de perfil historicamente ja usados na conta

## 11. Principais Hipoteses de Produto

- H1: O principal ganho inicial vira de visibilidade de gargalo por etapa e backlog por vendedor.
- H2: Conversao por `lista_origem` e por UTM mostrara diferencas relevantes de qualidade entre canais.
- H3: O simples ato de estruturar `motivo_perda` e exibir isso em Pareto dara insumos mais acionaveis do que apenas acompanhar `WON` e `LOST`.
- H4: Metricas de mediana e percentis por etapa serao mais uteis do que medias simples para tomada de decisao.
- H5: Se reunioes forem medidas corretamente, sera possivel identificar listas com volume alto e baixa qualificacao.

## 12. Escopo do MVP

### 12.1 Em escopo

- Aplicacao propria com backend Python e frontend dedicado.
- Ingestao automatizada dos dados da Clint.
- Persistencia historica em banco proprio.
- Dashboard com filtros globais e drill-downs.
- Analise por origem, lista, UTM, etapa, status e vendedor.
- Calculo de SLA operacional atual por etapa.
- Analise de conversao por etapa e total.
- Analise de perdas, se houver campo estruturado ou regra acordada.
- Analise de reunioes, se houver campo estruturado disponivel.
- Relatorio/insight resumido dentro da aplicacao.

### 12.2 Fora do escopo do MVP

- Escrita de atualizacoes na Clint.
- Edicao inline de regras no dashboard, se o painel administrativo nao existir ainda.
- Gerador dinamico de KPIs customizados por usuario.
- Modelo preditivo de chance de ganho.

## 13. Dependencias Criticas

- Definicao de SLA para todas as transicoes relevantes.
- Confirmacao se SLA sera medido em horas corridas ou horas uteis.
- Confirmacao se o dashboard sera mono-origem no MVP ou multi-origem desde o inicio.
- Confirmacao do campo oficial de `motivo_perda`.
- Confirmacao do campo oficial de contagem de reunioes, caso exista.
- Confirmacao se a API da Clint oferece historico de mudanca de etapa. Se nao oferecer, sera necessario inferir mudancas via snapshots periodicos.

## 14. Requisitos Funcionais

### RF01. Autenticacao e acesso

- O sistema deve suportar acesso autenticado para usuarios internos.
- O sistema deve suportar, no minimo, perfis de leitura e administracao.

### RF02. Sincronizacao com a Clint

- O sistema deve consumir dados da Clint via API de forma automatizada.
- O sistema deve sincronizar, no minimo, `deals`, `users`, `origins` e catalogo de campos.
- O sistema deve suportar sincronizacao recorrente sem dependencia do n8n.

### RF03. Persistencia historica propria

- O sistema deve armazenar historico de snapshots e/ou eventos em banco proprio.
- O sistema deve manter rastreabilidade da origem do dado e timestamps de sincronizacao.

### RF04. Dashboard executivo

- O sistema deve exibir KPIs executivos consolidados para periodo selecionado.
- O sistema deve permitir comparacao contra periodo anterior.

### RF05. Dashboard de funil

- O sistema deve exibir quantidade de leads por etapa.
- O sistema deve exibir conversao entre etapas e conversao total.
- O sistema deve permitir segmentacao por origem, lista, UTM, produto e vendedor.

### RF06. Dashboard de SLA

- O sistema deve exibir tempo atual em etapa para deals em aberto.
- O sistema deve exibir mediana, P75 e P90 por etapa.
- O sistema deve exibir taxa de estouro de SLA por etapa e por vendedor.

### RF07. Dashboard de perdas

- O sistema deve exibir quantidade e distribuicao de perdas por motivo, etapa, vendedor e origem.
- O sistema deve exibir tempo ate perda.
- O sistema deve destacar perdas sem motivo estruturado.

### RF08. Dashboard de vendedores

- O sistema deve exibir resultado por vendedor com visao de carteira, conversao, perda, reunioes e SLA.
- O sistema deve permitir comparar vendedor contra media da equipe.

### RF09. Dashboard de origem/lista/campanha

- O sistema deve exibir volume, conversao, velocidade e qualidade por `lista_origem`, `utm_source`, `utm_campaign` e `produto`.

### RF10. Dashboard de reunioes

- O sistema deve exibir reunioes marcadas no periodo.
- O sistema deve exibir reunioes por vendedor e por origem.
- O sistema deve mostrar, no minimo, deals com reuniao agendada e atraso sem reuniao.

### RF11. Drill-down operacional

- O sistema deve permitir sair do KPI para uma tabela detalhada com os deals que compoem o numero.
- O sistema deve permitir filtros por etapa, status, vendedor, origem, lista, produto e periodo.

### RF12. Relatorio dinamico

- O sistema deve gerar uma visao tipo relatorio com os principais highlights do periodo.
- O sistema deve destacar automaticamente variacoes relevantes, gargalos e outliers.

### RF13. Dicionario e confiabilidade

- O sistema deve documentar definicoes de metricas e formulas diretamente na interface ou em ajuda contextual.

## 15. Requisitos Nao Funcionais

- RNF01: A aplicacao deve ser independente do n8n em execucao e deploy.
- RNF02: Deve suportar crescimento para multi-origem sem refatoracao estrutural maior.
- RNF03: Deve ter tempo de resposta adequado para filtros comuns de 30 a 90 dias.
- RNF04: Deve ter observabilidade de sincronizacao, falhas e frescor dos dados.
- RNF05: Deve proteger PII e limitar exposicao desnecessaria na interface e nos logs.
- RNF06: Deve permitir deploy futuro em ambiente containerizado.
- RNF07: Deve ser resiliente a falhas parciais de sincronizacao.
- RNF08: Deve manter definicoes de metricas versionadas.

## 16. Proposta de Solucao

### 16.1 Arquitetura de alto nivel

- Backend API: FastAPI.
- Worker de sincronizacao: processo Python separado, agendado.
- Banco de dados: PostgreSQL.
- Frontend: aplicacao React/Next.js.
- Visualizacao: biblioteca de graficos com bom suporte a interacao e responsividade.
- Agendamento: scheduler da propria stack ou job externo de infra.

### 16.2 Por que esta abordagem

- Python atende bem ingestao, transformacao e camada analitica.
- React/Next.js atende melhor a necessidade de interface bonita, flexivel e escalavel do que dashboards Python prontos.
- Postgres atende o MVP e suporta agregacoes, visoes materializadas e evolucao gradual.

### 16.3 Recomendacao explicita de produto

Nao usar Streamlit ou Dash como interface final do produto se o objetivo for uma interface mais refinada, performatica e preparada para crescimento.

## 17. Modelo de Dados Recomendado

### 17.1 Camada bruta

- `raw_clint_deals`
- `raw_clint_users`
- `raw_clint_origins`
- `raw_clint_fields_catalog`
- `raw_sync_runs`

### 17.2 Camada tratada

- `dim_origin`
- `dim_stage`
- `dim_seller`
- `dim_product`
- `dim_source`
- `dim_contact_segment`

### 17.3 Fatos analiticos

- `fact_deal_current`
- `fact_deal_snapshot`
- `fact_stage_transition`
- `fact_deal_outcome`
- `fact_meeting`
- `fact_daily_sla`
- `fact_daily_conversion`

### 17.4 Agregados de desempenho

- `agg_stage_day`
- `agg_seller_day`
- `agg_origin_day`
- `agg_loss_reason_day`

## 18. Regras de Calculo das Metricas

### 18.1 Principio geral

Cada metrica deve ter formula, granularidade, filtro base e interpretacao documentados.

### 18.2 Metricas principais

- Leads por etapa:
  - contagem de deals pela etapa atual no recorte selecionado.
- Conversao entre etapas:
  - deals que avancaram de A para B dividido pelos deals elegiveis em A no mesmo criterio.
- Conversao total:
  - deals ganhos dividido pelos deals criados no cohort ou periodo definido.
- Tempo atual em etapa:
  - `agora - updated_stage_at`, com fallback para `created_at` quando necessario.
- Tempo real de passagem entre etapas:
  - `entered_at(stage B) - entered_at(stage A)`.
- SLA breach rate:
  - deals fora do SLA dividido pelos deals elegiveis para aquela regra.
- Reunioes marcadas:
  - numero de reunioes registradas, ou, na ausencia disso, deals com atributo de reuniao valido no recorte.
- Tempo ate reuniao:
  - data da primeira reuniao menos data de criacao do deal.
- Tempo ate perda:
  - data de perda menos data de criacao do deal.

### 18.3 Regra importante de semantica

O produto deve separar claramente:

- `tempo atual em etapa` para operacao;
- `tempo de passagem entre etapas` para analise historica.

Misturar as duas leituras no mesmo KPI criaria erro de interpretacao.

## 19. Tecnicas Analiticas e Estatisticas

- Mediana como metrica principal de tempo.
- P75 e P90 para visibilidade de cauda e gargalo.
- Media como metrica secundaria apenas para leitura complementar.
- Coortes por `data_importacao` e/ou `created_at`.
- Pareto de motivos de perda.
- Comparacao periodo atual vs periodo anterior.
- Baseline movel para detectar piora ou anomalia.
- Benchmark vendedor vs equipe.
- Analise de sobrevivencia por etapa em fase futura, se a base historica suportar.

## 20. Mecanismo de Ingestao

### 20.1 Dados minimos a sincronizar

- Deals `OPEN`, `WON` e `LOST`.
- Users.
- Origins e stages.
- Catalogo de campos da conta.

### 20.2 Frequencia recomendada

- Sincronizacao operacional: a cada 15, 30 ou 60 minutos.
- Agregacao diaria: fechamento de metricas 1 vez ao dia.
- Backfill inicial: maior janela historica que a API permitir.

### 20.3 Observacao critica

Se a API nao expuser historico de stage, o sistema precisara inferir transicoes por comparacao de snapshots. Neste caso, sincronizacao diaria nao e suficiente para medir com precisao boa tempos curtos de passagem. A recomendacao e sincronizacao subdiaria.

## 21. Requisitos de UX e Interface

- Filtros globais fixos no topo.
- Feedback visual claro de ultima atualizacao da base.
- Navegacao simples entre visao executiva, funil, SLA, vendedores, perdas e reunioes.
- Drill-down consistente em todas as visoes.
- Responsividade para desktop e tablet; mobile em modo consulta reduzida.
- Visualizacao clara, sem poluicao e com hierarquia forte de informacao.

## 22. Indicadores Prioritarios do MVP

- Quantidade de leads por etapa.
- Taxa de conversao entre etapas.
- Conversao total por origem/lista.
- Tempo mediano em etapa.
- P75 e P90 por etapa.
- Taxa de atraso SLA por etapa.
- Resultado por vendedor.
- Motivos de perda.
- Quantidade de reunioes marcadas.
- Tempo ate reuniao.

## 23. Riscos

- R1: inexistencia de historico de transicao na API.
- R2: motivo de perda nao estruturado ou inconsistente.
- R3: campo de reunioes nao padronizado na conta.
- R4: definicao de SLA incompleta para varias etapas.
- R5: crescimento de escopo para multi-origem antes da base do MVP estabilizar.
- R6: interpretacoes divergentes de metricas entre areas.

## 24. Mitigacoes

- M1: projetar desde o inicio um modelo que suporte snapshots e inferencia de transicoes.
- M2: formalizar um dicionario de metricas antes do build do frontend.
- M3: criar validacoes de qualidade de dados e buckets `nao informado`.
- M4: padronizar taxonomia de motivos de perda com dono de negocio.
- M5: manter flags de ativacao por modulo e por origem.

## 25. Decisoes de Produto a Fechar Antes da Implementacao

- Definir todos os SLAs por transicao.
- Definir horas corridas vs horas uteis.
- Confirmar mono-origem ou multi-origem no MVP.
- Confirmar campo oficial de `motivo_perda`.
- Confirmar campo oficial de contagem de reunioes.
- Confirmar frequencia minima aceitavel de sincronizacao.
- Confirmar politica de acesso por perfil.

## 26. Roadmap Proposto

### Fase 0. Descoberta e contrato de dados

- Validar todos os campos na conta Clint.
- Confirmar lacunas de `motivo_perda` e reunioes.
- Confirmar estrategia de historico de transicao.
- Fechar formulas das metricas.

### Fase 1. Fundacao de dados

- Construir conector e sincronizacao recorrente.
- Persistir camada bruta e tratada.
- Publicar primeiras tabelas analiticas.
- Implementar checks de qualidade e frescor.

### Fase 2. MVP do dashboard

- Entregar visao executiva.
- Entregar funil.
- Entregar SLA.
- Entregar vendedores.
- Entregar origens/listas.
- Entregar perdas e reunioes, se a base estiver estruturada.

### Fase 3. Insights e operacao assistida

- Adicionar relatorio automatico.
- Adicionar alertas de anomalia.
- Adicionar comparativos inteligentes por coorte e benchmark.

## 27. Criterios de Aceite do MVP

- A aplicacao roda fora do n8n.
- Existe sincronizacao automatica com a Clint e base propria persistida.
- O dashboard mostra, no minimo, volume por etapa, conversao, SLA e resultado por vendedor.
- O usuario consegue filtrar por periodo, origem/lista, etapa e vendedor.
- O sistema informa frescor dos dados.
- Existe pelo menos um drill-down detalhado por KPI principal.
- As formulas das metricas estao documentadas.

## 28. Instrumentacao e Telemetria do Produto

- Log de runs de sincronizacao.
- Alertas de falha de sync.
- Tempo de resposta dos endpoints analiticos.
- Uso por modulo do dashboard.
- Cliques em drill-downs e filtros.
- Frescor dos dados exibido ao usuario.

## 29. Open Questions

- Existe endpoint oficial de historico de alteracao de stage por deal?
- Existe `motivo_perda` como custom field estruturado ou o dado esta em nota/texto livre?
- A quantidade de reunioes vem de campo dedicado ou apenas de `latest_meeting_datetime`?
- O valor do deal (`value`) e confiavel e consistente para comparativos de resultado?
- O MVP deve nascer apenas para `Perpetuo Webinario` ou com arquitetura ativa para outras origins?

## 30. Recomendacao Final de Produto

O MVP deve ser construido como um produto de analise comercial em duas camadas:

- uma camada operacional, focada em backlog, SLA e carteira atual;
- uma camada gerencial, focada em conversao, perda, origem, vendedor e tendencias.

A maior prioridade tecnica nao e o frontend em si, mas sim garantir uma base historica correta e sem ambiguidade de definicao. Sem isso, o dashboard pode ficar bonito, mas gerencialmente fraco.
