"""Synthetic demo case for RealityCheck. Every name, figure, date and clause is invented.
Source: ../Synthetic-Covenant-Framework.md section 6 (CedarBridge Workflow, Inc.)."""

BORROWER = {
    "id": "cedarbridge",
    "name": "CedarBridge Workflow, Inc.",
    "industry": "Workflow software and implementation services",
    "loan": "$90m senior secured term loan, closed 2026-12-31, 5-year",
    "thesis_version": "T1 (approved 2026-12-15)",
    "synthetic": True,
}

# Underwriting memo passages the assumptions were extracted from.
MEMO = {
    "id": "memo-2026-12",
    "title": "Underwriting memo, approved 2026-12-15",
    "sections": {
        "Revenue quality, para 3": "Customer Atlas accounts for 35% of revenue under a two-year committed agreement with no termination for convenience. That commitment supports the base-case cash-flow forecast.",
        "Customer concentration, para 1": "No single customer exceeds 40% of revenue. The top five customers together represent 68% of revenue.",
        "Leverage, para 2": "Opening total net leverage is 4.00x against a 5.00x maintenance covenant (C01). The base case holds net leverage at or below 4.50x through 2028.",
        "Cash conversion, para 4": "Reported EBITDA of $19m converts to roughly $13m of cash before debt service, leaving about $3m after $9m interest and $1m scheduled principal.",
        "Strategy, para 1": "Management intends to remain a workflow-software business. Acquisitions are limited to related businesses, up to $5m per fiscal year (C05), with pro forma leverage at or below 4.50x.",
    },
}

ASSUMPTIONS = [
    {"id": "A1", "dimension": "Revenue predictability", "criticality": "critical",
     "claim": "Customer Atlas (35% of revenue) is committed for two years without termination for convenience.",
     "locator": "Revenue quality, para 3",
     "why": "Atlas revenue underpins the base-case cash-flow forecast and debt service.",
     "review_trigger": "Any reduction in the commitment term or a new termination right requires review."},
    {"id": "A2", "dimension": "Customer concentration", "criticality": "high",
     "claim": "No single customer exceeds 40% of revenue.",
     "locator": "Customer concentration, para 1",
     "why": "Concentration above 40% makes one customer decision a solvency event.",
     "review_trigger": "Largest customer share above 40% in any quarter."},
    {"id": "A3", "dimension": "Leverage", "criticality": "critical",
     "claim": "Total net leverage stays at or below 4.50x; covenant C01 maximum is 5.00x.",
     "locator": "Leverage, para 2",
     "why": "Headroom to the covenant is the lender's main downside protection.",
     "review_trigger": "Net leverage above 4.50x, or a missing covenant certificate."},
    {"id": "A4", "dimension": "Cash conversion", "criticality": "high",
     "claim": "Cash flow after interest and scheduled principal remains positive.",
     "locator": "Cash conversion, para 4",
     "why": "Negative free cash flow after debt service erodes the cash cushion.",
     "review_trigger": "Negative trailing free cash flow after debt service."},
    {"id": "A5", "dimension": "Strategy and downside resilience", "criticality": "medium",
     "claim": "CedarBridge remains a workflow-software business; acquisitions stay within the $5m annual basket and related businesses.",
     "locator": "Strategy, para 1",
     "why": "A strategy shift changes the risk profile the loan was priced on.",
     "review_trigger": "An executed acquisition above $5m, or a move outside related businesses."},
]

