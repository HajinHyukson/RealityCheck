import glob, re, sys, os
from collections import defaultdict
here = os.path.dirname(os.path.abspath(__file__))
labels = dict(l.strip().split("|",1) for l in open(os.path.join(here,"..","statements.txt"), encoding="utf-8") if "|" in l)
IDS = list(labels); N = len(IDS)
files = sorted(glob.glob(os.path.join(here, "judge-*.txt")))
borda = defaultdict(int); scores = defaultdict(list); ranks = defaultdict(dict); judges = []
for f in files:
    txt = open(f, encoding="utf-8").read()
    name = re.search(r"JUDGE:\s*(.+)", txt).group(1).strip(); judges.append(name); seen=set()
    for line in txt.splitlines():
        m = re.match(r"\s*(\d+)\s*\|\s*(S\d+)\s*\|\s*(\d+)\s*\|", line)
        if not m: continue
        r, v, s = int(m.group(1)), m.group(2), int(m.group(3))
        if v not in labels or v in seen: continue
        seen.add(v); borda[v] += N - r; scores[v].append(s); ranks[v][name] = r
    miss = set(IDS)-seen
    if miss: print(f"WARNING {name}: missing {sorted(miss)}", file=sys.stderr)
order = sorted(IDS, key=lambda v: (-borda[v], -sum(scores[v])/max(1,len(scores[v]))))
short = {j: j.split()[0] for j in judges}
print("| Rank | ID | Tagline | Borda | Avg | " + " | ".join(short[j] for j in judges) + " |")
print("|---|---|---|---|---|" + "---|"*len(judges))
for i, v in enumerate(order, 1):
    avg = sum(scores[v])/max(1,len(scores[v]))
    print(f"| {i} | {v} | {labels[v]} | {borda[v]} | {avg:.1f} | " + " | ".join(str(ranks[v].get(j,'-')) for j in judges) + " |")
