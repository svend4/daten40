"""
IFOS Genesis Parser — extracts conceptual steps from founding chat.
Source: chat_export_003.txt (РАЗГОВОР 5/1105)
"""
import re, csv

PHASE_RE = re.compile(r'^#{1,3}\s+Фаза\s+([A-Za-z0-9]+)\s+[—–-]+\s+(.+?)(?:[.。]\s*Шаги\s+(\d+)[–—-]+(\d+))?$')
STEP_RE  = re.compile(r'^(\d{1,5})\)\s+(.{5,})$')

def parse_genesis(filepath: str, max_lines: int = 21000):
    current_phase = "PREFACE"
    rows = []
    prev_step = 0

    with open(filepath, encoding='utf-8', errors='replace') as f:
        for i, line in enumerate(f, 1):
            if i > max_lines:
                break
            line = line.rstrip()

            m = PHASE_RE.match(line)
            if m:
                ph_id, ph_name = m.group(1), m.group(2).strip()
                step_range = f" [{m.group(3)}-{m.group(4)}]" if m.group(3) else ""
                current_phase = f"Фаза {ph_id} — {ph_name}{step_range}"
                continue

            m = STEP_RE.match(line)
            if not m:
                continue

            step_num = int(m.group(1))
            if step_num <= 10 and prev_step > 50:
                continue
            if step_num > 15000:
                continue
            prev_step = step_num

            raw = m.group(2).replace('&quot;', '"').replace('&amp;', '&').rstrip('.')
            parts = re.split(r'\s*→\s*', raw)
            rows.append({
                "phase":       current_phase,
                "step_num":    step_num,
                "action":      parts[0].replace('**', '_').strip(),
                "consequence": parts[1].strip() if len(parts) >= 2 else "",
                "result":      ' → '.join(parts[2:]).strip() if len(parts) >= 3 else "",
            })

    # Deduplicate by step_num
    seen, unique = set(), []
    for r in sorted(rows, key=lambda x: x["step_num"]):
        if r["step_num"] not in seen:
            seen.add(r["step_num"])
            unique.append(r)
    return unique


if __name__ == "__main__":
    import sys
    filepath = sys.argv[1] if len(sys.argv) > 1 else "chat_export_003.txt"
    steps = parse_genesis(filepath)
    print(f"Extracted {len(steps)} steps")
    with open("IFOS_steps_extracted.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["phase","step_num","action","consequence","result"])
        w.writeheader()
        w.writerows(steps)
    print("Saved to IFOS_steps_extracted.csv")
