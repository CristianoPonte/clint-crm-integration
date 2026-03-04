# Clint API Mappings

Este arquivo contém todos os IDs necessários da API da Clint e documenta o comportamento técnico descoberto durante a implementação.

## 1. Custom Fields (Campos Personalizados)
Usados ao criar ou atualizar um contato em `fields`. A chave JSON deve ser o nome da variável (ex: `produto`, `carreira_pretendida`).

### Entidade: DEAL
- **`produto`** (MULTIPLE_SELECT) - Label: *Produto*
- **`utm_term`** (TEXT) - Label: *utm_term*
- **`utm_medium`** (TEXT) - Label: *utm_medium*
- **`utm_source`** (TEXT) - Label: *utm_source*
- **`utm_content`** (TEXT) - Label: *utm_content*
- **`utm_campaign`** (TEXT) - Label: *utm_campaign*
- **`lista_origem`** (TEXT) - Label: *Lista Origem*
- **`data_importacao`** (TEXT) - Label: *Data Importação*

### Entidade: CONTACT
- **`idade`** (TEXT) - Label: *Idade*
- **`notes`** (RICH_TEXT) - Label: *Notas do contato*
- **`historico`** (SELECT) - Label: *Histórico*
- **`profissao`** (TEXT) - Label: *Profissão*
- **`turma_da_oab`** (TEXT) - Label: *Turma da OAB de Interesse*
- **`foi_aluno_oab`** (TEXT) - Label: *Foi Aluno OAB*
- **`horas_por_dia`** (TEXT) - Label: *Horas por Dia*
- **`renda_familiar`** (TEXT) - Label: *Renda Familiar*
- **`estuda_para_oab`** (TEXT) - Label: *Estuda para OAB?*
- **`tempo_de_estudo`** (TEXT) - Label: *Tempo de Estudo*
- **`e_aluno_concursos`** (TEXT) - Label: *É Aluno Concursos*
- **`maior_dificuldade`** (TEXT) - Label: *Maior Dificuldade*
- **`features_desejadas`** (TEXT) - Label: *Features Desejadas*
- **`carreira_pretendida`** (SELECT) - Label: *Carreira Pretendida*
- **`disciplina_segunda_f`** (TEXT) - Label: *Disciplina Segunda Fase*
- **`produto_de_interesse`** (SELECT) - Label: *Produto de Interesse*
- **`quantas_horas_por_di`** (TEXT) - Label: *Quantas horas por dia você estuda, em média?*
- **`quantas_vezes_voce_j`** (TEXT) - Label: *Quantas vezes você já fez a prova da OAB?*
- **`sentimento_de_aprova`** (TEXT) - Label: *Sentimento de aprovação atual*


### Entidade: ORGANIZATION

## 2. Origens e Funis (Stages)
Ao criar um Deal, **origin_id** é obrigatório. Também é preciso o **stage_id** para o Deal cair na fase do kanban (ex: coluna 'Base').

### Origem: Compras aprovadas (Grupo: VDE 180D - OAB 1F)
- **Origin ID:** `fe98c4b7-3b53-4da1-89c8-6ad661ec384b`
- **Stages (Fases do Funil):**
  - `7208d6cd-992d-407a-b6ac-8dd548b90eb2` - Base (Tipo: BASE)
  - `3eb1ffdf-6e92-4c67-9a5b-661adc18c8ea` - Onboarding (Tipo: CUSTOM)
  - `eed934d3-819e-4251-bf0e-558e0308b097` - On going (Tipo: CUSTOM)
  - `aacc9301-95af-4e24-b1b4-d89823fe94bb` - Sucesso (Tipo: CLOSING)

### Origem: Alunos VDE Aprovados na OAB (Grupo: CJ - Ciclo Prioritário)
- **Origin ID:** `fbbe8b34-36ff-4970-b952-80759eed15e8`
- **Stages (Fases do Funil):**
  - `d6c2cbf5-7576-43c9-a7b3-148ae5aae11e` - Base (Tipo: BASE)
  - `ab9f1405-b12f-4160-9c67-4b0f8e249ac2` - Prospecção (Tipo: CUSTOM)
  - `22a9ef7f-5408-4438-b6a2-3119096ca9d0` - Follow UP (Tipo: CUSTOM)
  - `1a5d4de4-2ea3-4a11-88db-732e4211991b` - Antes de Encerrar (Tipo: CUSTOM)
  - `f9a2752f-504b-429c-81c8-9b8a022c72e9` - Encerramento (Tipo: CUSTOM)
  - `6a5c618c-0b1e-430f-9a40-b6923eb4d7ce` - Conexão (Tipo: CUSTOM)
  - `6841cc19-4002-4491-861e-41bbf8935368` - Aguardando Compra (Tipo: CUSTOM)
  - `02b8da1a-abf0-49bf-b064-381093a12526` - Fechado (Tipo: CLOSING)

### Origem: Lista Alunos OAB 43 (Grupo: OAB - Primeira Fase)
- **Origin ID:** `f8e87bcb-a070-48e3-9c65-de0fff5d58b7`
- **Stages (Fases do Funil):**
  - `47f6dffa-ea8e-4b0c-b1fe-fb44c562dd49` - Base (Tipo: BASE)
  - `dc0406ea-a3bf-4e2e-855d-b54b49c649c4` - Prospecção (Tipo: CUSTOM)
  - `45745ec6-5028-4b7c-86b4-87655ee7f40d` - Conexão (Tipo: CUSTOM)
  - `43a27d4f-23fa-4072-aa76-84148042863f` - Aguardando Decisão (Tipo: CUSTOM)
  - `1ad390ae-3389-4dc9-a410-889d066b1a20` - Aguardando Pagamento (Tipo: CUSTOM)
  - `acd107b7-dc1a-40b9-acd3-0db25a21483a` - Fechado (Tipo: CLOSING)

### Origem: Reembolso/Chargeback (Grupo: VDE 60D - OAB 1F)
- **Origin ID:** `f8e07677-05ad-4e7d-8a14-8787033ad606`
- **Stages (Fases do Funil):**
  - `70df63ad-6a5c-44ec-999d-b3cb79926161` - Base (Tipo: BASE)
  - `0251a502-e315-4ef5-9bd5-0cc5d50c2203` - Sondagem (Tipo: CUSTOM)
  - `b4616536-b97c-40e0-b127-dacf85a99f05` - Em contato (Tipo: CUSTOM)
  - `d5b4e33b-05fc-4d29-85e3-788238697f66` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex em atraso (Grupo: OAB - Primeira Fase)
- **Origin ID:** `f8c4477a-3ad9-4699-9c49-80bb0efa56c0`
- **Stages (Fases do Funil):**
  - `0032e6b3-c947-483a-8346-5ba07fe5e8fe` - Base (Tipo: BASE)
  - `a9c7ade2-7833-4e90-a49e-3095af1e94fd` - Sondagem (Tipo: CUSTOM)
  - `3ece0b40-079b-4d27-8123-420cea9d7fdc` - Em contato (Tipo: CUSTOM)
  - `47b79c1c-38a5-4ff5-a6a5-45d87248615f` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex em atraso (Grupo: VDE 180D - OAB 1F)
- **Origin ID:** `f729e970-fbd4-452c-a41f-7bbafbad9733`
- **Stages (Fases do Funil):**
  - `0986a659-d556-4181-aca9-410d2ab56a7e` - Base (Tipo: BASE)
  - `d86fc00c-14ad-439f-b9d0-52d0cca7fb79` - Sondagem (Tipo: CUSTOM)
  - `e7eb49ac-6308-4d0c-86ee-8728ad4c00f9` - Em contato (Tipo: CUSTOM)
  - `4669cb93-1282-4c22-bb40-df961fdbef4c` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex em atraso (Grupo: Hotmart - 6979776)
- **Origin ID:** `f4d41320-3793-40ae-a132-d85de6069bf1`
- **Stages (Fases do Funil):**
  - `157a7539-1751-4f60-b3b2-bcd7692c19a5` - Base (Tipo: BASE)
  - `f727537a-33af-4123-8b08-7f3887e5b263` - Sondagem (Tipo: CUSTOM)
  - `0f65642f-37c0-4d9d-a4c2-472fd298f0b5` - Em contato (Tipo: CUSTOM)
  - `3c3831ea-1677-452b-aa02-5f4fa786ada0` - Fechado (Tipo: CLOSING)

### Origem: Leads Interessados na OAB 44 (Grupo: OAB - Primeira Fase)
- **Origin ID:** `f2e7e701-a3a2-4b24-94b2-95e70a74bd04`
- **Stages (Fases do Funil):**
  - `35381bab-290b-41d8-9343-e812c9223040` - Base (Tipo: BASE)
  - `09b16a1e-05f3-477b-af44-b37ef76a350c` - Prospecção (Tipo: CUSTOM)
  - `4db72bc6-fcdd-4b7f-acb4-6bff6ef77f3f` - Conexão (Tipo: CUSTOM)
  - `574726a3-a281-41a0-9ccc-cd607f615a20` - Aguardando Decisão (Tipo: CUSTOM)
  - `c05769a1-7984-41de-b90d-b092aee954ab` - Aguardando Compra (Tipo: CUSTOM)
  - `26bbaa67-1476-4259-8e73-504dc961f40f` - Fechado (Tipo: CLOSING)

### Origem: Lista Geral (Grupo: Hotmart - 6384818)
- **Origin ID:** `efb71de9-89a3-42e5-912f-b00136db38bf`
- **Stages (Fases do Funil):**
  - `4c40d653-ecae-492e-b697-28ccf850d3e6` - Base (Tipo: BASE)
  - `d1b173f3-5a89-4190-a7e2-666476a6db10` - Prospecção (Tipo: CUSTOM)
  - `57e0eb16-8962-4b24-ac81-b0794a455592` - Conexão (Tipo: CUSTOM)
  - `ad973f79-044b-43fb-af51-b530e7f8d2e8` - Aguardando compra (Tipo: CUSTOM)
  - `340319e4-2640-483c-a374-b49ce0610e81` - Fechado (Tipo: CLOSING)

### Origem: Reprovados_Pós recurso 2º fase (Grupo: OAB - Segunda Fase)
- **Origin ID:** `ed48e104-a718-4c53-a9af-0eba8a0841c9`
- **Stages (Fases do Funil):**
  - `55b92b71-e071-4623-b2b8-40836cb6658f` - Base (Tipo: BASE)
  - `f26b1236-099a-416c-8e70-7fdda85f61ac` - Prospecção (Tipo: CUSTOM)
  - `36ed259b-39a4-4a83-9b05-8ec4c32b099d` - Conexão (Tipo: CUSTOM)
  - `356387de-51d0-45f8-807e-6d0ca8b614c8` - Aguardando Decisão (Tipo: CUSTOM)
  - `675a5073-96af-4c06-8858-2d32a8554090` - Aguardando Pagamento (Tipo: CUSTOM)
  - `fa58f3d6-4024-4420-999f-2b12f21b312f` - Fechado (Tipo: CLOSING)

### Origem: Compras em aberto (Grupo: OAB - Primeira Fase)
- **Origin ID:** `e7443437-476e-4730-99aa-fe39be51e4c9`
- **Stages (Fases do Funil):**
  - `f81adfee-107c-4cc0-a326-e2ec247edb8a` - Base (Tipo: BASE)
  - `ae840d86-cd21-463b-8c1e-8ee995646e57` - Prospecção (Tipo: CUSTOM)
  - `3fe83dfd-e4e2-43d7-b56a-2d72e4cad8f7` - Conexão (Tipo: CUSTOM)
  - `19bdc082-201c-4bc3-b3c5-931f2fa67c33` - Aguardando compra (Tipo: CUSTOM)
  - `1133043a-2a5d-4a64-8d88-6e22f1dc14e1` - Fechado (Tipo: CLOSING)

### Origem: VDE 120D - OAB 47 (Grupo: OAB - Primeira Fase)
- **Origin ID:** `e6e7c30c-0434-461b-95fc-67f77ea17792`
- **Stages (Fases do Funil):**
  - `cb9f501d-bedd-4f24-9bca-08c80287b494` - Base (Tipo: BASE)
  - `9a75da76-3dce-4720-a793-c1cbaad35e31` - Prospecção (Tipo: CUSTOM)
  - `f80bb916-f0b8-4ccc-911e-48618faf064d` - Agendadas (Tipo: CUSTOM)
  - `33e767e7-3ab8-4542-9536-65229be868c6` - Follow Up (Tipo: CUSTOM)
  - `187f7396-224e-47de-b758-f52f45df88d0` - Antes de Encerrar (Tipo: CUSTOM)
  - `0cd0546c-6428-4eaa-a83f-48c7bc144461` - Encerramento (Tipo: CUSTOM)
  - `f8f4846a-1c53-4c8f-b896-71518e97e291` - Conexão (Tipo: CUSTOM)
  - `715f902d-dd2b-4018-a21c-ec8e146b174d` - Aguardando Compra (Tipo: CUSTOM)
  - `e860387b-5c2d-4412-bd99-cc1fb411940c` - Fechado (Tipo: CLOSING)

