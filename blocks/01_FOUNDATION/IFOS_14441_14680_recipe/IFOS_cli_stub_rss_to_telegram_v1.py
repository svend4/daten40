#!/usr/bin/env python3
"""
IFOS CLI stub for recipe.rss_to_telegram.digest_v1
Usage:
  python IFOS_cli_stub_rss_to_telegram_v1.py --rss-url ... --chat-id ... --dry-run
Secrets:
  TELEGRAM_BOT_TOKEN in env
"""
import os, argparse, json, sys, datetime

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rss-url", required=True)
    ap.add_argument("--chat-id", required=True)
    ap.add_argument("--max-items", type=int, default=5)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    token = os.getenv("TELEGRAM_BOT_TOKEN","")
    rss_url = args.rss_url
    chat_id = args.chat_id

    # TODO: fetch RSS, track last_seen in a local state file
    digest_text = f"(stub) Digest from {rss_url} (max_items={args.max_items})"

    evidence = {
        "recipe_id":"recipe.rss_to_telegram.digest_v1",
        "ts": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
        "dry_run": bool(args.dry_run),
        "preview": digest_text[:2000],
        "status":"PASS_DRY_RUN" if args.dry_run else "NOT_SENT_STUB"
    }
    print(json.dumps(evidence, ensure_ascii=False, indent=2))

    if args.dry_run:
        return 0

    if not token:
        print("Missing TELEGRAM_BOT_TOKEN", file=sys.stderr)
        return 2

    # NOTE: real sending omitted in stub to avoid accidental messages
    print("[TODO] Implement Telegram sendMessage call safely.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
