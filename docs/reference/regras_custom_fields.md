# Regras de Custom Fields - Clint

Este documento define o mapeamento dos campos personalizados que devem ser configurados na Clint para a correta ingestão dos leads via planilha.

## 1. Entidade: CONTACT (Contato)

Estes campos representam o perfil permanente do usuário. Devem ser criados como campos de texto ou seleção conforme a necessidade na interface da Clint.

| Identificador (API) | Label / Pergunta (Planilha) | Tipo sugerido |
| :--- | :--- | :--- |
| `idade` | "Idade" | TEXT |
| `profissao` | "Você é bacharel, estudante ou advogado ?" | SELECT / TEXT |
| `tempo_de_estudo` | "Há quanto tempo estuda pra Concursos?" | TEXT |
| `foi_aluno_oab` | "É ou já foi aluno VDE OAB?" | SELECT (Sim/Não) |
| `e_aluno_concursos` | "É aluno VDE Concursos - Carreiras Jurídicas?" | SELECT (Sim/Não) |
| `carreira_pretendida` | "Qual Carreira Jurídica pretende seguir?" | SELECT / TEXT |
| `horas_por_dia` | "Quantas horas livres por dia você tem em média para estudar?" | TEXT |
| `renda_familiar` | "Qual a sua renda familiar?" | TEXT |
| `features_desejadas` | "O que você mais preza em um Curso Preparatório para o ENAM?" | TEXT |
| `maior_dificuldade` | "Qual a sua maior dificuldade na sua preparação para o ENAM?" | TEXT |

---

## 2. Entidade: DEAL (Negócio)

Utilize estes campos para informações específicas da oportunidade atual/venda.

| Identificador (API) | Descrição |
| :--- | :--- |
| `utm_source` | Origem do tráfego (ex: facebook, google) |
| `utm_medium` | Meio do tráfego (ex: cpc, email) |
| `utm_campaign` | Nome da campanha |
| `utm_term` | Termo/Palavra-chave |
| `utm_content` | Conteúdo do anúncio |
| `lista_origem` | Lista de origem (deve pegar diretamente do front-end) |
| `data_importacao` | Data/Hora que o lead foi injetado pelo sistema |
| `produto` | Produto desejado naquela negociação específica |
| `value` | Valor do produto desejado |

> **Nota:** Recomenda-se colocar UTMs e informações da "viagem" atual do lead no **Deal** para rastrear a origem de cada venda individualmente sem sobrescrever o histórico do contato.