### Origem: Cartão recusado (Grupo: OAB - Segunda Fase)
- **Origin ID:** `e44c4e20-6812-4cbe-ba39-4ca768645b3c`
- **Stages (Fases do Funil):**
  - `2904766d-f72e-440d-bfe6-080f628a8b56` - Base (Tipo: BASE)
  - `a06353ba-24c4-443d-a242-8ca26bfa5768` - Prospecção (Tipo: CUSTOM)
  - `22e04688-d469-4998-b0f1-4783a7993bde` - Conexão (Tipo: CUSTOM)
  - `936626c9-100c-4076-8cc7-d0db8c962346` - Aguardando compra (Tipo: CUSTOM)
  - `7e28db38-796a-4769-b647-8313e7af1a72` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex ativas (Grupo: Hotmart - 6384818)
- **Origin ID:** `e2790107-a4ff-4c06-a77b-d6dc5434d169`
- **Stages (Fases do Funil):**
  - `9a24c574-8788-4284-afc3-c6a3c64f35af` - Base (Tipo: BASE)
  - `495366b7-8416-4a26-ab8b-526788d02f45` - On going (Tipo: CUSTOM)
  - `80f6554e-049d-4723-b5b5-4d829415312e` - Sucesso (Tipo: CLOSING)

### Origem: Abandono de carrinho (Grupo: CJ - Ciclo Prioritário)
- **Origin ID:** `e20df957-7ef2-44ab-b055-dcebb8e0b0ca`
- **Stages (Fases do Funil):**
  - `d3595b58-f6e3-4fd3-b11c-fc9c0f08b1b7` - Base (Tipo: BASE)
  - `de2f1c3b-bda3-4562-bd1a-a1c7d283c5c2` - Prospecção (Tipo: CUSTOM)
  - `8991ba55-64cf-4596-93e7-001ef4edb102` - Follow UP (Tipo: CUSTOM)
  - `4d556b29-baf7-47f1-ada6-317ad49aa999` - Conexão (Tipo: CUSTOM)
  - `61cea4eb-8439-499c-bed4-c681f98de9ef` - Aguardando compra (Tipo: CUSTOM)
  - `982e1fd4-a280-40cb-9d6a-ba4e6987a8ef` - Fechado (Tipo: CLOSING)

### Origem: Compras em aberto (Grupo: CJ - Ciclo Prioritário)
- **Origin ID:** `e0bb933d-5f5f-4f58-8369-c0e18cc16bb4`
- **Stages (Fases do Funil):**
  - `99378d24-439c-4cbe-84f6-cab47cb6e16f` - Base (Tipo: BASE)
  - `73abfd02-ebe9-4290-9fcb-08e9601997ee` - Prospecção (Tipo: CUSTOM)
  - `aac2ae56-74e9-4cbd-bbe9-f797a2cd525e` - Conexão (Tipo: CUSTOM)
  - `012d10cd-aa62-4885-a415-45f83572345c` - Aguardando compra (Tipo: CUSTOM)
  - `cfadaa00-4564-4d3b-b42b-783cca74ef50` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex ativas (Grupo: ENAM - 90 Dias)
- **Origin ID:** `e05c69c7-6f68-413f-82ef-16fbf88c1d1f`
- **Stages (Fases do Funil):**
  - `554e2090-3a4f-4848-900d-67aa9d7bb17b` - Base (Tipo: BASE)
  - `7cd98699-ad2d-4ef8-b311-7cedb8a4651f` - On going (Tipo: CUSTOM)
  - `510cf944-0771-44ad-b6ac-23479b16d02b` - Sucesso (Tipo: CLOSING)

### Origem: Reembolso/Chargeback (Grupo: CJ - Ciclo Prioritário)
- **Origin ID:** `e0319da3-f88d-4856-a881-88f26c90df35`
- **Stages (Fases do Funil):**
  - `6bc64eb9-4110-4807-be3d-ccf21a4d3c9d` - Base (Tipo: BASE)
  - `e33b9437-ec6b-4ea8-82ac-2e8c90f5d246` - Sondagem (Tipo: CUSTOM)
  - `a7a5b1a6-dedf-42f3-8192-91aa685b5999` - Em contato (Tipo: CUSTOM)
  - `68d51016-fc45-4a2c-89a9-4da47486eddc` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex ativas (Grupo: ENAM - ANUAL)
- **Origin ID:** `e01453de-796d-4804-88c5-f26a02667d18`
- **Stages (Fases do Funil):**
  - `336fbee2-f802-404b-bec9-3a3124a70004` - Base (Tipo: BASE)
  - `04248a63-5de0-4314-8129-cbfd8dca28e4` - On going (Tipo: CUSTOM)
  - `59d3acfe-0b57-4ff4-b092-32b81546c43f` - Sucesso (Tipo: CLOSING)

### Origem: Compras aprovadas (Grupo: OAB - 1º Fase ANUAL)
- **Origin ID:** `dffc9e20-1b5a-49e2-b321-ceb6d6616c36`
- **Stages (Fases do Funil):**
  - `267d8e4c-be69-4e02-bb1a-7b32c563410a` - Base (Tipo: BASE)
  - `d480a2a7-6d2f-4148-b5cf-4ed8a74582ec` - Onboarding (Tipo: CUSTOM)
  - `d8e35ab3-10a2-4a63-ae88-2d6ff57f1f26` - On going (Tipo: CUSTOM)
  - `4c2b1e1c-04ef-46c1-b9a7-aaee07b5aa76` - Sucesso (Tipo: CLOSING)

### Origem: Compras em aberto (Grupo: ENAM - ANUAL)
- **Origin ID:** `ddfd9a06-649a-4ef4-bda6-c76dd3ac1fd5`
- **Stages (Fases do Funil):**
  - `806fc939-caa2-47af-893f-57a2ab9f6bdb` - Base (Tipo: BASE)
  - `2d793390-ca91-4313-a3d3-094902935f9a` - Prospecção (Tipo: CUSTOM)
  - `cff67f3e-bd20-4120-b141-b79023c7d630` - Conexão (Tipo: CUSTOM)
  - `7b689cbb-b098-47c4-89ee-21a494bb1e63` - Aguardando compra (Tipo: CUSTOM)
  - `65fd1f20-a304-41cf-b269-a80a7cde4134` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex ativas (Grupo: OAB - Primeira Fase)
- **Origin ID:** `dae97271-f1fc-4175-8f68-91150513c1af`
- **Stages (Fases do Funil):**
  - `a8b40cd1-66b0-444a-b81c-025c1e932462` - Base (Tipo: BASE)
  - `e0b313b8-2b37-4beb-a0fe-e288c13fccd8` - On going (Tipo: CUSTOM)
  - `f976ee89-4288-47bb-9749-029b46224288` - Sucesso (Tipo: CLOSING)

### Origem: Leads Quentes - 90 Dias (Grupo: OAB - Primeira Fase)
- **Origin ID:** `d836f358-1fce-4e4f-9024-628a3a835ce0`
- **Stages (Fases do Funil):**
  - `2e62b43f-d913-4932-9a7e-acee5b614ddd` - Base (Tipo: BASE)
  - `5fa335a9-0fbb-4357-a420-636910c0dfa0` - Prospecção (Tipo: CUSTOM)
  - `88f426d0-fd82-4fd0-b4b0-910eb77e71ea` - Material Gratuito (Tipo: CUSTOM)
  - `3821b209-0432-4c17-9f95-e8b47dc8dc08` - Inicio da Turma (Tipo: CUSTOM)
  - `e11685b8-4c49-4e5e-b064-c7f72155d119` - Pós Live (Tipo: CUSTOM)
  - `9e74f73d-3d50-4581-b517-534aefcd4e5d` - Conexão (Tipo: CUSTOM)
  - `00b888a4-0728-48ae-a2af-6471a277d4da` - Aguardando Pagamento (Tipo: CUSTOM)
  - `0bb6ebdd-84b9-4f46-a650-e91d57b421bd` - Encerramento (Tipo: CUSTOM)
  - `77d1f226-8ed5-4d63-8e21-cf9fca71d9f3` - Fechado (Tipo: CLOSING)

### Origem: Hotmart (Grupo: Comercial)
- **Origin ID:** `d57b0b34-7b36-4c72-babf-5196e5c35657`
- **Stages (Fases do Funil):**
  - `fc718ab5-fb87-45bd-b73c-8c440b777c03` - Base (Tipo: BASE)
  - `64923334-afee-4b9c-be9d-24d9de099c13` - Prospecção (Tipo: CUSTOM)
  - `4abda377-94f3-4f92-9e5a-0818f6ab9eae` - Conexão (Tipo: CUSTOM)
  - `fae45f79-4b23-409c-a7b8-c982c69d0620` - Aguardando compra (Tipo: CUSTOM)
  - `823e7739-a08d-474a-a5f1-12c094b21620` - Fechado (Tipo: CLOSING)

### Origem: Compras expiradas (Grupo: CJ - Ciclo Prioritário)
- **Origin ID:** `d035ff35-cfbf-471b-a2a5-eb2dad009f30`
- **Stages (Fases do Funil):**
  - `35c229a9-3905-40a8-b0b2-e336d43f51c2` - Base (Tipo: BASE)
  - `c2c24e80-5b76-4ba1-8687-5c0cc5675543` - Prospecção (Tipo: CUSTOM)
  - `67799102-3e97-41ec-bc3e-b5b67707ce41` - Conexão (Tipo: CUSTOM)
  - `2222dc1a-2fbe-4c82-a58f-94c515b8144d` - Aguardando compra (Tipo: CUSTOM)
  - `3420190b-4836-4410-8906-142102085971` - Fechado (Tipo: CLOSING)

### Origem: VDE 60D - OAB 46 (Grupo: OAB - Primeira Fase)
- **Origin ID:** `cf7e148e-01c1-44f7-92cb-ed6d69c52a97`
- **Stages (Fases do Funil):**
  - `7f5a9c88-2600-4c49-a155-9241a54a731d` - Base (Tipo: BASE)
  - `b9d34314-76c2-4f89-af79-2d1185d39519` - Agendamento (Tipo: CUSTOM)
  - `c737aa8f-aab8-4f25-895f-eecfde554062` - Leads Quentes (Tipo: CUSTOM)
  - `1ec51437-05a6-47cb-939b-000cf025a072` - Prospecção (Tipo: CUSTOM)
  - `f4e057d9-f90e-450b-be9c-fefdd50394f1` - Follow UP 1 (Tipo: CUSTOM)
  - `b4d99a0b-83aa-47be-991d-16180d3c1b58` - Follow UP 2 (Tipo: CUSTOM)
  - `9e3a9f13-7b45-41b9-9c10-7096d7d3b415` - Follow Up 3 (Tipo: CUSTOM)
  - `9bbb7e26-9bed-46ee-b8b9-3cffdb6810bd` - Encerramento (Tipo: CUSTOM)
  - `a2299fd9-cf9b-472e-8357-21d014ad3375` - Conexão (Tipo: CUSTOM)
  - `509523e3-701a-48c7-b9a5-d6d622d2c98f` - Aguardando Pagamento (Tipo: CUSTOM)
  - `ee9c33a9-3b4c-47ff-b3c9-c380d79172ee` - Fechado (Tipo: CLOSING)

### Origem: Compras expiradas (Grupo: Hotmart - 6979776)
- **Origin ID:** `ce814595-c214-475b-bf08-7062417b2bf6`
- **Stages (Fases do Funil):**
  - `d5d4d2f5-2c9d-4eed-9067-9fbe38cbb883` - Base (Tipo: BASE)
  - `1d6d65ae-aa9e-4594-b1ce-0ee179087364` - Prospecção (Tipo: CUSTOM)
  - `f87fa1dc-420d-4124-96de-b397080a53f1` - Conexão (Tipo: CUSTOM)
  - `93c41bb7-a20b-4045-a231-2681040df81e` - Aguardando compra (Tipo: CUSTOM)
  - `962b4696-08a9-4cc8-9be4-7384851d7a62` - Fechado (Tipo: CLOSING)

### Origem: Cartão recusado (Grupo: CJ - Ciclo Prioritário)
- **Origin ID:** `cb4835c8-c4d3-4586-85ff-ff904964529d`
- **Stages (Fases do Funil):**
  - `ee3873d6-144a-4a94-92d3-e1f6a5e92833` - Base (Tipo: BASE)
  - `c9b16ed5-5f19-467c-b80f-7fa53be12194` - Prospecção (Tipo: CUSTOM)
  - `9a0b664d-f373-4884-9887-ecb0d3ab65fa` - Conexão (Tipo: CUSTOM)
  - `4bf6ccf2-63aa-4389-8d6d-b316cb158275` - Aguardando compra (Tipo: CUSTOM)
  - `82601418-6aac-4a69-bb4e-e26678ea5a03` - Fechado (Tipo: CLOSING)

### Origem: Cartão recusado (Grupo: VDE 60D - OAB 1F)
- **Origin ID:** `c6a8de5b-52a0-43f3-973b-e1b122704838`
- **Stages (Fases do Funil):**
  - `e2fa3f5a-eab5-4616-8858-92e7639fbc2e` - Base (Tipo: BASE)
  - `e5e3d046-80fa-4f18-936d-c69c7425c41f` - Prospecção (Tipo: CUSTOM)
  - `893b5756-1829-46b5-adc9-a6d592063b68` - Conexão (Tipo: CUSTOM)
  - `3162ef4e-6916-4312-ac8d-c879235706cf` - Aguardando compra (Tipo: CUSTOM)
  - `0c148b9f-2b05-4f86-ac81-9624e66b7ed5` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex em atraso (Grupo: OAB - 1º Fase ANUAL)
