# Mapa de Telas - Dashboard Comercial Clint

Status: Planejamento de UX e navegacao
Data: 2026-03-07
Dependencia: este documento pressupoe o PRD em `dashboard-comercial-clint/PRD.md`

## 1. Objetivo do Mapa

Definir a arquitetura de informacao, as telas principais, a hierarquia de navegacao e os componentes essenciais do dashboard comercial Clint.

## 2. Principios de Interface

- Priorizar leitura executiva rapida sem sacrificar drill-down operacional.
- Manter filtros globais persistentes entre telas.
- Exibir sempre o frescor do dado.
- Separar visualmente operacao atual de historico e tendencia.
- Reduzir ambiguidades com definicoes curtas de metricas e tooltips.

## 3. Estrutura Global de Navegacao

### Navegacao principal

- Visao Geral
- Funil
- SLA
- Vendedores
- Origens e Listas
- Perdas
- Reunioes
- Deals
- Configuracoes

### Filtros globais fixos

- Periodo
- Origem
- Lista origem
- Produto
- Vendedor
- Status
- Etapa
- UTM Source
- UTM Campaign

### Barra superior fixa

- Titulo da tela
- Ultima sincronizacao
- Estado do sync
- Exportar dados
- Salvar visualizacao

## 4. Tela 1 - Visao Geral

### Objetivo

Dar uma leitura executiva em menos de 30 segundos.

### Blocos

- KPIs do topo:
  - leads criados
  - deals abertos
  - deals ganhos
  - deals perdidos
  - taxa de conversao total
  - taxa de SLA estourado
  - reunioes marcadas
- Cards de tendencia:
  - variacao vs periodo anterior
- Grafico principal:
  - funil resumido
- Grafico secundario:
  - linha de tendencia diaria de criados, ganhos e perdas
- Painel de alertas:
  - etapas com maior atraso
  - vendedores com maior backlog
  - listas com pior conversao
- Bloco de highlights automatizados:
  - 3 a 5 insights de texto curto

### Acoes de drill-down

- clique em KPI abre tabela filtrada
- clique em etapa abre tela de funil ja filtrada
- clique em alerta abre detalhe correspondente

## 5. Tela 2 - Funil

### Objetivo

Analisar volume, passagem e conversao entre etapas.

### Blocos

- Funil principal por etapa
- Tabela lateral com:
  - volume
  - conversao para proxima etapa
  - conversao acumulada
  - tempo mediano na etapa
  - P75 da etapa
- Grafico de cohort por semana de entrada
- Quebra por segmento:
  - origem
  - lista
  - produto
  - vendedor
- Toggle de leitura:
  - funil atual
  - funil historico
  - cohort de entrada

### Acoes de drill-down

- clicar em etapa abre deals daquela etapa
- clicar em segmento refaz todos os blocos da tela

## 6. Tela 3 - SLA

### Objetivo

Monitorar risco operacional e gargalos de permanencia.

### Blocos

- KPI row:
  - deals fora do SLA
  - taxa de estouro total
  - etapa mais critica
  - vendedor com maior atraso medio
- Heatmap:
  - etapa x vendedor
- Grafico de distribuicao:
  - boxplot ou barras por faixa de aging
- Tabela de SLA por etapa:
  - meta
  - mediana atual
  - P75
  - P90
  - % fora do SLA
- Lista de deals criticos:
  - top atrasos do periodo atual

### Acoes de drill-down

- clicar em etapa leva ao detalhe de deals fora do SLA
- clicar em vendedor filtra a tela

## 7. Tela 4 - Vendedores

### Objetivo

Comparar resultado individual e carga operacional.

### Blocos

- Ranking de vendedores por meta selecionavel:
  - ganhos
  - conversao
  - reunioes
  - SLA
- Scorecard por vendedor:
  - leads recebidos
  - open
  - won
  - lost
  - win rate
  - loss rate
  - reunioes
  - taxa de atraso SLA
  - tempo mediano ate primeiro avanco
- Grafico radar ou barras comparativas
- Timeline de resultado por vendedor
- Mix de perdas por vendedor

### Drill-down

- clique no vendedor abre subpagina detalhada

## 8. Tela 5 - Detalhe do Vendedor

### Objetivo

Dar uma leitura 360 graus da carteira de um vendedor.

### Blocos

- Header com nome, carteira atual e status de desempenho
- KPIs individuais
- Funil individual
- SLA individual
- Reunioes marcadas
- Perdas por motivo
- Carteira atual por etapa
- Lista detalhada de deals

## 9. Tela 6 - Origens e Listas

### Objetivo

Responder quais canais, listas e campanhas geram volume com qualidade.

### Blocos

- Ranking de `lista_origem`
- Tabela comparativa com:
  - leads
  - reunioes
  - conversao por etapa
  - ganho
  - perda
  - tempo mediano por etapa
  - taxa de SLA estourado
