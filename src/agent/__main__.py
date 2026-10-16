import argparse
import json
import os
import sys

from .gateway import execute
from .llm import ask_model


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m agent")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--intent")
    group.add_argument("--ask")
    parser.add_argument("--approve")
    args = parser.parse_args(argv)

    base_url = os.environ.get("QUIZ_URL", "http://127.0.0.1:8000")
    agent_token = os.environ.get("QUIZ_TOKEN_AGENTE")
    if not agent_token:
        print("Falta QUIZ_TOKEN_AGENTE (el token del agente).", file=sys.stderr)
        return 1

    if args.ask is not None:
        try:
            intent = ask_model(args.ask)
        except (RuntimeError, ValueError, OSError) as exc:
            print(f"No se pudo consultar al modelo: {exc}", file=sys.stderr)
            return 1
        approval = None
        print("El modelo propone:", json.dumps(intent, ensure_ascii=False))
    else:
        try:
            intent = json.loads(args.intent)
        except json.JSONDecodeError as exc:
            print(f"--intent no es JSON válido: {exc}", file=sys.stderr)
            return 1
        approval = args.approve

    result = execute(
        intent, base_url=base_url, agent_token=agent_token, approval=approval,
        human_token=os.environ.get("QUIZ_TOKEN_HUMANO") if approval else None,
        audit_path="agent_audit.jsonl",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] == "approval_required":
        print("\nNo se aplicó nada. Si TÚ apruebas este plan, repite el comando con "
              f"--approve {result['plan']['plan_hash']} (y QUIZ_TOKEN_HUMANO definido).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