- **Origin ID:** `c685418f-8124-43fc-9c72-e2e357300170`
- **Stages (Fases do Funil):**
  - `621bb788-2acf-4859-987f-5c5b7258ff8f` - Base (Tipo: BASE)
  - `16ff729f-5c41-45ab-b65c-22c68fbef071` - Sondagem (Tipo: CUSTOM)
  - `1a98c8b9-e06a-4790-b303-87bf4eb256c9` - Em contato (Tipo: CUSTOM)
  - `30e9ef0a-7967-4693-8227-d9ce78039861` - Fechado (Tipo: CLOSING)

### Origem: Abandono de carrinho (Grupo: ENAM - 90 Dias)
- **Origin ID:** `c4d4f925-6689-4b20-aa76-55d85835ed7d`
- **Stages (Fases do Funil):**
  - `86b1da3b-da3b-44bc-8598-7efd239bdda5` - Base (Tipo: BASE)
  - `1f0ece95-7ae9-45f6-aee9-fd8bcfed6715` - Prospecção (Tipo: CUSTOM)
  - `565e6c42-1e15-46d1-9a9a-f6456faa21d5` - Conexão (Tipo: CUSTOM)
  - `16ed6ac6-4030-4563-8b97-d89caf32b097` - Aguardando compra (Tipo: CUSTOM)
  - `d92a5922-4851-45a1-97b2-c0b7e6934c06` - Fechado (Tipo: CLOSING)

### Origem: Reembolso/Chargeback (Grupo: VDE 180D - OAB 1F)
- **Origin ID:** `c2ba8dee-e0b6-4ed6-b22e-78f92b4a4756`
- **Stages (Fases do Funil):**
  - `26ff2060-74b4-4c19-acc0-7aab089dea90` - Base (Tipo: BASE)
  - `a877d46a-145f-4cd4-9b48-c19dfee84387` - Sondagem (Tipo: CUSTOM)
  - `881e35bd-8c64-4dc2-ac02-2f0c345da613` - Em contato (Tipo: CUSTOM)
  - `1eb4a9ae-addf-4d68-b739-81ad63d86474` - Fechado (Tipo: CLOSING)

### Origem: Cartão recusado (Grupo: VDE 180D - OAB 1F)
- **Origin ID:** `c187f5ca-84ac-486a-bdba-8027eda64f16`
- **Stages (Fases do Funil):**
  - `c95b190a-1b1c-4e88-957d-bad22a645809` - Base (Tipo: BASE)
  - `4e1a2c89-576c-4b61-a7e8-5c9eccebbc5c` - Prospecção (Tipo: CUSTOM)
  - `7d1bb990-3046-4383-b22b-9e3f07691317` - Conexão (Tipo: CUSTOM)
  - `a2dd33ee-2942-4e85-9090-3430e96174fb` - Aguardando compra (Tipo: CUSTOM)
  - `0e2acb7e-8488-425d-a329-6d41e7ec7f07` - Fechado (Tipo: CLOSING)

### Origem: Reembolso/Chargeback (Grupo: OAB - Primeira Fase)
- **Origin ID:** `c1468e93-2e4e-428d-9475-14d37d5d5429`
- **Stages (Fases do Funil):**
  - `49a4f82e-bce4-4643-bd9b-554496f150e5` - Base (Tipo: BASE)
  - `d4fe1003-edc0-48b9-b979-5fc3606153a5` - Em recuperação (Tipo: CUSTOM)
  - `cace9501-ba89-4d86-811b-2a469aa32946` - Aguardando Pagamento (Tipo: CUSTOM)
  - `bbcf67ae-fcbd-4737-ac77-7c64e1b4d044` - Fechado (Tipo: CLOSING)

### Origem: Reembolso/Chargeback (Grupo: ENAM - ANUAL)
- **Origin ID:** `be7d960c-2231-46af-a9e5-5e5b9493c832`
- **Stages (Fases do Funil):**
  - `b02c790d-189b-4253-b864-315ab2102d93` - Base (Tipo: BASE)
  - `e5ef262b-bc02-4d52-8021-682f73a37c0e` - Sondagem (Tipo: CUSTOM)
  - `d54baf8f-7497-4d92-af11-493c128b955e` - Em contato (Tipo: CUSTOM)
  - `99b15c4e-9b9b-451b-9000-867c9f03c1d4` - Fechado (Tipo: CLOSING)

### Origem: VDE 40D - OAB 45 (Grupo: OAB - Primeira Fase)
- **Origin ID:** `b8eb8a51-16d7-4fc7-9a5a-1d2a27c48985`
- **Stages (Fases do Funil):**
  - `b14064a3-7898-4513-bfac-2b25c1c7130a` - Base (Tipo: BASE)
  - `48ec435f-3887-4052-be5a-d38a015660ed` - Prospecção (Tipo: CUSTOM)
  - `3dd2eb17-a26e-4c19-bb50-db2b7768caea` - Conexão (Tipo: CUSTOM)
  - `e9934ba5-6d56-4910-a4a1-46779177f898` - Aguardando Decisão (Tipo: CUSTOM)
  - `614d52c5-571b-4b34-936d-f4151e6f6f17` - Aguardando Compra (Tipo: CUSTOM)
  - `b42fcbaa-9d4b-44d3-ad4d-a70e770c6edb` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex canceladas (Grupo: VDE 60D - OAB 1F)
