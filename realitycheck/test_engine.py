"""Smallest checks that fail if the engine logic breaks. Run: python test_engine.py"""
from app import assess, deterministic, net_leverage, validate, rules_semantic
from data import PACKETS, PACKETS_MITIGATED

P = {p["id"]: p for p in PACKETS + PACKETS_MITIGATED}

# Covenant arithmetic from the framework's sensitivity table (net debt 80, EBITDA 20 -> 4.00x; EBITDA 15 -> 5.33x fail)
base = {"debt": 90, "eligible_cash": 10, "reported_ebitda": 19, "restructuring": 1}
assert round(net_leverage(base), 2) == 4.00
assert deterministic({**base, "reported_ebitda": 14, "top_customer": "x", "top_customer_share": .3, "fcf_after_debt_service": 1})["C01"]["result"] == "fail"
assert deterministic({**base, "reported_ebitda": 15, "restructuring": 0, "top_customer": "x", "top_customer_share": .3, "fcf_after_debt_service": 1})["C01"]["result"] == "fail"  # 5.33x
assert deterministic({**base, "reported_ebitda": 16, "restructuring": 0, "top_customer": "x", "top_customer_share": .3, "fcf_after_debt_service": 1})["C01"]["result"] == "pass"  # exactly 5.00x passes
assert deterministic({**base, "restructuring": 5, "top_customer": "x", "top_customer_share": .3, "fcf_after_debt_service": 1})["C01"]["leverage"] == round(80 / (19 + 1.9), 2)  # adjustment capped at 10%
assert deterministic(None)["A3"][0] == "insufficient_evidence"

# Quote verification: a fabricated quote is downgraded, a real one passes.
pk = P["pkt-2027q2"]
fake = validate([{"assumption_id": "A1", "proposed_status": "contradicted", "credit_implication": "adverse", "suggested_action": "review_credit_view",
                  "evidence": [{"locator": "Customer contracts, para 2", "quote": "Atlas will terminate immediately."}]}], pk)[0]
assert fake["proposed_status"] == "insufficient_evidence" and not fake["evidence"][0]["verified"]
real = validate([{"assumption_id": "A1", "proposed_status": "contradicted", "credit_implication": "adverse", "suggested_action": "review_credit_view",
                  "evidence": [{"locator": "Customer contracts, para 2", "quote": pk["text"]["Customer contracts, para 2"]}]}], pk)[0]
assert real["proposed_status"] == "contradicted" and real["evidence"][0]["verified"]
assert validate([{"assumption_id": "Z9"}], pk) == []

# Rules baseline on the four demo packets matches the frozen answer key.
def row(pid, aid):
    r = next(x for x in assess(pid, "rules")["rows"] if x["assumption_id"] == aid)
    return r["status"], r["implication"], r["action"]
assert all(row("pkt-2027q1", a) == ("supported", "neutral", "continue_routine_monitoring") for a in ("A1", "A2", "A3", "A4", "A5"))
assert row("pkt-2027q2", "A1") == ("contradicted", "adverse", "review_credit_view")
assert row("pkt-2027q2", "A3") == ("supported", "neutral", "continue_routine_monitoring")
assert row("pkt-2027q3", "A3") == ("insufficient_evidence", "unclear", "request_information")
assert row("pkt-2027q3", "A5") == ("supported", "unclear", "request_information")      # proposed, not executed
assert row("pkt-m-2027q2", "A1") == ("contradicted", "mixed", "request_information")   # mitigated
print("ok")

# Parse 2.0 output -> packet text: tag regex, section-header locators, header/footer/picture dropped.
from parse import TAG, elements_to_packet_text
raw = "<x_0.1><y_0.1>CedarBridge Q2<x_0.5><y_0.12><class_Page-header>\n<x_0.1><y_0.2>Customer contracts<x_0.4><y_0.22><class_Section-header>\n<x_0.1><y_0.3>Atlas may terminate on 30 days' notice.<x_0.9><y_0.35><class_Text>\n<x_0.1><y_0.4><x_0.3><y_0.5><class_Picture>\n<x_0.1><y_0.9>Page 1<x_0.2><y_0.92><class_Page-footer>"
els = [{"class": m.group(6), "bbox": (), "text": m.group(3).strip()} for m in TAG.finditer(raw)]
assert [e["class"] for e in els] == ["Page-header", "Section-header", "Text", "Picture", "Page-footer"]
assert elements_to_packet_text([els]) == {"Customer contracts, para 1 (p1)": "Atlas may terminate on 30 days' notice."}
print("parse ok")
