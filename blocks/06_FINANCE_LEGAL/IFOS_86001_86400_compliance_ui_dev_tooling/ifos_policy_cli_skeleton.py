
#!/usr/bin/env python3
"""IFOS Policy CLI — skeleton.

This is a non-functional scaffold to lock the CLI contract.
"""
import argparse, json, sys

def main():
    p = argparse.ArgumentParser(prog="ifos-policy")
    sub = p.add_subparsers(dest="cmd", required=True)

    lint = sub.add_parser("lint")
    lint.add_argument("path")

    vpack = sub.add_parser("validate-pack")
    vpack.add_argument("target")

    sim = sub.add_parser("simulate")
    sim.add_argument("--bundle", required=True)
    sim.add_argument("--context", required=True)

    exp = sub.add_parser("explain")
    exp.add_argument("--step", required=True)
    exp.add_argument("--context", required=True)

    ev = sub.add_parser("evidence")
    ev_sub = ev.add_subparsers(dest="evcmd", required=True)
    ev_sub.add_parser("status")

    args = p.parse_args()
    # TODO: wire to API / local engine
    print(json.dumps({"cmd": args.cmd, "args": vars(args)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