- **Origin ID:** `b5f50f15-881c-42bf-8bc8-d0c8b077cb67`
- **Stages (Fases do Funil):**
  - `7ec6cefa-d94c-4bad-9f9b-98c899090b92` - Base (Tipo: BASE)
  - `9d638ed5-b839-4751-8f4e-631007dec7af` - Sondagem (Tipo: CUSTOM)
  - `543a2103-4afd-4b39-8dfe-ab2895ebad04` - Em contato (Tipo: CUSTOM)
  - `42097e44-5f69-437e-8a45-106a433600d8` - Venda realizada (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex ativas (Grupo: VDE 60D - OAB 1F)
- **Origin ID:** `b51d7005-24a0-4adf-8edf-a76488046f59`
- **Stages (Fases do Funil):**
  - `eb7a8171-10d1-40d6-a7e3-2395e2f2ecbb` - Base (Tipo: BASE)
  - `56084add-6ce1-4220-8813-e4e5680f1df3` - On going (Tipo: CUSTOM)
  - `e15a0a95-14ac-4f85-b07b-92f9c26b2e88` - Sucesso (Tipo: CLOSING)

### Origem: Compras expiradas (Grupo: ENAM - ANUAL)
- **Origin ID:** `b4bb7f6e-7574-4a1d-b210-f465d7002634`
- **Stages (Fases do Funil):**
  - `017a34e3-7754-4738-b875-90e8b17eafdd` - Base (Tipo: BASE)
  - `4c57323a-768f-458b-a6d6-80bdac32df8d` - Prospecção (Tipo: CUSTOM)
  - `435a0ccb-09a2-428e-9f1b-17dbe892632b` - Conexão (Tipo: CUSTOM)
  - `02ad5a2f-3b15-4b7e-aa5b-618899975200` - Aguardando compra (Tipo: CUSTOM)
  - `1fbbea42-ace6-4b52-b199-1957e3d3b243` - Fechado (Tipo: CLOSING)

### Origem: Cronograma Anual (Grupo: ENAM - Preparatório)
- **Origin ID:** `b40aa410-1aa9-43bb-a28d-9a470d91efe4`
- **Stages (Fases do Funil):**
  - `7d453d14-d3c0-4dd5-b7b4-6360b73ddc42` - Base (Tipo: BASE)
  - `d195f0c0-c5be-4fef-a37c-2812c6d252d8` - Fechado (Tipo: CLOSING)

### Origem: Cartão recusado (Grupo: Hotmart - 6979776)
- **Origin ID:** `b0dfe6e0-06f3-4d6c-ad07-d43d40c51690`
- **Stages (Fases do Funil):**
  - `75eb8003-6a6a-4158-98a9-7c26d2eeddc8` - Base (Tipo: BASE)
  - `d6fb069e-6015-428f-b30d-0c00e91fdc6b` - Prospecção (Tipo: CUSTOM)
  - `0f8b8d29-2b39-4c26-a259-28c3d02673c7` - Conexão (Tipo: CUSTOM)
  - `7543baff-a235-4667-a751-d91c1c45ec67` - Aguardando compra (Tipo: CUSTOM)
  - `e9565dca-4ad1-452e-9424-4f59e91870e5` - Fechado (Tipo: CLOSING)

### Origem: Compras expiradas (Grupo: OAB - 1º Fase ANUAL)
- **Origin ID:** `b0ad33b9-039a-48f4-86e4-8e84e3298630`
- **Stages (Fases do Funil):**
  - `4cd14877-cb04-4a19-8354-4c8cbd3f75d9` - Base (Tipo: BASE)
  - `440dc29b-715d-4df1-b982-1ed2df70449e` - Prospecção (Tipo: CUSTOM)
  - `c0e99619-70f6-431f-ad8d-86feb54aa76e` - Conexão (Tipo: CUSTOM)
  - `31a91a50-4804-4111-86ae-a3584cb602d4` - Aguardando compra (Tipo: CUSTOM)
  - `ba1b3918-b33c-46ce-8c63-6a7fce3b86c7` - Fechado (Tipo: CLOSING)

### Origem: Compras em aberto (Grupo: OAB - 1º Fase ANUAL)
- **Origin ID:** `af2fabe4-367b-422b-bbf6-97769e7aaeb2`
- **Stages (Fases do Funil):**
  - `a4033f67-f836-4490-abf3-300160471049` - Base (Tipo: BASE)
  - `af98113c-18fd-470d-a546-4bfd3d55ebd5` - Prospecção (Tipo: CUSTOM)
  - `75f35eb4-1670-4cac-b5c6-43f8051ebc2c` - Conexão (Tipo: CUSTOM)
  - `0306403f-582c-4fc4-a3f7-caeb3a973405` - Aguardando compra (Tipo: CUSTOM)
  - `d4822279-596a-4dd8-b9ba-f53df2388b0b` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex ativas (Grupo: OAB - Segunda Fase)
- **Origin ID:** `a9a0bbec-5667-48a7-bb6f-de4c2e78e5c9`
- **Stages (Fases do Funil):**
  - `8d907375-5b79-4471-b736-8935ac3c14c8` - Base (Tipo: BASE)
  - `00e5379d-4c33-4614-961b-740b7698f0a7` - On going (Tipo: CUSTOM)
  - `9f56924d-e467-4615-a28a-3081244e5192` - Sucesso (Tipo: CLOSING)

### Origem: Inbound 2º Fase (Grupo: OAB - Segunda Fase)
- **Origin ID:** `a992dd0f-7993-4c25-b9d9-22b9cc59713a`
- **Stages (Fases do Funil):**
  - `36eda9ca-d97a-4e07-9245-ce5c2739ad29` - Base (Tipo: BASE)
  - `d6f4fa23-7ffe-4782-ac2f-b43c6eb2b5d6` - Conexão (Tipo: CUSTOM)
  - `05f63f36-d0e8-428b-aa5a-3099cbd67616` - Aguardando Decisão (Tipo: CUSTOM)
  - `598de1c5-2a80-4202-a017-f4fde4f9d2af` - Aguardando Pagamento (Tipo: CUSTOM)
  - `93d1601b-14ad-4d6e-b44b-8d0e369d10d2` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex canceladas (Grupo: OAB - Primeira Fase)
- **Origin ID:** `a46798f5-f0f3-44af-a3a4-7355ef7e9c2a`
- **Stages (Fases do Funil):**
  - `6a8a2931-cc31-4ed0-aa7f-7ea2bc63d5d3` - Base (Tipo: BASE)
  - `852c63c5-bfb5-467f-a9a8-7b7c21c135c8` - Sondagem (Tipo: CUSTOM)
  - `e9806e0a-42bb-4e24-a46b-6fc6cd31e4af` - Em contato (Tipo: CUSTOM)
  - `df5174dd-9162-4ff9-98ea-9348720e0bcd` - Venda realizada (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex canceladas (Grupo: Hotmart - 6384818)
- **Origin ID:** `a014113d-b0e6-43d6-89a9-50c5841af3e2`
- **Stages (Fases do Funil):**
  - `22c3612e-58d0-4ac5-89cb-7dcbad35581e` - Base (Tipo: BASE)
  - `1034223e-42bd-4080-9e33-4cb8357539ff` - Sondagem (Tipo: CUSTOM)
  - `a59ab272-da2c-428d-ba21-1c278b0232a5` - Em contato (Tipo: CUSTOM)
  - `795f2949-d961-4e23-b7ab-7ac8e2c7d775` - Venda realizada (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex canceladas (Grupo: ENAM - ANUAL)
- **Origin ID:** `9f5955fd-09d7-467d-a545-8b5751ab25b7`
- **Stages (Fases do Funil):**
  - `788fddb7-acb6-4595-852e-d1899b32be07` - Base (Tipo: BASE)
  - `c7242966-bb70-4c69-8a11-d08fd81464e4` - Sondagem (Tipo: CUSTOM)
  - `8b04eb38-f5bd-454f-8489-e6601dfa13a4` - Em contato (Tipo: CUSTOM)
  - `27b80e8d-4c80-4ec2-a577-e025f4721321` - Venda realizada (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex em atraso (Grupo: ENAM - 90 Dias)
- **Origin ID:** `9e2d069c-f27c-4dc8-9c2f-fd1c41fff77e`
- **Stages (Fases do Funil):**
  - `f0411a4d-f442-4103-8814-2aa776cfa6df` - Base (Tipo: BASE)
  - `fbf6dfa8-f3ac-4cea-aeec-0c7754fb4226` - Sondagem (Tipo: CUSTOM)
  - `9c35ce0a-1808-4d16-bd1e-09590fe421e8` - Em contato (Tipo: CUSTOM)
  - `d5386d2f-3351-49c5-9e53-c0efe151ad81` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex canceladas (Grupo: CJ - Ciclo Prioritário)
- **Origin ID:** `9ba97ec0-1887-4784-a24c-02338bd326f6`
- **Stages (Fases do Funil):**
  - `8380f468-2640-4e1e-8a39-ca1133e0373e` - Base (Tipo: BASE)
  - `3471045c-ece7-44ee-ad0c-daad6a9aa920` - Sondagem (Tipo: CUSTOM)
  - `95dcd786-44d1-47e0-9099-18a30305ae99` - Em contato (Tipo: CUSTOM)
  - `9a3b83ea-2c74-4f5c-8464-f0e93a50fa55` - Venda realizada (Tipo: CLOSING)

### Origem: Compras expiradas (Grupo: OAB - Primeira Fase)
- **Origin ID:** `9af7672d-d2c4-4612-86ae-0d784d80ce1c`
- **Stages (Fases do Funil):**
  - `d76e98f2-185f-4ca2-b5eb-c018f541e989` - Base (Tipo: BASE)
  - `973d29c5-63f2-4bdd-b8c0-2bfe1eb4ca2f` - Prospecção (Tipo: CUSTOM)
  - `8e51b161-9d70-40f0-bf9d-ae6da7e9b394` - Conexão (Tipo: CUSTOM)
  - `c034ff81-54b9-4c4c-bd59-5e92cc212569` - Aguardando compra (Tipo: CUSTOM)
  - `38732748-a32d-463a-a4ca-13ef33056fcb` - Fechado (Tipo: CLOSING)

### Origem: Lista Geral (Grupo: Hotmart - 6979776)
- **Origin ID:** `9a61cd09-e54c-4e70-a7ad-5042ecc9a9e1`
- **Stages (Fases do Funil):**
  - `6b72d0e0-5db7-4d23-9602-13cb3396267b` - Base (Tipo: BASE)
  - `596b7f1b-9715-4207-8f04-c309f28ba590` - Prospecção (Tipo: CUSTOM)
  - `344ca790-5e14-4ed1-9a3a-3ab530c6a447` - Conexão (Tipo: CUSTOM)
  - `be881adc-9024-4593-b921-d3e0b0c7b895` - Aguardando compra (Tipo: CUSTOM)
  - `98fe4c54-6b35-4a10-a028-b2164b81c9fd` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex canceladas (Grupo: OAB - Segunda Fase)
- **Origin ID:** `9a557d55-ab6a-4071-b785-2cd853ac5d81`
- **Stages (Fases do Funil):**
  - `f8d19502-cbf0-40d5-bb46-88e5f04e94a6` - Base (Tipo: BASE)
  - `155e32c2-35f9-4c05-b62c-badaaac8ab4e` - Sondagem (Tipo: CUSTOM)
  - `eba2424d-6eee-4df0-ae87-21808b58a69d` - Em contato (Tipo: CUSTOM)
  - `9813d31e-f539-470f-8885-66d985357efa` - Venda realizada (Tipo: CLOSING)

### Origem: VDE 90D - OAB 47 (Grupo: OAB - Primeira Fase)
- **Origin ID:** `99f29a58-bd50-486a-80b5-84639c929119`
- **Stages (Fases do Funil):**
  - `0616a82c-8cc3-48d1-9bcf-f33e6c176803` - Base (Tipo: BASE)
  - `a9595ec4-108d-4443-a47f-7f319a44c46a` - Prospecção (Tipo: CUSTOM)
  - `b644e40f-d74b-4644-9867-37d1b3e992e8` - Agendada (Tipo: CUSTOM)
  - `4417b3d9-e88f-46ab-a61d-4b6864af4dad` - Follow UP (Tipo: CUSTOM)
  - `7f7bdb1f-def3-4928-81b8-569fee697ff8` - Antes de Encerrar (Tipo: CUSTOM)
  - `0ac1df37-2eb8-410b-89af-f13d21597fbf` - Encerramento (Tipo: CUSTOM)
  - `3c702595-30ee-4713-9c35-2a733cc8f3ef` - Conexão (Tipo: CUSTOM)
  - `0b3975b9-15ed-4f28-be89-e31c8f3e2ddc` - Aguardando pagamento (Tipo: CUSTOM)
  - `260dfcd7-c3b3-444d-b17d-a61aeee293af` - Fechado (Tipo: CLOSING)

### Origem: Abandono de carrinho (Grupo: OAB - Primeira Fase)
- **Origin ID:** `9757f58c-9bd3-429d-9501-b6064c50f5f2`
- **Stages (Fases do Funil):**
  - `ea4a87d0-8877-420b-bc69-243a61ede773` - Base (Tipo: BASE)
  - `45fdfa10-ef4b-4149-b344-71a112b3a808` - Prospecção (Tipo: CUSTOM)
  - `7f2d591f-04c5-412e-ad1f-983074e45158` - Conexão (Tipo: CUSTOM)
  - `a76713a6-4193-4168-a4a5-933a65f34d66` - Aguardando Decisão (Tipo: CUSTOM)
  - `c2c8d2d2-7732-47d7-a361-46afb4b85c46` - Aguardando compra (Tipo: CUSTOM)
  - `e473a2ae-e951-424d-b9b2-60072a8dd779` - Fechado (Tipo: CLOSING)

### Origem: Compras expiradas (Grupo: OAB - Segunda Fase)
- **Origin ID:** `9054a9b5-5e88-4917-83bf-d4fb63249a9c`
- **Stages (Fases do Funil):**
  - `ae1e9b0d-cd62-48ba-940e-5ee85c1dcdb7` - Base (Tipo: BASE)
  - `ddf19cca-67d1-432f-bd5c-425e589fb87a` - Prospecção (Tipo: CUSTOM)
  - `b47326fd-2a55-4359-8d9b-b24b80c3465c` - Conexão (Tipo: CUSTOM)
  - `ad7ba7bc-b368-45dd-9c87-715971a4e4ff` - Aguardando compra (Tipo: CUSTOM)
  - `a6695d5a-6f95-42f9-8cae-f18189b391e7` - Fechado (Tipo: CLOSING)

### Origem: Compras aprovadas (Grupo: Hotmart - 6384818)
- **Origin ID:** `8f463240-cbb6-477f-96fe-fb4839079967`
- **Stages (Fases do Funil):**
  - `7e4c12ca-61ad-4a94-823a-3cd2c77bd1e1` - Base (Tipo: BASE)
  - `7573635c-e31d-4790-8db9-3203328d3e47` - Onboarding (Tipo: CUSTOM)
  - `a9ba32cf-ee4a-48a8-8e48-4f2a06146018` - On going (Tipo: CUSTOM)
  - `7056b0ce-5640-4472-8280-3fd55ac8ed71` - Sucesso (Tipo: CLOSING)

### Origem: Compras em aberto (Grupo: OAB - Segunda Fase)
- **Origin ID:** `8e2e29d3-dc19-4957-a85a-430f74a29823`
- **Stages (Fases do Funil):**
  - `8ea16a1c-98aa-4d0d-a1cf-300e32894038` - Base (Tipo: BASE)
  - `e3682c9c-9a64-48bb-96be-feaf2813ac04` - Prospecção (Tipo: CUSTOM)
  - `f2c58258-f7a4-484d-9303-334c22140bb3` - Conexão (Tipo: CUSTOM)
  - `0a38e190-fb4f-4757-9207-62b97e64ba94` - Aguardando compra (Tipo: CUSTOM)
  - `ee22c8f1-1891-46d0-954e-a65824b481c8` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex em atraso (Grupo: Hotmart - 6384818)
- **Origin ID:** `8c3a790d-e006-4d3a-9fed-a97da03a1058`
- **Stages (Fases do Funil):**
  - `7bf76e33-7af5-4cc8-a49c-9b6386cb1606` - Base (Tipo: BASE)
  - `da8dcc56-21e0-454e-a247-50ac8926b5fd` - Sondagem (Tipo: CUSTOM)
  - `b660311d-ea02-4285-971d-e8b51847aef7` - Em contato (Tipo: CUSTOM)
  - `d90bc7f1-2f17-4920-b905-66872ba2a7d9` - Fechado (Tipo: CLOSING)

### Origem: Abandono de carrinho (Grupo: OAB - 1º Fase ANUAL)
- **Origin ID:** `8a4f1dde-d704-401e-b853-7ff79c10451d`
- **Stages (Fases do Funil):**
  - `4a14291f-379d-4da4-a4dd-30671ca47ab2` - Base (Tipo: BASE)
  - `c5632f02-09c0-42a3-8b71-cd9c085b7d74` - Prospecção (Tipo: CUSTOM)
  - `0ec74338-aa99-43bc-a047-49ab108a38d2` - Conexão (Tipo: CUSTOM)
  - `74fde6cf-9f03-44be-901e-c6ad02e97052` - Aguardando compra (Tipo: CUSTOM)
  - `630a4e8e-9944-49cd-85f5-1bdfe3129784` - Fechado (Tipo: CLOSING)

### Origem: Leads Quentes - URGENTE! (Grupo: CJ - Ciclo Prioritário)
- **Origin ID:** `87985431-fca0-4c27-9aac-a1b94e733e06`
- **Stages (Fases do Funil):**
  - `7555d313-8561-45ad-ab1c-7a8141172721` - Base (Tipo: BASE)
  - `233e78ad-d694-4d24-ad6c-d659df19dd34` - Prospecção (Tipo: CUSTOM)
  - `1c587169-5989-415d-baa7-57555b9fd10a` - Envio de Material (Tipo: CUSTOM)
  - `8849e031-dd99-46d9-8280-24620951cfce` - Curiosidade sobre nossa plataforma (Tipo: CUSTOM)
  - `505ec47b-52ba-485f-b192-8113c0f77a8c` - Encerramento (Tipo: CUSTOM)
  - `11def7a5-8802-4da8-a20a-1ddb295c4327` - Conexão (Tipo: CUSTOM)
  - `9bebf64d-110d-4a57-acbf-e6615402e789` - Apresentação Meet (Tipo: CUSTOM)
  - `3955de53-5705-47c0-b82f-6fbfca3b1517` - Aguardando Fechamento (Tipo: CUSTOM)
  - `ffa2484a-fbd0-406d-adb6-f8ef891e3e09` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex canceladas (Grupo: Hotmart - 6979776)
- **Origin ID:** `8785ccc3-6ac4-4c97-8245-7e13142c9a3c`
- **Stages (Fases do Funil):**
  - `e38a60f2-fdb9-409b-98c6-0be6378b28de` - Base (Tipo: BASE)
  - `2aad58fe-5ac1-4e69-8abc-4729d57db408` - Sondagem (Tipo: CUSTOM)
  - `dfe7f45f-8a49-4a3f-b412-3d4785c13f57` - Em contato (Tipo: CUSTOM)
  - `fa10af4d-323e-4fda-88d4-5de8eda86a59` - Venda realizada (Tipo: CLOSING)

### Origem: Inbound 1º Fase (Grupo: OAB - Primeira Fase)
- **Origin ID:** `8209dfcf-206d-4f96-9f92-b13a899e3510`
- **Stages (Fases do Funil):**
  - `23a1cc3c-14bd-405a-9360-92cc57a9f681` - Base (Tipo: BASE)
  - `7a619e0a-edb0-422d-b0fa-3a39259a0393` - Conexão (Tipo: CUSTOM)
  - `0a85925e-29d6-447d-ae62-9522aa70659b` - Aguardando Decisão (Tipo: CUSTOM)
  - `6beb64a6-00e5-4ad6-b92a-8b8ccc3a99b9` - Aguardando Pagamento (Tipo: CUSTOM)
  - `04dbced6-0afa-434a-b73f-08d18ea582d7` - Fechado (Tipo: CLOSING)

### Origem: LG - 2º FASE (Grupo: OAB - Segunda Fase)
- **Origin ID:** `804bae2b-14c4-48cb-8cb6-282f547e061f`
- **Stages (Fases do Funil):**
  - `763cc768-115f-4ac2-a44c-dc95d580f267` - Base (Tipo: BASE)
  - `4d9a4eb0-fd55-4dfd-a8cc-f76551212ad5` - Prospecção (Tipo: CUSTOM)
  - `fb615c76-c9c8-45de-beee-f71c626105e7` - Conexão (Tipo: CUSTOM)
  - `7fd61f7b-9352-4ea2-afd3-4e252ca861e8` - Agendada (Tipo: CUSTOM)
  - `58af7bfe-e7bc-4cc0-a25b-08cc2a35c200` - Aguardando Pagamento (Tipo: CUSTOM)
  - `de3a384f-d6ed-4c47-b536-acc666619c76` - Fechado (Tipo: CLOSING)

### Origem: Interessados 120D - OAB 44 (Grupo: OAB - Primeira Fase)
- **Origin ID:** `7e4ad0ed-b3d3-4169-8193-9cd912565b6f`
- **Stages (Fases do Funil):**
  - `84e8f8d0-78f2-41ab-bbdb-18f6294c4259` - Base (Tipo: BASE)
  - `76017aa2-63ea-480c-97f6-2790187407c3` - Chamar pro Agendamento (Tipo: CUSTOM)
  - `ce7c94cc-517b-436c-88c9-5d4357e9e605` - Aguardando confirmação (Tipo: CUSTOM)
  - `7590233c-3160-49f1-ac8f-ed2123d20c6d` - Contato Agendado (Tipo: CUSTOM)
  - `04f06bb1-3baa-4e0d-9641-d120e5216550` - Contato Realizado (Tipo: CUSTOM)
  - `f6277cb6-627a-4682-99fc-a3a489f39d91` - Fechado (Tipo: CLOSING)

### Origem: Alunos Reprovados_OAB 42 2º Fase (Grupo: OAB - Segunda Fase)
- **Origin ID:** `7e2655a5-00c0-43e4-bb42-6301cf2498ec`
- **Stages (Fases do Funil):**
  - `939e5b5c-c94f-47ae-b300-feb7cfb1d40b` - Base (Tipo: BASE)
  - `2065550f-f636-4f9a-954f-9307bc3546c7` - Prospecção (Tipo: CUSTOM)
  - `f51e664e-25e7-4e35-96c3-aacca8f65fa7` - Conexão (Tipo: CUSTOM)
  - `e57e482a-da0e-49fd-a273-af1a3231bf4d` - Aguardando Decisão (Tipo: CUSTOM)
  - `7ca3f85e-2b96-41e6-8039-70fc563ef1f7` - Aguardando Pagamento (Tipo: CUSTOM)
  - `7fe202c0-0c23-479b-875a-3cffd200a346` - Fechado (Tipo: CLOSING)

### Origem: Ciclo Prioritário (Grupo: CJ - Ciclo Prioritário)
- **Origin ID:** `7be48c06-7cfe-464a-9c08-cb6a58feb27b`
- **Stages (Fases do Funil):**
  - `ddf0f0f7-7146-4720-8b51-5333f290dee8` - Base (Tipo: BASE)
  - `d4cbcd2d-f33a-4f4b-a9e9-b10ab43cff97` - Agendado (Tipo: CUSTOM)
  - `17908828-bb0c-47d3-9362-b940e05a159a` - Prospecção (Tipo: CUSTOM)
  - `2e49e233-1c4b-4032-84fb-a26d9aa79e42` - Material Gratuito (Tipo: CUSTOM)
  - `07d299ac-2edf-46ab-ba79-d270078f47bf` - Material Enviado (Tipo: CUSTOM)
  - `49524bb4-55af-4351-8d2a-f74d1f99b74c` - Não Respondeu (Tipo: CUSTOM)
  - `a6116936-cec2-4809-9610-9081fc9798e5` - Após Envio do Material (Tipo: CUSTOM)
  - `40b4ed00-2e29-4182-a6ec-c482ba8b6ea4` - Encerramento (Tipo: CUSTOM)
  - `ea207ca0-3147-4a7b-b36c-9b6d14648ead` - Conexão (Tipo: CUSTOM)
  - `d03a7b60-c3f1-4502-91ca-d8b970e20af0` - Aguardando compra (Tipo: CUSTOM)
  - `76ed58d9-cb7d-4370-8a9b-af32b5b7d6bb` - Fechado (Tipo: CLOSING)

### Origem: Lista Geral - 180 Dias (Grupo: VDE 180D - OAB 1F)
- **Origin ID:** `79348a32-c33b-45e5-b0c5-c0600a778ba7`
- **Stages (Fases do Funil):**
  - `555ead9e-f4e9-414f-bd71-50719d157ce0` - Base (Tipo: BASE)
  - `6f6f6f44-cfce-4f52-bf92-ef6205604133` - Prospecção (Tipo: CUSTOM)
  - `0316ec57-61bd-4e8c-a15c-3f57b6c60cae` - Agendamento (Tipo: CUSTOM)
  - `af987003-b6f0-4bb2-afab-1617c175224b` - Follow UP 1 (Tipo: CUSTOM)
  - `173e8885-d417-4b28-8fa6-e2bf27343e9d` - Follow Up 2 (Tipo: CUSTOM)
  - `cbdf4693-e4e7-4e02-8134-c860dd3c7d11` - Encerramento (Tipo: CUSTOM)
  - `eddc1ddd-fd13-4faf-b788-c7646cd76787` - Conexão (Tipo: CUSTOM)
  - `78dd7169-5ba2-44fb-8b0b-aa0ec5b23e2c` - Aguardando Compra (Tipo: CUSTOM)
  - `463dfd15-7db3-46ba-8ac5-52db8086f0e3` - Fechado (Tipo: CLOSING)

### Origem: Compras aprovadas (Grupo: ENAM - ANUAL)
- **Origin ID:** `77adc9c7-3638-4b95-b783-89fde3710a1b`
- **Stages (Fases do Funil):**
  - `2a088a76-734d-4aae-8a17-efd8a56609e3` - Base (Tipo: BASE)
  - `0cd6bcd1-55f5-44c1-b484-44d23c2b99d3` - Onboarding (Tipo: CUSTOM)
  - `d861f87f-5e7d-4ee4-8c89-0a44421e1296` - On going (Tipo: CUSTOM)
  - `ed46ef84-b301-4bbb-bd23-d42a2492f0b7` - Sucesso (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex canceladas (Grupo: ENAM - 90 Dias)
- **Origin ID:** `770076ac-be85-4be7-b7ea-abcc2b789f5a`
- **Stages (Fases do Funil):**
  - `2a414b2b-af83-4c1a-bf7d-a78a444ce751` - Base (Tipo: BASE)
  - `f37c6e07-515e-4beb-9aa3-cfdbcdac34cc` - Sondagem (Tipo: CUSTOM)
  - `99a374fb-4a1e-4164-8a99-96a53476df51` - Em contato (Tipo: CUSTOM)
  - `d4321adc-ebbc-42de-ab7a-de6bb24f3895` - Venda realizada (Tipo: CLOSING)

### Origem: Reembolso/Chargeback (Grupo: OAB - 1º Fase ANUAL)
- **Origin ID:** `7619fde4-754d-4312-ab0a-18937ed20883`
- **Stages (Fases do Funil):**
  - `7f6b0c06-0ccd-49b0-84eb-0aa327d3eb79` - Base (Tipo: BASE)
  - `721dcdcf-5bb0-4d44-9bcb-64f3b1998aa2` - Sondagem (Tipo: CUSTOM)
  - `57a27f31-3939-432f-8d68-ecfe59c8b4a4` - Em contato (Tipo: CUSTOM)
  - `f3d345c3-5310-480e-9c08-8f1bc8d0b1ad` - Fechado (Tipo: CLOSING)

### Origem: Lista Geral (Grupo: OAB - Segunda Fase)
- **Origin ID:** `745baa00-4157-4a27-975a-497bd21af64e`
- **Stages (Fases do Funil):**
  - `131d3a70-aba6-4e48-94c9-dbc2603cde96` - Base (Tipo: BASE)
  - `6b90a4b7-a080-41b8-bfb8-bfd6839ec033` - Prospecção (Tipo: CUSTOM)
  - `eed4801f-8025-4da5-a74b-1e02465a7615` - Conexão (Tipo: CUSTOM)
  - `7ef97b82-76d8-4ea3-abc4-32a60cbaf80f` - Aguardando compra (Tipo: CUSTOM)
  - `d947dc6b-a093-4471-a22a-937e835015ca` - Fechado (Tipo: CLOSING)

### Origem: Compras expiradas (Grupo: Hotmart - 6384818)
- **Origin ID:** `734bbbcb-e486-4ced-8c12-cf4822c647fd`
- **Stages (Fases do Funil):**
  - `2d95e1f2-765b-4c28-a0f2-6efc8608f688` - Base (Tipo: BASE)
  - `d024a3ab-e3ff-49c9-bc57-cd6daaaa516f` - Prospecção (Tipo: CUSTOM)
  - `bf4f5a9d-0681-4ada-a342-00e7b919bf5a` - Conexão (Tipo: CUSTOM)
  - `57659556-7863-43f4-9b46-ebe23e50761c` - Aguardando compra (Tipo: CUSTOM)
  - `70d953f1-5449-49de-a0ad-8a7f684efed3` - Fechado (Tipo: CLOSING)

### Origem: Cartão recusado (Grupo: OAB - Primeira Fase)
- **Origin ID:** `717536cb-2fcc-4c84-aa93-471f1dd32c57`
- **Stages (Fases do Funil):**
  - `57701127-e97f-42db-8cd0-de78a4b1cbd7` - Base (Tipo: BASE)
  - `a8d30d8a-dd11-4ab4-b812-b469d4756262` - Prospecção (Tipo: CUSTOM)
  - `dee3ef06-7d07-45c9-9d7b-5a227b8fddee` - Conexão (Tipo: CUSTOM)
  - `d34b8311-1ad8-450e-b316-b695366d4008` - Aguardando Decisão (Tipo: CUSTOM)
  - `3fb1a347-8efa-4af8-948c-d6314a2967dd` - Aguardando compra (Tipo: CUSTOM)
  - `ac6b4355-f12d-4146-af8b-6374ebe55b15` - Fechado (Tipo: CLOSING)

### Origem: Compras expiradas (Grupo: VDE 180D - OAB 1F)
- **Origin ID:** `713ce006-ce98-4bfe-a728-e9b1cde89361`
- **Stages (Fases do Funil):**
  - `3ad4bb31-7b64-49e9-aa3f-03ec06f43316` - Base (Tipo: BASE)
  - `5156d693-929c-4d61-b3ee-a715a3c0319f` - Prospecção (Tipo: CUSTOM)
  - `1504d71a-6352-4c6a-bd4c-7b1ab7570445` - Conexão (Tipo: CUSTOM)
  - `38ef6465-04f8-4a8a-bfaf-94be28205d1f` - Aguardando compra (Tipo: CUSTOM)
  - `f69a74cf-6a77-4a5e-a231-eb2d70ab56d0` - Fechado (Tipo: CLOSING)

### Origem: Cartão recusado (Grupo: ENAM - ANUAL)
- **Origin ID:** `704dca8f-ecb4-4474-b13c-6d0a9e288746`
- **Stages (Fases do Funil):**
  - `ff31b347-8a24-42a7-be89-cbcc0db30c71` - Base (Tipo: BASE)
  - `e037db89-62a6-400b-bec4-0ffa326f0b1d` - Prospecção (Tipo: CUSTOM)
  - `f532aa6d-21e7-4891-8d35-364dfbf32c13` - Conexão (Tipo: CUSTOM)
  - `9afffe91-6dea-4281-b386-c8a58f3aee89` - Aguardando compra (Tipo: CUSTOM)
  - `1dc414b7-bc57-4048-a496-f57d20ce36bb` - Fechado (Tipo: CLOSING)

### Origem: Compras aprovadas (Grupo: CJ - Ciclo Prioritário)
- **Origin ID:** `6c35118f-c8fb-47d0-83fb-8b805a93e06a`
- **Stages (Fases do Funil):**
  - `b6990548-2b8e-4683-8577-328799dd071e` - Base (Tipo: BASE)
  - `23a722c5-f3b3-4ab6-b4d8-bdcfb3dcb4da` - Onboarding (Tipo: CUSTOM)
  - `2e5b0718-ef68-44f8-9d5d-d9e8714548e5` - On going (Tipo: CUSTOM)
  - `8952473a-a268-4afb-b42c-c604c2ecc66f` - Sucesso (Tipo: CLOSING)

### Origem: Compras aprovadas (Grupo: OAB - Segunda Fase)
- **Origin ID:** `63dd8b0f-8b01-4750-b0dd-19ef60ed5624`
- **Stages (Fases do Funil):**
  - `522b5fa0-8369-48d6-b2e7-bfa209f1c21e` - Base (Tipo: BASE)
  - `eebc51ca-8c6d-4402-aee6-f4bb02b3c200` - Onboarding (Tipo: CUSTOM)
  - `48c9250a-dedb-49da-b1e2-15fb396477bb` - On going (Tipo: CUSTOM)
  - `7d56c75a-a02e-4339-b8c2-104c7c9bfd62` - Sucesso (Tipo: CLOSING)

### Origem: LG - ENAM ANUAL (Grupo: ENAM - ANUAL)
- **Origin ID:** `5e77a45c-b780-4373-a7a5-b2a199e9a93a`
- **Stages (Fases do Funil):**
  - `526a684e-3444-447f-9187-d6f78a0d1c60` - Base (Tipo: BASE)
  - `52a6d4c3-50aa-4566-a4be-f3010edb3c46` - Agendamentos (Tipo: CUSTOM)
  - `8adb1a82-5d8c-41c8-ba67-52d2a8c1e475` - Conexão (Tipo: CUSTOM)
  - `e7a22760-ee76-4ee5-9915-ed748661cba6` - Aguardando compra (Tipo: CUSTOM)
  - `8ef6c3eb-3f31-441a-aed4-60121667a0ec` - Fechado (Tipo: CLOSING)

### Origem: recuperação (Grupo: Comercial)
- **Origin ID:** `5df0a7bd-aa45-4693-a9d0-6fe1d640413c`
- **Stages (Fases do Funil):**
  - `f2b74c14-0bb1-47ea-b279-f22353daf0ae` - Base (Tipo: BASE)
  - `98a12703-2a02-4562-8725-f41f5f5ba6a0` - Prospecção (Tipo: CUSTOM)
  - `2543e39a-ceee-4b1d-9c97-e528790c7b45` - Conexão (Tipo: CUSTOM)
  - `c47702f7-a0cf-44ed-8c0a-1cc3799b12a4` - Aguardando compra (Tipo: CUSTOM)
  - `fb6632e0-9841-465b-b421-21b38032db3a` - Fechado (Tipo: CLOSING)

### Origem: Inbound OAB (Grupo: Inbound Whatsapp)
- **Origin ID:** `5ba3c273-a802-4991-b934-960929047c2d`
- **Stages (Fases do Funil):**
  - `7ea54f15-7d6b-4dec-ae1d-ba5c7f1b2108` - Base (Tipo: BASE)
  - `ebe52faf-cf63-411c-aea4-43288fb4beee` - Conexão (Tipo: CUSTOM)
  - `276e8a0f-536e-4b7f-b843-8134fba68072` - Aguardando Decisão (Tipo: CUSTOM)
  - `fbebf691-f279-400e-bdda-3bc0b6f10709` - Aguardando Pagamento (Tipo: CUSTOM)
  - `06db54f6-e557-46b8-8608-fd57afd40b42` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex em atraso (Grupo: CJ - Ciclo Prioritário)
- **Origin ID:** `5792debe-c804-4ee9-9371-84ad585e87f5`
- **Stages (Fases do Funil):**
  - `4cdb081e-b78c-4430-b897-aabcd6072c76` - Base (Tipo: BASE)
  - `77d88e31-0781-44a3-82f3-d23be33fb8ca` - Sondagem (Tipo: CUSTOM)
  - `8b9ee88d-11c8-4abc-8e81-67aa126b1f77` - Em contato (Tipo: CUSTOM)
  - `80c4074e-2e1b-4fec-8c45-27b699c2b680` - Fechado (Tipo: CLOSING)

### Origem: Abandono de carrinho (Grupo: VDE 180D - OAB 1F)
- **Origin ID:** `55848529-0071-4d3e-9052-ea54697283cd`
- **Stages (Fases do Funil):**
  - `2a3a8223-6b98-41aa-920d-ed6204fbea5f` - Base (Tipo: BASE)
  - `87f87f50-1ad9-4611-a745-2f2bc5fca5ab` - Prospecção (Tipo: CUSTOM)
  - `be815422-91d3-4788-94b8-b5db4515b1dd` - Conexão (Tipo: CUSTOM)
  - `225870f7-7628-4f62-961c-12f2430acd61` - Aguardando compra (Tipo: CUSTOM)
  - `ef82b3ec-2fd4-4790-acd1-d07f1b114be4` - Fechado (Tipo: CLOSING)

### Origem: Lista Geral (Grupo: OAB - Primeira Fase)
- **Origin ID:** `5483f06d-4bd2-4f16-9b14-706fe18a2bc4`
- **Stages (Fases do Funil):**
  - `e17cde90-39bc-4215-b4a7-75ef7729eb67` - Base (Tipo: BASE)
  - `0939fe97-4ff2-4169-8539-beae6d78a460` - Prospecção (Tipo: CUSTOM)
  - `89e6b07c-2ce1-4d1e-b458-3237bb5b846c` - Conexão (Tipo: CUSTOM)
  - `95e02879-5e1a-4fdb-866f-69cb167679b2` - Aguardando compra (Tipo: CUSTOM)
  - `6e8cf6d4-f65b-4833-b244-70026184239d` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex em atraso (Grupo: VDE 60D - OAB 1F)
- **Origin ID:** `52260597-d678-4c1b-a414-cae6357b9032`
- **Stages (Fases do Funil):**
  - `19015eb6-8041-4a1e-8cad-e374030f0963` - Base (Tipo: BASE)
  - `dcc0714d-b26b-4dbb-b196-493fdeb64f1f` - Sondagem (Tipo: CUSTOM)
  - `ea4aca8e-a783-421f-ac4b-6ada7c20977d` - Em contato (Tipo: CUSTOM)
  - `8b96bcd4-6876-4a6b-b9f3-a71bf0c5de5e` - Fechado (Tipo: CLOSING)

### Origem: Captação Nocaute 43_ Lead OAB 44 (Grupo: OAB - Primeira Fase)
- **Origin ID:** `5030c76a-7ee8-4814-b431-0467f35aa768`
- **Stages (Fases do Funil):**
  - `498285c2-eed6-4977-ac90-3fe3c0b6b087` - Base (Tipo: BASE)
  - `34c486d7-0387-41e9-baf5-6450de386a39` - Prospecção (Tipo: CUSTOM)
  - `abe24701-867d-4c91-ba28-376727fe88b1` - Conexão (Tipo: CUSTOM)
  - `a040206f-30d0-4cd4-9a4c-48d1e8400ecd` - Aguardando Decisão (Tipo: CUSTOM)
  - `be8ab4da-a100-4c8a-a2b8-32d82442c287` - Aguardando Compra (Tipo: CUSTOM)
  - `edcc2953-7b02-4605-91a5-c216a84932ed` - Fechado (Tipo: CLOSING)

### Origem: Compras expiradas (Grupo: VDE 60D - OAB 1F)
- **Origin ID:** `4cd40e3a-34e9-41b2-9e11-3aef507fd867`
- **Stages (Fases do Funil):**
  - `83e817e4-08bb-4799-8090-78b288c9c81b` - Base (Tipo: BASE)
  - `2a44e7bf-d344-43fa-83b8-4fe20b632840` - Prospecção (Tipo: CUSTOM)
  - `de219b9b-97b2-4787-b6ed-279949f31411` - Conexão (Tipo: CUSTOM)
  - `ca937ce8-14b1-4782-a81f-bd53ba98b517` - Aguardando compra (Tipo: CUSTOM)
  - `460a5eac-a7ce-444d-b78c-462c75a98aeb` - Fechado (Tipo: CLOSING)

### Origem: VDE 40D - OAB 46 (Grupo: OAB - Primeira Fase)
- **Origin ID:** `4c852af6-0e39-4f92-902b-7bdce04f0f6f`
- **Stages (Fases do Funil):**
  - `19ec8513-ead4-47cb-9bfd-0da4341ef452` - Base (Tipo: BASE)
  - `3f123c48-99c0-41cc-b694-db91cd6b2fa8` - Prospecção (Tipo: CUSTOM)
  - `7259a56a-e083-42c2-b9d0-beeb12e908db` - Agendadas (Tipo: CUSTOM)
  - `93c32591-7996-4f40-9655-e9563e354391` - Conexão (Tipo: CUSTOM)
  - `8213fcf2-12de-442e-ae16-01fdfcbc1625` - Aguardando Pagamento (Tipo: CUSTOM)
  - `68a94c77-5cc0-45cd-b727-508dc8d4cc5d` - Fechado (Tipo: CLOSING)

### Origem: Compras em aberto (Grupo: VDE 180D - OAB 1F)
- **Origin ID:** `4905f56b-606b-477f-b1b2-d5a8f0e93c08`
- **Stages (Fases do Funil):**
  - `94617427-4860-4e4f-8e2c-da08f5b7d738` - Base (Tipo: BASE)
  - `a91dfbb3-ea71-4348-9cb0-7214f07f2a92` - Prospecção (Tipo: CUSTOM)
  - `f8db9558-9c8b-4058-accd-b83bdacd896c` - Conexão (Tipo: CUSTOM)
  - `f794075f-57cf-4061-9b3a-3e1e438b63ea` - Aguardando compra (Tipo: CUSTOM)
  - `f1f406fe-fd7d-481d-a098-35b539a89a50` - Fechado (Tipo: CLOSING)

### Origem: Inbound - 1º Fase (Grupo: OAB - Primeira Fase)
- **Origin ID:** `46d14cb0-f9cb-42c8-a667-f709c38ac63e`
- **Stages (Fases do Funil):**
  - `43ab09d6-9f65-40a4-b769-3b76382d8146` - Base (Tipo: BASE)
  - `31d091b3-4208-455f-a200-ec906bb20f78` - Conexão (Tipo: CUSTOM)
  - `960f8b95-7ce1-49e1-b31f-f439ef065be9` - Aguardando Decisão (Tipo: CUSTOM)
  - `00ecda21-3a0b-4170-a5d2-649f5f92421a` - Aguardando Pagamento (Tipo: CUSTOM)
  - `258e0556-86e0-4569-a206-c841c7324020` - Fechado (Tipo: CLOSING)

### Origem: Abandono de carrinho (Grupo: OAB - Segunda Fase)
- **Origin ID:** `461ca700-b6ec-4bf1-96cf-3a79521cd458`
- **Stages (Fases do Funil):**
  - `3cbde6df-47fa-44c6-b26e-3d985a910f62` - Base (Tipo: BASE)
  - `faa725c1-cf09-4400-bdff-2f9ece95f7de` - Prospecção (Tipo: CUSTOM)
  - `36256444-6804-4d35-8f71-c4058dc98970` - Conexão (Tipo: CUSTOM)
  - `df4c5074-3ca1-4000-94bf-3654e7a36baf` - Aguardando compra (Tipo: CUSTOM)
  - `28be2fb4-abee-42be-83e4-af33197fc99e` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex ativas (Grupo: VDE 180D - OAB 1F)
- **Origin ID:** `43f48e13-5019-424d-a8cf-254848cde0f9`
- **Stages (Fases do Funil):**
  - `821cb503-6ea2-4206-8f88-6edb870db1ae` - Base (Tipo: BASE)
  - `12270195-092e-441a-87bf-c7b9013cc698` - On going (Tipo: CUSTOM)
  - `ce176a15-ea7f-4ad6-8ef6-0faffe9a4431` - Sucesso (Tipo: CLOSING)

### Origem: Compras aprovadas (Grupo: VDE 60D - OAB 1F)
- **Origin ID:** `41c6b638-541f-48ca-b2f7-4f73c7dd9059`
- **Stages (Fases do Funil):**
  - `5d62f652-105f-42aa-a15b-3d5514184b7d` - Base (Tipo: BASE)
  - `cf0609bd-488b-49e0-aae4-39464e66ed43` - Onboarding (Tipo: CUSTOM)
  - `2152bcff-9841-4a8e-bc04-97843de3aa06` - On going (Tipo: CUSTOM)
  - `adf099a4-1db1-40c0-991b-e716e09453cb` - Sucesso (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex canceladas (Grupo: VDE 180D - OAB 1F)
- **Origin ID:** `3c32b401-7035-4bae-b6b5-733efb2ffd9a`
- **Stages (Fases do Funil):**
  - `ea38461e-ebf2-4495-b117-e58b6304fb4b` - Base (Tipo: BASE)
  - `98108ce1-5001-40ae-9dd4-819cd3d8ec44` - Sondagem (Tipo: CUSTOM)
  - `13d9ed8f-5759-4e11-83a9-07d868dcaab3` - Em contato (Tipo: CUSTOM)
  - `79ee2b17-6441-4400-b9bd-99bbffa3b1ba` - Venda realizada (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex em atraso (Grupo: ENAM - ANUAL)
- **Origin ID:** `38ac79d2-a18e-4e82-8765-24477972e4b9`
- **Stages (Fases do Funil):**
  - `aebbd6d0-dbff-45cc-a15a-1bbd7b02b59a` - Base (Tipo: BASE)
  - `c1669717-2510-48c1-9384-7e9110f29e07` - Sondagem (Tipo: CUSTOM)
  - `e95c0cf5-dcaf-4168-b0c0-7e56377cbf0e` - Em contato (Tipo: CUSTOM)
  - `404d84fb-daa8-40a9-9172-6229fe09faa4` - Fechado (Tipo: CLOSING)

### Origem: Compras em aberto (Grupo: Hotmart - 6979776)
- **Origin ID:** `370a49ac-caf6-4c55-8e47-291e22b78892`
- **Stages (Fases do Funil):**
  - `efde2c30-f61b-4516-b223-1ba77ff1fc14` - Base (Tipo: BASE)
  - `971f2281-1858-482d-b576-85cf0cec76b2` - Prospecção (Tipo: CUSTOM)
  - `ec96ad87-f911-4b3a-ac1f-cb9d7f12b657` - Conexão (Tipo: CUSTOM)
  - `a422a0f8-c1cf-4a72-aee1-a6262612c2da` - Aguardando compra (Tipo: CUSTOM)
  - `38057d21-ae43-40b8-bf89-e59088ad0833` - Fechado (Tipo: CLOSING)

### Origem: N8N (Grupo: N8N)
- **Origin ID:** `36634fbe-8f13-4148-aa8a-4921b1ebbc5f`
- **Stages (Fases do Funil):**
  - `37681980-fd55-4f1c-a41e-8cd908d356b6` - Base (Tipo: BASE)
  - `e38f3e1d-4457-4b54-839c-858f42601a9f` - Fechado (Tipo: CLOSING)

### Origem: Compras aprovadas (Grupo: ENAM - 90 Dias)
- **Origin ID:** `358fe4e5-3e44-41e0-8b97-48e5d9bddbb9`
- **Stages (Fases do Funil):**
  - `1b8d5cdb-469b-4c5c-865b-0ba70415a4eb` - Base (Tipo: BASE)
  - `890d37ef-837c-43f7-a13b-cf124f2e5115` - Onboarding (Tipo: CUSTOM)
  - `7ce24330-75ef-4cfd-ac66-92af10eea516` - On going (Tipo: CUSTOM)
  - `9bb6ab52-660c-451b-912c-803f5ec06f36` - Sucesso (Tipo: CLOSING)

### Origem: Cartão recusado (Grupo: ENAM - 90 Dias)
- **Origin ID:** `3421d140-2e1a-41f7-bc78-cbe55e12564b`
- **Stages (Fases do Funil):**
  - `5232689d-33b2-46a8-b361-5446669991b5` - Base (Tipo: BASE)
  - `61e4e501-d03a-4301-bf10-e112bba1a149` - Prospecção (Tipo: CUSTOM)
  - `4b7fa313-30c2-40fc-b039-adb7e92c37ba` - Conexão (Tipo: CUSTOM)
  - `4a089c3f-f0cc-44eb-ab2e-a38ccf5a832a` - Aguardando compra (Tipo: CUSTOM)
  - `789ff3c0-8ff5-4a6d-ac8d-8a75652092cb` - Fechado (Tipo: CLOSING)

### Origem: Inbound Concursos (Grupo: Inbound Whatsapp)
- **Origin ID:** `33c7898f-029f-4fe9-af94-f4e3c27bca48`
- **Stages (Fases do Funil):**
  - `b69ef3d9-7dc0-4bd4-892a-e03434e16dad` - Base (Tipo: BASE)
  - `20cbfcb9-5973-4318-ae08-b16484595bee` - Fechado (Tipo: CLOSING)

### Origem: Abandono de carrinho (Grupo: ENAM - ANUAL)
- **Origin ID:** `2e71c675-f603-4b19-a835-a83d60795b42`
- **Stages (Fases do Funil):**
  - `7fb0d2b0-467f-4ca2-9d1c-ea0801f782ce` - Base (Tipo: BASE)
  - `3f178065-3389-4a68-8948-40332088e283` - Prospecção (Tipo: CUSTOM)
  - `1b6260e7-0d16-40a8-972a-71958e9adfa3` - Conexão (Tipo: CUSTOM)
  - `f01b7a76-2e19-4bc4-975c-5f065d015c8c` - Aguardando compra (Tipo: CUSTOM)
  - `44c49d57-7f99-4f74-a5f3-89b898dcd59f` - Fechado (Tipo: CLOSING)

### Origem: Lista Geral - 60D (Grupo: VDE 60D - OAB 1F)
- **Origin ID:** `2d74fdeb-1040-4161-bfa8-f268a0858f81`
- **Stages (Fases do Funil):**
  - `c5c7146a-2aca-4977-a1bd-4ceff08e2bc6` - Base (Tipo: BASE)
  - `0716ad98-ed1b-4638-8206-628f513860fa` - Agendamento (Tipo: CUSTOM)
  - `25042ab1-3b5e-4cd1-817a-adc063829054` - Prospecção (Tipo: CUSTOM)
  - `9894dad3-a173-4b51-9324-eb5644afa51f` - Follow UP 1 (Tipo: CUSTOM)
  - `f2b3a36f-7cae-4e33-8ba5-1532dda319ae` - Follow UP 2 (Tipo: CUSTOM)
  - `c1a0ed93-a910-4657-abcd-6146830b40a5` - Encerramento (Tipo: CUSTOM)
  - `28ad1c89-bf30-4a3c-bcf4-27fdf42039cf` - Conexão (Tipo: CUSTOM)
  - `0e0fed9c-cd86-4b3f-be83-e2777ad662c0` - Aguardando compra (Tipo: CUSTOM)
  - `e63efb65-1524-4a4d-aa4b-6e29e2845031` - Fechado (Tipo: CLOSING)

### Origem: VDE 90 D - OAB 45 (Grupo: OAB - Primeira Fase)
- **Origin ID:** `2ca39757-6456-4ff6-813c-e6150b5ce716`
- **Stages (Fases do Funil):**
  - `8a2fad03-02a9-480c-af62-065444dfbc79` - Base (Tipo: BASE)
  - `acdc5a8c-a716-4fd3-a07d-673fd7ae5c54` - Prospecção (Tipo: CUSTOM)
  - `369a47b8-683b-4afe-972c-fbb35238fba1` - Conexão (Tipo: CUSTOM)
  - `4411c66f-4f25-46f5-95ba-6f019d596ba2` - Aguardando Decisão (Tipo: CUSTOM)
  - `e625a87a-0573-44ef-8908-7d6b64a4bf1e` - Aguardando Compra (Tipo: CUSTOM)
  - `81c6e808-db14-47ba-984b-5fe3e51e4bb2` - Fechado (Tipo: CLOSING)

### Origem: Funil de Teste (Grupo: Geral)
- **Origin ID:** `2b47667b-9802-4a16-a447-03e033cbb76d`
- **Stages (Fases do Funil):**
  - `ec6e7df7-4b4e-4be5-9dd9-8d7057e5b70e` - Base (Tipo: BASE)
  - `bdcaad88-210e-4fff-aa03-aa2ee61b39a9` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex ativas (Grupo: OAB - 1º Fase ANUAL)
- **Origin ID:** `29e20069-b000-41ef-b9d9-d60050616150`
- **Stages (Fases do Funil):**
  - `fd0baaf1-8b6f-4a2f-bfab-11f24b466209` - Base (Tipo: BASE)
  - `5dc80db7-d7fb-42de-9fc7-12dc1d134f8a` - On going (Tipo: CUSTOM)
  - `3c6dc24a-926a-4e2a-99bc-5d9b56306448` - Sucesso (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex canceladas (Grupo: OAB - 1º Fase ANUAL)
- **Origin ID:** `29acaf93-d9c6-41f7-81a0-ed4d00cad4e7`
- **Stages (Fases do Funil):**
  - `6b32aaf7-b64a-495b-b4d3-b4ba297b8604` - Base (Tipo: BASE)
  - `f1f6f7ef-694c-4b13-8977-9c36d51e253a` - Sondagem (Tipo: CUSTOM)
  - `dea27a6e-1bca-443c-b95a-3383d24efb92` - Em contato (Tipo: CUSTOM)
  - `9fce765d-8a98-4588-a65c-8989e49019a9` - Venda realizada (Tipo: CLOSING)

### Origem: Cartão recusado (Grupo: Hotmart - 6384818)
- **Origin ID:** `26fa2901-e0b3-4f9f-8d9a-d2137714daac`
- **Stages (Fases do Funil):**
  - `d7fdaec9-ba50-4e75-8d01-d6c834bc879b` - Base (Tipo: BASE)
  - `174477d9-4fd9-4d4f-8ec8-9c43042ed9d8` - Prospecção (Tipo: CUSTOM)
  - `8dc561e1-80a8-4772-b7fd-a71854735017` - Conexão (Tipo: CUSTOM)
  - `014e79e2-9466-4574-8c57-eaaf47cf6d45` - Aguardando compra (Tipo: CUSTOM)
  - `d8f0e2dd-f1a7-4ec6-8ed4-60906d17e360` - Fechado (Tipo: CLOSING)

### Origem: Reembolso/Chargeback (Grupo: Hotmart - 6979776)
- **Origin ID:** `25e3b57d-d991-4607-9aa1-bde3aa3ebba0`
- **Stages (Fases do Funil):**
  - `8ebea989-9485-4f3a-9d3e-eab67a23dbfd` - Base (Tipo: BASE)
  - `a48cadff-83e2-4575-b2c4-86ffea49114e` - Sondagem (Tipo: CUSTOM)
  - `e5e4ebc5-345b-471c-bd3f-023293402f0e` - Em contato (Tipo: CUSTOM)
  - `14971eb0-aa52-4827-9b56-6d235ed5cbb9` - Fechado (Tipo: CLOSING)

### Origem: Compras em aberto (Grupo: Hotmart - 6384818)
- **Origin ID:** `24952d3b-08cd-4b69-8079-0cf248bb023c`
- **Stages (Fases do Funil):**
  - `fda46edd-046d-4e97-a732-89c8f92842d4` - Base (Tipo: BASE)
  - `2215dce5-e756-460f-941f-13dbe1217f5f` - Prospecção (Tipo: CUSTOM)
  - `7d5e9c28-c162-4738-908b-e8aed0904086` - Conexão (Tipo: CUSTOM)
  - `81635165-c864-4685-ade7-a1c45f837e46` - Aguardando compra (Tipo: CUSTOM)
  - `d844a15a-2f6d-4236-ac97-62115db6884b` - Fechado (Tipo: CLOSING)

### Origem: Leads 180D (Grupo: Active Campaign)
- **Origin ID:** `24693485-cc45-40bd-aa01-4be4ac002a92`
- **Stages (Fases do Funil):**
  - `76502cb5-45a5-4a23-a64a-61b94fec4476` - Base (Tipo: BASE)
  - `45bc4e21-3ca1-4b63-9358-21f42cda3ffd` - Prospecção (Tipo: CUSTOM)
  - `4d848dcf-7f32-44ef-b350-39009a3ad059` - Conexão (Tipo: CUSTOM)
  - `b423f1e9-9cd8-4bca-9a9a-281fd885c3da` - Aguardando Compra (Tipo: CUSTOM)
  - `b0432a1d-b147-41f9-8d46-db7a78381d8a` - Fechado (Tipo: CLOSING)

### Origem: VDE 180D - OAB 47 (Grupo: OAB - Primeira Fase)
- **Origin ID:** `23e802b3-a5ab-41fb-9e97-1084e852061d`
- **Stages (Fases do Funil):**
  - `b21abfb1-dd7a-4bab-a862-3741e73360a7` - Base (Tipo: BASE)
  - `472aad31-c605-4a5d-bc92-970ecd48094c` - Prospecção (Tipo: CUSTOM)
  - `b5c93117-5fc9-4bf9-90bd-812e0329af5f` - Agendamento (Tipo: CUSTOM)
  - `8753b459-5cac-4465-806a-bf3eeafe6ea6` - Follow UP 1 (Tipo: CUSTOM)
  - `9e25095c-c707-404a-9adf-f0861fe4e151` - Follow Up 2 (Tipo: CUSTOM)
  - `9213157c-ec7e-4005-a5c0-91c3fdad027a` - Encerramento (Tipo: CUSTOM)
  - `32b0afb9-6dfd-4879-920b-46d94066e130` - Conexão (Tipo: CUSTOM)
  - `485c6990-9170-4fc0-82db-408dbe3ceef7` - Aguardando Compra (Tipo: CUSTOM)
  - `e860ec63-e7c6-40b0-8b0a-0f369f45c723` - Fechado (Tipo: CLOSING)

### Origem: Cronograma 90 Dias (Grupo: ENAM - Preparatório)
- **Origin ID:** `2362b94d-dbca-4f49-94e2-53c1db222aef`
- **Stages (Fases do Funil):**
  - `11f7b2ae-63fb-4563-a7e7-4c61d75dd9fa` - Base (Tipo: BASE)
  - `5fc27007-9223-4fb8-83d4-d7b111e0e017` - Fechado (Tipo: CLOSING)

### Origem: VDE 120D - OAB 46 - (Participaram da Nocaute) (Grupo: OAB - Primeira Fase)
- **Origin ID:** `235ab7db-4d6f-4ca9-8236-d1f0da840a4d`
- **Stages (Fases do Funil):**
  - `b143f188-81ff-48cc-b08b-1faadbc194fd` - Base (Tipo: BASE)
  - `e8954dc2-d5b5-4b42-8712-14bef3d7689f` - Fechado (Tipo: CLOSING)

### Origem: Reembolso/Chargeback (Grupo: OAB - Segunda Fase)
- **Origin ID:** `22368f5d-f225-429c-aa86-10142724d6c6`
- **Stages (Fases do Funil):**
  - `3c51ade0-ad53-49ed-8f56-f1cbb8e21cfb` - Base (Tipo: BASE)
  - `2e75732b-05cb-4430-b9fb-8d3fe02d75f8` - Sondagem (Tipo: CUSTOM)
  - `0d97b721-973a-45a1-bafb-ce77e57b9020` - Em contato (Tipo: CUSTOM)
  - `e58b6c43-5294-4de2-9aa4-5053cbc580e8` - Fechado (Tipo: CLOSING)

### Origem: Compras aprovadas (Grupo: Hotmart - 6979776)
- **Origin ID:** `2184ac6a-086d-4f58-a5fa-02e13522c305`
- **Stages (Fases do Funil):**
  - `f1639dd5-a813-4747-a4c7-b7d4b219fdee` - Base (Tipo: BASE)
  - `d075083c-71da-4149-b1a4-f9525e7d0668` - Onboarding (Tipo: CUSTOM)
  - `5545ab10-badc-43c5-8a26-ffb06483be44` - On going (Tipo: CUSTOM)
  - `4a6ddbdd-ce4e-4284-b5a5-47331a88ea81` - Sucesso (Tipo: CLOSING)

### Origem: Cartão recusado (Grupo: OAB - 1º Fase ANUAL)
- **Origin ID:** `20c9e726-d5b2-46a5-9494-ef91b43492a8`
- **Stages (Fases do Funil):**
  - `0e66004a-9db7-43cb-ac26-c1e1b2f5b063` - Base (Tipo: BASE)
  - `81720ff8-8353-4cfa-8780-0bb63c162b10` - Prospecção (Tipo: CUSTOM)
  - `74328b56-232d-4c6f-9e02-516ee7b55f16` - Aguardando compra (Tipo: CUSTOM)
  - `4b8be796-a6be-4968-84b7-5705608d62a3` - Conexão (Tipo: CUSTOM)
  - `1ba9e0df-b083-429f-8244-e1176bad23d0` - Antes de Finalizar (Tipo: CUSTOM)
  - `f1f30476-736f-4a43-aa5f-4307bf47901d` - Finalizando (Tipo: CUSTOM)
  - `fe14794f-c620-457a-99c0-3e4f24aa6c9f` - Fechado (Tipo: CLOSING)

### Origem: Compras em aberto (Grupo: ENAM - 90 Dias)
- **Origin ID:** `20c2abb4-2912-4992-bdd0-df05d24dabd9`
- **Stages (Fases do Funil):**
  - `f5c171c0-8e73-431e-9ff2-a9d3b5464867` - Base (Tipo: BASE)
  - `fd38a2e5-3689-4462-8dad-d2c2c120b367` - Prospecção (Tipo: CUSTOM)
  - `9c0d824a-c9ea-47f3-9862-2e4a185efd61` - Conexão (Tipo: CUSTOM)
  - `66397d3e-a2ed-4e0a-8c1e-31c60502d5d9` - Aguardando compra (Tipo: CUSTOM)
  - `40a5a49e-0c23-48f5-a8f5-d8e5b5f9fbb2` - Fechado (Tipo: CLOSING)

### Origem: Compras aprovadas (Grupo: OAB - Primeira Fase)
- **Origin ID:** `1f47fd00-3636-4325-81a3-d99b360c752b`
- **Stages (Fases do Funil):**
  - `2d658fb5-b5fd-4ca7-8cd3-5aeb0c7be764` - Base (Tipo: BASE)
  - `07d0d649-0337-4b6a-a210-51147b66fb60` - Onboarding (Tipo: CUSTOM)
  - `77f80529-02a8-4ab8-b43d-a174335e2aeb` - On going (Tipo: CUSTOM)
  - `9f65257b-2f57-453c-9020-e586c088bb30` - Sucesso (Tipo: CLOSING)

### Origem: Inbound Whatsapp (Grupo: VDE Concursos)
- **Origin ID:** `1c8fa2e9-bdad-4a8c-87b2-839b4feab75a`
- **Stages (Fases do Funil):**
  - `7ed6d505-940f-4689-9c0b-d786cb96d510` - Base (Tipo: BASE)
  - `2f608d34-bbc7-4755-8c5b-b4e728c4d026` - Prospecção (Tipo: CUSTOM)
  - `1eaa159c-2db4-4a0a-b3c4-f5590f09b402` - Conexão (Tipo: CUSTOM)
  - `23f5df00-52e8-4404-9171-0fcfe956266f` - Aguardando compra (Tipo: CUSTOM)
  - `1003a8e7-1271-47b3-b18e-efc47141add0` - Fechado (Tipo: CLOSING)

### Origem: Reembolso/Chargeback (Grupo: Hotmart - 6384818)
- **Origin ID:** `1b768441-cc50-48a5-841f-b246d5c27875`
- **Stages (Fases do Funil):**
  - `e849330f-f867-4cb0-9d64-7cfa2df0c568` - Base (Tipo: BASE)
  - `d699b7d6-9aa5-42f8-9e1c-b7192d964c06` - Sondagem (Tipo: CUSTOM)
  - `ddb88204-ce64-43ba-adef-30961d76eff1` - Em contato (Tipo: CUSTOM)
  - `cd4d836b-5838-417c-b72e-ffd2f263227b` - Fechado (Tipo: CLOSING)

### Origem: LG - ENAM 90 DIAS (Grupo: ENAM - 90 Dias)
- **Origin ID:** `1a055f3d-066c-42c5-b2b9-d9944db0e4af`
- **Stages (Fases do Funil):**
  - `d045f815-1d4e-48b6-91e3-d91794b9ae0e` - Base Fria (Tipo: BASE)
  - `c5b2f968-880b-4483-a881-d17c043c52ef` - Leads Quentes URGENTE (Tipo: CUSTOM)
  - `642ad540-c609-4211-99ba-a23dae27fe5d` - Agendamentos (Tipo: CUSTOM)
  - `77dd3ad3-a636-4b07-b373-615df82136fe` - Prospecção (Tipo: CUSTOM)
  - `939e9aac-437a-4388-a645-61e3c0aead11` - Follow UP 1 (Tipo: CUSTOM)
  - `a894b655-ea93-4365-b4f0-386c9ba601c1` - Follow UP 2 (Tipo: CUSTOM)
  - `97d631df-32a3-4ed0-972f-3c283259c51e` - Encerramento (Tipo: CUSTOM)
  - `299454e3-d400-4ef8-8e4f-e2b5334173b4` - Conexão (Tipo: CUSTOM)
  - `3d085699-414c-4428-9159-7ddf17c4ad80` - Aguardando compra (Tipo: CUSTOM)
  - `6dde6adf-113f-4baf-a42d-171ed70ef66e` - Fechado (Tipo: CLOSING)

### Origem: Reembolso/Chargeback (Grupo: ENAM - 90 Dias)
- **Origin ID:** `161b191d-c48b-4fce-9f2e-9cfb49ff268a`
- **Stages (Fases do Funil):**
  - `c3a88e20-2e34-418a-9290-70a762cebce5` - Base (Tipo: BASE)
  - `295cc54f-7e25-4b60-8f04-02a277cac5fb` - Sondagem (Tipo: CUSTOM)
  - `3d3d2b5d-3140-4328-b96a-9f3f8f48832a` - Em contato (Tipo: CUSTOM)
  - `5aa2d8cb-f10d-4ed3-9d0b-eb4af71f27f0` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex ativas (Grupo: CJ - Ciclo Prioritário)
- **Origin ID:** `1613f6b0-5545-4f8f-ab82-ff330db24d9c`
- **Stages (Fases do Funil):**
  - `150dd8bf-ea94-47e7-9cb9-05806aa148c4` - Base (Tipo: BASE)
  - `c6e65512-6967-4b9f-9a55-f05bdfaa63dc` - On going (Tipo: CUSTOM)
  - `1134ed32-ca0f-4758-bd19-5b4c832b848e` - Sucesso (Tipo: CLOSING)

### Origem: LG - ANUAL (Grupo: OAB - 1º Fase ANUAL)
- **Origin ID:** `14bc535c-a693-4c51-a438-7071e703a5ea`
- **Stages (Fases do Funil):**
  - `ff2e84b0-9162-4520-8edb-4c7a9399c073` - Base (Tipo: BASE)
  - `d793a0cc-f1f9-429e-afe0-c08c18267270` - Prospecção (Tipo: CUSTOM)
  - `be302128-c44a-4314-bd8d-4e8d5767c74f` - Conexão (Tipo: CUSTOM)
  - `4e7f4b16-eac0-4863-862f-0e17f54ac466` - Aguardando compra (Tipo: CUSTOM)
  - `3003ad5a-f03f-4413-bcf0-9cbfcfcd5708` - Fechado (Tipo: CLOSING)

### Origem: Pós Venda (Grupo: Novos Leads)
- **Origin ID:** `11278790-a423-41f0-99c8-07225fdd8910`
- **Stages (Fases do Funil):**
  - `898493e0-e24b-46b6-8d56-83f30443b51a` - Base (Tipo: BASE)
  - `00379783-2ac5-4da9-a3b5-59514cbcc1c9` - Fechado (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex ativas (Grupo: Hotmart - 6979776)
- **Origin ID:** `0f7021f9-fe0e-4694-8b5c-2fd96bdcb383`
- **Stages (Fases do Funil):**
  - `79c8597b-b2d8-4e22-b51b-0de403d455c8` - Base (Tipo: BASE)
  - `ccaf3a95-89c1-4df5-9ddb-1abf12f80f61` - On going (Tipo: CUSTOM)
  - `d3e132bd-4ce2-4c5d-ac29-4389f02f9813` - Sucesso (Tipo: CLOSING)

### Origem: Assinaturas/Parcelex em atraso (Grupo: OAB - Segunda Fase)
- **Origin ID:** `0de9a72c-3f01-4a7f-96e5-c2f8a9e1d827`
- **Stages (Fases do Funil):**
  - `0e51206f-6b5b-4f4f-9003-d09a3846d0b9` - Base (Tipo: BASE)
  - `a82acb0f-e3bc-473c-82ca-d249c0ee49a4` - Sondagem (Tipo: CUSTOM)
  - `be55e380-e7bc-4ae0-9375-e35418988080` - Em contato (Tipo: CUSTOM)
  - `d66a55e0-be7c-4ada-bebd-0f173677c531` - Fechado (Tipo: CLOSING)

### Origem: Compras expiradas (Grupo: ENAM - 90 Dias)
- **Origin ID:** `0c8f84f2-39e5-4a5f-b9ed-c55ca476c311`
- **Stages (Fases do Funil):**
  - `e175e61f-4f52-46e1-a77f-187642984bd1` - Base (Tipo: BASE)
  - `7a05fe4d-9749-4f9c-b97c-05302ef7e5f5` - Prospecção (Tipo: CUSTOM)
  - `a8460cd9-9df9-489c-9ae1-b72d1e43aa23` - Conexão (Tipo: CUSTOM)
  - `739fdf81-f4ea-4378-88a3-64796987e3ae` - Aguardando compra (Tipo: CUSTOM)
  - `2e8cbac7-c47a-4e2d-b3b3-5ddf760c854c` - Fechado (Tipo: CLOSING)

### Origem: Compras em aberto (Grupo: VDE 60D - OAB 1F)
- **Origin ID:** `0b321c23-0217-486f-9e7c-488252343dda`
- **Stages (Fases do Funil):**
  - `187a0d2a-1a56-44f2-aeb2-66acb94cd17e` - Base (Tipo: BASE)
  - `2b88f9ea-9036-4c24-9a61-dea670e75036` - Prospecção (Tipo: CUSTOM)
  - `723f2fc5-7eee-4d4d-961a-47c8f5b7726f` - Conexão (Tipo: CUSTOM)
  - `bf70f15c-4187-465d-ab6b-dba24abf35c2` - Aguardando compra (Tipo: CUSTOM)
  - `bacfe700-b4eb-4e9b-95ef-545a8a36f8fa` - Fechado (Tipo: CLOSING)

### Origem: Abandono de carrinho (Grupo: Hotmart - 6979776)
- **Origin ID:** `08d5b56e-7974-46aa-b777-ef0bf15f897b`
- **Stages (Fases do Funil):**
  - `9eb1ac4f-b4ba-44ca-a83c-0a31d61e37a7` - Base (Tipo: BASE)
  - `4d74bf42-d7d9-4dfb-bf04-183aada163a7` - Prospecção (Tipo: CUSTOM)
  - `d62f3088-3bf2-4de5-ac0c-7669d47a50ec` - Conexão (Tipo: CUSTOM)
  - `a2cde117-5584-4514-838f-384c551fc213` - Aguardando compra (Tipo: CUSTOM)
  - `b81d1399-5107-4e9f-bfcf-2cde89ab02dc` - Fechado (Tipo: CLOSING)

### Origem: N8N (Grupo: N8N)
- **Origin ID:** `08449d69-ba48-4a49-9ffb-5f906980b764`
- **Stages (Fases do Funil):**
  - `46f9de4c-fb6a-4984-89a9-3874e9445d32` - Base (Tipo: BASE)
  - `f4fc20a0-bc39-42c8-8f86-33a728bc353f` - Fechado (Tipo: CLOSING)

### Origem: Abandono de carrinho (Grupo: Hotmart - 6384818)
- **Origin ID:** `05770b91-f97c-47c3-bb99-4134b22483ea`
- **Stages (Fases do Funil):**
  - `f1788d71-64c5-4fb8-85f4-e89ebc6b12cb` - Base (Tipo: BASE)
  - `48f14966-9431-4e78-bb64-456bcd6047d2` - Prospecção (Tipo: CUSTOM)
  - `91c7fbe3-b0e5-4a90-bd06-628dd6b532e2` - Conexão (Tipo: CUSTOM)
  - `90704763-eb18-4e9b-8066-fc7e224ed4c1` - Aguardando compra (Tipo: CUSTOM)
  - `38f0c92d-c907-4a7a-a2cd-2ed09a8d0560` - Fechado (Tipo: CLOSING)

### Origem: Abandono de carrinho (Grupo: VDE 60D - OAB 1F)
- **Origin ID:** `04c2a193-2750-43d8-9aa2-64e96844948e`
- **Stages (Fases do Funil):**
  - `d177c55f-8436-4eaf-a83f-45486a3321f5` - Base (Tipo: BASE)
  - `85a9614a-f57b-45f9-b97f-d26e048ff7c1` - Prospecção (Tipo: CUSTOM)
  - `eed9b554-c157-474d-8778-aae2950a2d51` - Conexão (Tipo: CUSTOM)
  - `547ee8c6-aa0a-45dd-9b8e-d73c4c3cd09b` - Aguardando compra (Tipo: CUSTOM)
  - `6b30ce49-8299-45cd-a80b-9c3efb12a434` - Fechado (Tipo: CLOSING)

## 3. Validação do POST de Contato
O payload de inserção (apenas name, email e object phone segregado com ddi e number) foi aceito com **Status 201 Created**, validando nossa estrutura para a Task 2.
