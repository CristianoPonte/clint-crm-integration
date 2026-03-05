# Acesso à API do n8n

## Base URL

```bash
http://54.232.226.241:5678/api/v1
```

## Token de API

Use este header em todas as requisições:

```bash
X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNDFkN2YyYi1jNDNhLTQyNWYtOGZjOS0xMzc4MGY0MzY0ODkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiZmI5MDA0YWQtZGI1MS00ZjJjLWIwNTUtZGM0NGJkZDQ3MDJiIiwiaWF0IjoxNzcyNzM2Nzg4LCJleHAiOjE3NzUyNzE2MDB9.KlbvupAVPgHU4GRrA5DT6chxc4aCmYI6In6rBjsX_vY
```

## Teste rápido

```bash
curl http://54.232.226.241:5678/api/v1/users \
  --header 'X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNDFkN2YyYi1jNDNhLTQyNWYtOGZjOS0xMzc4MGY0MzY0ODkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiZmI5MDA0YWQtZGI1MS00ZjJjLWIwNTUtZGM0NGJkZDQ3MDJiIiwiaWF0IjoxNzcyNzM2Nzg4LCJleHAiOjE3NzUyNzE2MDB9.KlbvupAVPgHU4GRrA5DT6chxc4aCmYI6In6rBjsX_vY'
```

## Uso com variável de ambiente (recomendado)

```bash
export N8N_BASE_URL='http://54.232.226.241:5678/api/v1'
export N8N_API_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNDFkN2YyYi1jNDNhLTQyNWYtOGZjOS0xMzc4MGY0MzY0ODkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiZmI5MDA0YWQtZGI1MS00ZjJjLWIwNTUtZGM0NGJkZDQ3MDJiIiwiaWF0IjoxNzcyNzM2Nzg4LCJleHAiOjE3NzUyNzE2MDB9.KlbvupAVPgHU4GRrA5DT6chxc4aCmYI6In6rBjsX_vY'
```

Exemplo de listagem:

```bash
curl "$N8N_BASE_URL/workflows" \
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

## Atualizar workflow (PATCH)

Substitua `WORKFLOW_ID`:

```bash
curl -X PATCH "$N8N_BASE_URL/workflows/WORKFLOW_ID" \
  --header "X-N8N-API-KEY: $N8N_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "Workflow atualizado via API"
  }'
```

## Deletar workflow (DELETE)

Substitua `WORKFLOW_ID`:

```bash
curl -X DELETE "$N8N_BASE_URL/workflows/WORKFLOW_ID" \
  --header "X-N8N-API-KEY: $N8N_API_KEY"
```

## Observações

- O endpoint `/projects` retornou `403 Forbidden` por limitação de licença.
- Os demais endpoints testados responderam `200 OK`.
