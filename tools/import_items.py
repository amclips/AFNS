#!/usr/bin/env python3
"""Write AFNS markdown articles from a JSON list of research items.
Usage: python3 tools/import_items.py items.json
Each item: {"desk","slug","title","date","summary","status"(optional),"featured"(bool),
            "key_points":[...], "sources":[["Title","URL"],...], "body":"markdown"}
"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
q = lambda s: '"' + str(s).replace('"', '\\"') + '"'
for it in json.loads(Path(sys.argv[1]).read_text()):
    fm = ["---", f"title: {q(it['title'])}", f"desk: {it['desk']}", f"date: {it['date']}", f"summary: {q(it['summary'])}"]
    if it.get("status"): fm.append(f"status: {q(it['status'])}")
    if it.get("featured"): fm.append("featured: true")
    if it.get("desk_lead"): fm.append("desk_lead: true")
    if it.get("key_points"): fm += ["key_points:"] + [f"  - {k}" for k in it["key_points"]]
    fm += ["sources:"] + [f"  - {t} | {u}" for t, u in it["sources"]] + ["---", ""]
    p = ROOT / "content" / it["desk"] / f"{it['slug']}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(fm) + "\n" + it["body"].strip() + "\n", encoding="utf-8")
    print("wrote", p.relative_to(ROOT))
