"""Compare the extraction+rules baseline and Nemotron against the frozen answer key.
Run: python eval.py            Prints exact counts; no percentages without denominators.
Caveat (plan s17): these four packets are DEVELOPMENT cases authored by the prompt author. They show mechanism, not generalization."""
import os, time
from app import assess, MODEL
from data import ANSWER_KEY, ASSUMPTIONS

DEFAULT = ("supported", "neutral", "continue_routine_monitoring")

def expected(pid, aid):
    return ANSWER_KEY[pid].get(aid, DEFAULT)

def run(engine, retries=3):
    hits = {"status": 0, "implication": 0, "action": 0}; n = 0; false_alerts = 0; missed = 0; unverified = 0; fell_back = []
    for pid in ANSWER_KEY:
        for attempt in range(retries):
            rec = assess(pid, engine)
            if engine == "rules" or not rec["error"]:
                break
            time.sleep(5)                       # hosted endpoint returns 503 under load; retry before scoring a fallback
        if rec["error"]:
            fell_back.append(pid); continue     # do not score baseline rows as if the model produced them
        for r in rec["rows"]:
            exp = expected(pid, r["assumption_id"]); got = (r["status"], r["implication"], r["action"]); n += 1
            for i, k in enumerate(hits):
                hits[k] += got[i] == exp[i]
            if exp[0] == "supported" and got[0] != "supported": false_alerts += 1
            if exp[0] != "supported" and got[0] == "supported": missed += 1
            unverified += sum(1 for e in r["evidence"] if not e["verified"])
            if got != exp:
                print(f"  {rec['engine']:9} {pid} {r['assumption_id']}: expected {exp}, got {got}")
    label = "rules" if engine == "rules" else MODEL.split("/")[-1]
    print(f"{label}: scored rows n={n} | status {hits['status']}/{n} implication {hits['implication']}/{n} action {hits['action']}/{n} "
          f"| false_alerts {false_alerts} missed {missed} unverified_quotes {unverified}"
          + (f" | NOT scored (endpoint failed after {retries} tries): {fell_back}" if fell_back else ""))

if __name__ == "__main__":
    run("rules")
    if os.environ.get("NVIDIA_API_KEY"):
        run("auto")
    else:
        print("nemotron  skipped: NVIDIA_API_KEY not set")