- Grafico bolha:
  - volume x conversao x atraso
- Quebras por:
  - `utm_source`
  - `utm_campaign`
  - `produto`

### Drill-down

- clique em lista ou campanha abre deals filtrados e cohort correspondente

## 10. Tela 7 - Perdas

### Objetivo

Entender por que os deals estao sendo perdidos e onde agir.

### Blocos

- KPI row:
  - perdas totais
  - % com motivo informado
  - principal motivo
  - etapa com maior perda
- Grafico Pareto de motivos de perda
- Matriz:
  - motivo x etapa
- Quebras por:
  - vendedor
  - lista
  - produto
  - origem
- Grafico de tempo ate perda
- Lista de perdas recentes

### Observacao de UX

Se o dado de motivo estiver incompleto, mostrar banner de qualidade indicando cobertura do preenchimento.

## 11. Tela 8 - Reunioes

### Objetivo

Monitorar volume e influencia das reunioes na progressao do funil.

### Blocos

- KPI row:
  - reunioes marcadas
  - deals com reuniao futura
  - taxa lead -> reuniao
  - tempo mediano ate reuniao
- Serie temporal de reunioes
- Ranking por vendedor
- Comparativo por lista/origem
- Distribuicao de deals sem reuniao apos X dias
- Se existir contagem oficial:
  - media de reunioes por deal

### Observacao de UX

Se so existir `latest_meeting_datetime`, rotular a leitura como `deals com reuniao registrada`, nao como contagem total de reunioes.

## 12. Tela 9 - Deals

### Objetivo

Servir como camada de auditoria e drill-down universal.

### Estrutura

- tabela com busca e filtros
- colunas configuraveis
- exportacao CSV
- ordenacao
- filtros salvos

### Colunas iniciais sugeridas

- deal id
- nome do deal
- contato
- etapa atual
- status
- vendedor
- origem
- lista origem
- produto
- created_at
- updated_stage_at
- aging atual
- SLA status
- ultima reuniao
- motivo de perda

## 13. Tela 10 - Configuracoes

### Objetivo

Dar visibilidade administrativa das regras e do estado da base.

### Blocos

- estado do sync
- historico de execucoes de sincronizacao
- origens sincronizadas
- mapeamento de etapas
- regras de SLA por transicao
- cobertura de campos criticos:
  - motivo de perda
  - reunioes
  - lista origem
  - vendedor responsavel
- glossario de metricas

## 14. Componentes Reutilizaveis

- card KPI com comparativo
- filtro multi-select
- seletor de periodo com presets
- tabela com drill-down
- badge de qualidade de dados
- badge de frescor de sync
- tooltip de formula
- painel de insight automatico
- empty state com explicacao do motivo

## 15. Fluxos Principais do Usuario

### Fluxo 1. Lider comercial

- entra em `Visao Geral`
- identifica alerta de gargalo
- navega para `SLA`
- filtra etapa e vendedor
- abre `Deals` para acao operacional

### Fluxo 2. RevOps

- entra em `Origens e Listas`
- compara listas e campanhas
- percebe piora de conversao
- abre `Funil`
- cruza com `Perdas`

### Fluxo 3. Gestor de time

- entra em `Vendedores`
- compara resultado individual
- abre `Detalhe do Vendedor`
- observa perdas e backlog

## 16. Regras de Drill-Down

- Todo KPI principal deve abrir um detalhe filtrado.
- Todo grafico principal deve permitir clique em segmento.
- A tabela `Deals` deve ser o destino padrao do drill-down operacional.
- O usuario nunca deve perder os filtros globais ao navegar.

## 17. Regras de Responsividade

- Desktop: experiencia completa, com grid de cards e graficos em duas ou tres colunas.
- Tablet: empilhamento parcial dos blocos, mantendo filtros no topo.
- Mobile: leitura reduzida, focada em KPIs, listas resumidas e tabela simplificada.

## 18. Recomendacao de Prioridade de Telas

### Prioridade P0

- Visao Geral
- Funil
- SLA
- Vendedores
- Deals

### Prioridade P1

- Origens e Listas
- Perdas
- Reunioes

### Prioridade P2

- Configuracoes
- Insights automatizados mais avancados

## 19. Riscos de UX

- Excesso de filtros e sobrecarga cognitiva.
- Graficos bonitos, mas sem semantica clara.
- Mistura de operacao atual com historico fechado.
- Falta de contexto quando o dado estiver incompleto.

## 20. Recomendacao Final de Navegacao

A melhor estrutura para o MVP e:

- uma home executiva (`Visao Geral`),
- modulos funcionais separados (`Funil`, `SLA`, `Vendedores`, `Origens e Listas`, `Perdas`, `Reunioes`),
- uma camada unica de auditoria (`Deals`),
- uma camada administrativa (`Configuracoes`).

Essa organizacao reduz ambiguidade, facilita adocao e deixa o produto pronto para crescer sem refazer a navegacao central.
