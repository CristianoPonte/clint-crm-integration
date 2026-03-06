# Acesso à API do n8n

## Base URL

```bash
https://sisifo.metodovde.com.br/api/v1
```

## Token de API

Use este header em todas as requisições:

```bash
X-N8N-API-KEY: SEU_TOKEN
```

## Uso com variável de ambiente (recomendado)

```bash
export N8N_BASE_URL='https://sisifo.metodovde.com.br/api/v1'
export N8N_API_KEY='SEU_TOKEN'
```

## Teste rápido

```bash
curl "$N8N_BASE_URL/users" \
  --header "X-N8N-API-KEY: $N8N_API_KEY"
```

## Endpoints úteis (GET)

```bash
curl "$N8N_BASE_URL/users" --header "X-N8N-API-KEY: $N8N_API_KEY"
curl "$N8N_BASE_URL/workflows" --header "X-N8N-API-KEY: $N8N_API_KEY"
curl "$N8N_BASE_URL/executions" --header "X-N8N-API-KEY: $N8N_API_KEY"
curl "$N8N_BASE_URL/tags" --header "X-N8N-API-KEY: $N8N_API_KEY"
curl "$N8N_BASE_URL/credentials" --header "X-N8N-API-KEY: $N8N_API_KEY"
```

## Criar workflow (POST)

```bash
curl -X POST "$N8N_BASE_URL/workflows" \
  --header "X-N8N-API-KEY: $N8N_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "Workflow de teste via API",
    "nodes": [],
    "connections": {},
    "settings": {}
  }'
```

## Atualizar workflow (PATCH/PUT)

Substitua `WORKFLOW_ID`:

```bash
curl -X PATCH "$N8N_BASE_URL/workflows/WORKFLOW_ID" \
  --header "X-N8N-API-KEY: $N8N_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "Workflow atualizado via API"
  }'
```

Se o `PATCH` retornar `405`, usar fallback `PUT`:

```bash
curl -X PUT "$N8N_BASE_URL/workflows/WORKFLOW_ID" \
  --header "X-N8N-API-KEY: $N8N_API_KEY" \
  --header "Content-Type: application/json" \
  --data @workflow.json
```

## Ativar workflow

```bash
curl -X POST "$N8N_BASE_URL/workflows/WORKFLOW_ID/activate" \
  --header "X-N8N-API-KEY: $N8N_API_KEY"
```

## Deletar workflow (DELETE)

```bash
curl -X DELETE "$N8N_BASE_URL/workflows/WORKFLOW_ID" \
  --header "X-N8N-API-KEY: $N8N_API_KEY"
```

## Observações

- O endpoint `/projects` pode retornar `403 Forbidden` por limitação de licença.
- Para webhooks de producao funcionarem, o node Webhook deve ter `webhookId` persistido no JSON.
- Nao depender de `active` no body de create/update; ativar por endpoint dedicado.
