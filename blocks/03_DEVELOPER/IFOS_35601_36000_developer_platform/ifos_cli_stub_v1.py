# ifos_cli_stub_v1.py
from __future__ import annotations
import argparse

def main():
    p=argparse.ArgumentParser(prog="ifos")
    sub=p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("lint")
    sub.add_parser("test")
    sub.add_parser("pack")
    sub.add_parser("run")
    sub.add_parser("publish")
    args=p.parse_args()
    print(f"stub: {args.cmd}")

if __name__=="__main__":
    main()
