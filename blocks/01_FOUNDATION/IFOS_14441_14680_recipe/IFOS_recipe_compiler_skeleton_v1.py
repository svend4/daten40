# IFOS Recipe Compiler Skeleton v1
# Reads a recipe JSON and generates target stubs (Make/n8n/WP/CLI).
# MVP: produce illustrative artifacts + notes, not vendor-perfect exports.

from __future__ import annotations
import json, os, argparse, datetime
from typing import Dict, Any, List

def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def compile_make_stub(recipe: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": f"{recipe['title']} (IFOS stub)",
        "recipe_id": recipe["recipe_id"],
        "generated_at": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
        "notes": [
            "Stub only: replace with real Make blueprint format.",
            "Inputs and secrets are placeholders."
        ],
        "modules": [{"id": i+1, "type": "action", "uses": s.get("uses",""), "kind": s["kind"]}
                    for i, s in enumerate(recipe["steps"])],
        "links": [{"from": i+1, "to": i+2} for i in range(len(recipe["steps"])-1)]
    }

def compile_n8n_stub(recipe: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": f"{recipe['title']} (IFOS stub)",
        "recipe_id": recipe["recipe_id"],
        "generated_at": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
        "notes": ["Stub only: replace with real n8n workflow format."],
        "nodes": [{"name": s["id"], "type": "action", "uses": s.get("uses",""), "kind": s["kind"]}
                  for s in recipe["steps"]],
        "connections": "linear_stub"
    }

def compile_wp_stub(recipe: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "bundle_id": f"bundle.{recipe['recipe_id'].replace('.','_')}",
        "version": recipe.get("version","1.0.0"),
        "recipe_id": recipe["recipe_id"],
        "generated_at": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
        "notes": ["Stub only: WP bundle requires install plan & hooks."],
        "install_plan": [
            {"step": "Create plugin", "how": "Implement steps as WP cron/webhook."},
            {"step": "Configure secrets", "how": "Use WP secret storage."},
            {"step": "Run evidence", "how": "dry-run preview + test chat/sheet."}
        ]
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recipe", required=True)
    ap.add_argument("--out_dir", required=True)
    args = ap.parse_args()

    recipe = load_json(args.recipe)
    out = args.out_dir
    os.makedirs(out, exist_ok=True)

    targets: List[str] = recipe.get("targets", [])
    if "make_blueprint_json" in targets:
        write_json(os.path.join(out, "make_blueprint_stub.json"), compile_make_stub(recipe))
    if "n8n_workflow_json" in targets:
        write_json(os.path.join(out, "n8n_workflow_stub.json"), compile_n8n_stub(recipe))
    if "wp_bundle_manifest_json" in targets:
        write_json(os.path.join(out, "wp_bundle_stub.json"), compile_wp_stub(recipe))

    write_text(os.path.join(out, "README.txt"),
               "Generated stubs. Replace with real exports. Add evidence artifacts after running dry-run.\n")
    print("OK. Generated to", out)

if __name__ == "__main__":
    main()
