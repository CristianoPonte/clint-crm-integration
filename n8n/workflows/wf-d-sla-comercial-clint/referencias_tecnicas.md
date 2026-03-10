# Referencias Tecnicas - WF D SLA Comercial

## Endpoints Clint usados

- `GET /deals?origin_id=<id>&status=OPEN&page=<n>&limit=<n>`
- `GET /origins/<origin_id>`
- `GET /users?limit=100`
- `GET /account/fields`

Base URL: `https://api.clint.digital/v1`

## Integracao Slack implementada

- Tipo de node: `n8n-nodes-base.slack`
- Node de envio: `Slack - Send Message`
- Credencial n8n: `Slack account` (tipo `slackApi`, usada com `authentication=accessToken`)
- Canal operacional: `comercial-bot`
- Manifest do app: `slack_app_manifest.yaml`
- Escopo minimo utilizado: `chat:write` (com `chat:write.public` habilitado no app atual)
- Opcoes aplicadas no node:
  - `otherOptions.appendAttribution = false`
  - `otherOptions.includeLinkToWorkflow = false`
- Formato final da mensagem:
  - titulo em inline code (mrkdwn)
  - bullets por lead
  - separador somente no final de cada mensagem por vendedora

## Estrutura relevante de deal (retornada pela API)

Campos observados:

- `id`
- `origin_id`
- `stage_id`
- `stage` (label textual)
- `status` (`OPEN`, `WON`, `LOST`, etc.)
- `created_at`
- `updated_at`
- `updated_stage_at`
- `latest_meeting_datetime`
- `latest_meeting_link`
- `user` (`id`, `email`, `full_name`)
- `contact` (`id`, `name`, `email`, `phone`, `ddi`, `instagram`)
- `fields` (custom fields do deal)

## Origem e stages do projeto

Origem:

- `bd1bd846-0c87-4acb-b221-d7f8d2089e68` - `Perpetuo Webinario`

Stages:

- `d34e0d52-c401-41dd-907c-80b1d27373ee` - `Lead Cadastrado` (BASE)
- `05a13438-b800-406b-b0c1-fd17a7f52fa6` - `Contato Realizado`
- `582df60d-9cb4-40e5-8a66-365d7b0e8c8a` - `Diagnostico`
- `f58d9353-9454-487a-b7db-b125814ebf97` - `Negociacao`
- `c2d8136e-5451-4294-bf43-d16eca3c52cc` - `Follow-up`
- `b12f6608-ff0a-459f-bcb5-93f1ddb37bbf` - `Fechado` (CLOSING)

## Campos custom de deal ja existentes

Em `GET /account/fields`, entidade `DEAL`:

- `produto`
- `utm_term`
- `sla_status`
- `utm_medium`
- `utm_source`
- `utm_content`
- `lista_origem`
- `utm_campaign`
- `data_importacao`

## Roteamento atual de vendedores

- Fonte de cadastro inicial: `GET /users` da Clint.
- Total cadastrado no workflow/config: `8` usuarias.
- Regra atual: todas as usuarias e fallback `sem_responsavel` enviam para `comercial-bot`.