# Reporting packets, in release order. The UI must not show a packet before its available_at date.
# metrics are $m; None means the covenant certificate has not been delivered.
PACKETS = [
    {"id": "pkt-2027q1", "borrower": "cedarbridge", "period": "Q1 2027", "available_at": "2027-05-10",
     "type": "Quarterly packet with covenant certificate",
     "metrics": {"debt": 90.0, "eligible_cash": 11.0, "reported_ebitda": 20.4, "restructuring": 0.0,
                 "top_customer": "Atlas", "top_customer_share": 0.34, "fcf_after_debt_service": 0.9},
     "text": {
         "Management update, para 1": "Trading is in line with budget. Trailing EBITDA rose to $20.4m on renewals across the top ten accounts.",
         "Customer contracts, para 2": "The Atlas master agreement remains in force through December 2028 on its original terms.",
         "Covenant certificate, para 1": "Total net leverage at March 31, 2027 is 3.92x against a 5.00x maximum.",
     }},
    {"id": "pkt-2027q2", "borrower": "cedarbridge", "period": "Q2 2027", "available_at": "2027-08-12",
     "type": "Quarterly packet with covenant certificate and contract amendment",
     "metrics": {"debt": 89.0, "eligible_cash": 10.5, "reported_ebitda": 20.6, "restructuring": 0.0,
                 "top_customer": "Atlas", "top_customer_share": 0.35, "fcf_after_debt_service": 1.1},
     "text": {
         "Management update, para 1": "Revenue and EBITDA are stable. Net leverage is unchanged at 3.8x.",
         "Customer contracts, para 2": "Effective July 1, 2027, Customer Atlas may terminate its agreement on 30 days' notice without penalty.",
         "Customer contracts, para 3": "Atlas has not indicated any intention to terminate. Management expects the relationship to continue.",
         "Covenant certificate, para 1": "Total net leverage at June 30, 2027 is 3.83x against a 5.00x maximum.",
     }},
    {"id": "pkt-2027q3", "borrower": "cedarbridge", "period": "Q3 2027", "available_at": "2027-11-20",
     "type": "Management update only; covenant certificate not delivered (due 2027-11-14)",
     "metrics": None,
     "text": {
         "Management update, para 1": "The quarterly covenant certificate will follow once the audit committee has reviewed the EBITDA bridge.",
         "Management update, para 2": "Management has signed a non-binding letter of intent to acquire Lumen Ops, a field-service scheduling vendor, for $7m, subject to lender consent under C05.",
         "Management update, para 3": "Atlas volumes were stable in the quarter.",
     }},
]

# Paired mitigated case: same termination right, but with documented replacement commitments.
PACKETS_MITIGATED = [
    {"id": "pkt-m-2027q2", "borrower": "cedarbridge", "period": "Q2 2027 (mitigated case)", "available_at": "2027-08-12",
     "type": "Quarterly packet with contract amendment and new customer agreement",
     "metrics": {"debt": 89.0, "eligible_cash": 10.5, "reported_ebitda": 20.6, "restructuring": 0.0,
                 "top_customer": "Atlas", "top_customer_share": 0.35, "fcf_after_debt_service": 1.1},
     "text": {
         "Management update, para 1": "Revenue and EBITDA are stable. Net leverage is unchanged at 3.8x.",
         "Customer contracts, para 2": "Effective July 1, 2027, Customer Atlas may terminate its agreement on 30 days' notice without penalty.",
         "Customer contracts, para 4": "On June 28, 2027, Customer Beacon executed a three-year committed agreement worth $9m annually with no termination for convenience.",
         "Covenant certificate, para 1": "Total net leverage at June 30, 2027 is 3.83x against a 5.00x maximum.",
     }},
]

ALLOWED_STATUS = ["supported", "weakened", "contradicted", "insufficient_evidence"]
ALLOWED_IMPLICATION = ["adverse", "neutral", "beneficial", "mixed", "unclear"]
ALLOWED_ACTION = ["continue_routine_monitoring", "request_information", "review_credit_view", "consider_reunderwriting"]

# Answer key for the eval (frozen before any model run). Only assumptions that change are listed;
# everything else is expected supported / neutral / continue_routine_monitoring.
ANSWER_KEY = {
    "pkt-2027q1": {},
    "pkt-2027q2": {"A1": ("contradicted", "adverse", "review_credit_view")},
    "pkt-2027q3": {"A2": ("insufficient_evidence", "unclear", "request_information"),
                   "A3": ("insufficient_evidence", "unclear", "request_information"),
                   "A4": ("insufficient_evidence", "unclear", "request_information"),
                   "A5": ("supported", "unclear", "request_information")},
    "pkt-m-2027q2": {"A1": ("contradicted", "mixed", "request_information")},
}
