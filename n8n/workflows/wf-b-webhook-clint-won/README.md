# WF B - Webhook Clint Won

## Objetivo

Receber evento de deal ganho e evoluir para registrar venda e notificar canais externos.

## Arquivos

- `workflow.bootstrap.json`: versao bootstrap da validacao inicial.

## Endpoint de producao

- `POST https://sisifo.metodovde.com.br/webhook/clint-won`

## Entrada esperada

Payload com identificadores do deal/contato:

- `contact_id`
- `deal_id`

Campos opcionais atuais:

- `product_name`
- `product_value`

## Saida

Resposta JSON padrao:

- `status=bootstrap_ready`
- `received_at`
- eco dos principais campos recebidos

## Status

- Bootstrap ativo e validado em producao em `2026-03-06`.
- Retorno de sucesso atual: `HTTP 200` + `status=bootstrap_ready`.
- Proxima fase: Google Sheets + Slack + validacao ponta a ponta do fluxo completo de venda ganha.
