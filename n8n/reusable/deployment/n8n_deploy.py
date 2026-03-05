#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Variavel de ambiente obrigatoria ausente: {name}")
    return value


class N8NClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "X-N8N-API-KEY": api_key,
                "Content-Type": "application/json",
            }
        )

    def request(self, method: str, path: str, **kwargs) -> Any:
        url = f"{self.base_url}{path}"
        response = self.session.request(method=method, url=url, timeout=30, **kwargs)
        if not response.ok:
            body = response.text[:600]
            raise RuntimeError(
                f"Erro na API n8n: {method} {path} -> {response.status_code} | {body}"
            )
        if response.status_code == 204 or not response.text:
            return {}
        return response.json()

    def list_entities(self, path: str, limit: int = 250) -> list[dict[str, Any]]:
        cursor = None
        results: list[dict[str, Any]] = []

        while True:
            params = {"limit": limit}
            if cursor:
                params["cursor"] = cursor

            response = self.request("GET", path, params=params)
            results.extend(response.get("data", []))
            cursor = response.get("nextCursor")
            if not cursor:
                break

        return results

    def find_workflow_by_name(self, name: str) -> dict[str, Any] | None:
        workflows = self.list_entities("/workflows")
        for workflow in workflows:
            if workflow.get("name") == name:
                return workflow
        return None


def load_workflow(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    required_keys = ["name", "nodes", "connections", "settings"]
    missing = [k for k in required_keys if k not in payload]
    if missing:
        raise RuntimeError(f"Workflow invalido em {path}: faltando {missing}")
    return payload


def deploy_workflow(client: N8NClient, payload: dict[str, Any]) -> dict[str, str]:
    name = payload["name"]
    existing = client.find_workflow_by_name(name)

    body = {
        "name": payload["name"],
        "nodes": payload["nodes"],
        "connections": payload["connections"],
        "settings": payload.get("settings", {}),
    }

    if existing:
        workflow_id = existing["id"]
        try:
            client.request("PATCH", f"/workflows/{workflow_id}", json=body)
        except RuntimeError as exc:
            if " 405 " not in str(exc):
                raise
            client.request("PUT", f"/workflows/{workflow_id}", json=body)
        return {"name": name, "id": workflow_id, "action": "updated"}

    created = client.request("POST", "/workflows", json=body)
    workflow_id = created.get("id") or created.get("data", {}).get("id")
    if not workflow_id:
        raise RuntimeError(f"Nao foi possivel identificar ID do workflow criado: {name}")

    return {"name": name, "id": workflow_id, "action": "created"}


def run_baseline_check(client: N8NClient) -> dict[str, int]:
    users = client.list_entities("/users")
    workflows = client.list_entities("/workflows")
    credentials = client.list_entities("/credentials")
    tags = client.list_entities("/tags")
    return {
        "users": len(users),
        "workflows": len(workflows),
        "credentials": len(credentials),
        "tags": len(tags),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Deploy de workflows n8n (create/update) e baseline check."
    )
    parser.add_argument(
        "workflow_files",
        nargs="*",
        help="Arquivos JSON de workflow versionados no repositorio.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Executa apenas validacao de baseline (users/workflows/credentials/tags).",
    )
    args = parser.parse_args()

    try:
        base_url = require_env("N8N_BASE_URL")
        api_key = require_env("N8N_API_KEY")
        client = N8NClient(base_url=base_url, api_key=api_key)

        baseline = run_baseline_check(client)
        print(
            "Baseline n8n -> users: {users}, workflows: {workflows}, credentials: {credentials}, tags: {tags}".format(
                **baseline
            )
        )

        if args.check_only:
            return 0

        if not args.workflow_files:
            raise RuntimeError(
                "Informe pelo menos um arquivo de workflow ou use --check-only."
            )

        for workflow_file in args.workflow_files:
            wf_path = Path(workflow_file).expanduser().resolve()
            payload = load_workflow(wf_path)
            result = deploy_workflow(client, payload)
            print(
                f"{result['action'].upper()}: {result['name']} (id={result['id']})"
            )

        return 0
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Falha: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
