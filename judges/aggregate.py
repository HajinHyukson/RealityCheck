import glob, re, sys, os
from collections import defaultdict

VERBS = ["Detect","Expose","Flag","Uncover","Trace","Audit","Challenge","Validate","Reassess",
         "Reclassify","Reconcile","Correct","Update","Realign","Monitor","Diagnose","Interrogate",
         "Surface","Reveal","Stress-test","Prevent"]
N = len(VERBS)
here = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(os.path.join(here, "judge-*.txt")))
borda = defaultdict(int); scores = defaultdict(list); ranks = defaultdict(dict); judges = []
for f in files:
    txt = open(f, encoding="utf-8").read()
    name = re.search(r"JUDGE:\s*(.+)", txt).group(1).strip(); judges.append(name)
    seen = set()
    for line in txt.splitlines():
        m = re.match(r"\s*(\d+)\s*\|\s*([A-Za-z\-]+)\s*\|\s*(\d+)\s*\|", line)
        if not m: continue
        r, v, s = int(m.group(1)), m.group(2), int(m.group(3))
        v = next((x for x in VERBS if x.lower()==v.lower()), None)
        if v is None or v in seen: continue
        seen.add(v); borda[v] += N - r; scores[v].append(s); ranks[v][name] = r
    missing = set(VERBS) - seen
    if missing: print(f"WARNING {name}: missing {sorted(missing)}", file=sys.stderr)
order = sorted(VERBS, key=lambda v: (-borda[v], -sum(scores[v])/max(1,len(scores[v]))))
short = {j: j.split()[0] for j in judges}
print("| Rank | Verb | Borda | Avg score | " + " | ".join(short[j] for j in judges) + " |")
print("|---|---|---|---|" + "---|"*len(judges))
for i, v in enumerate(order, 1):
    avg = sum(scores[v])/max(1,len(scores[v]))
    print(f"| {i} | {v} | {borda[v]} | {avg:.1f} | " + " | ".join(str(ranks[v].get(j,'-')) for j in judges) + " |")
