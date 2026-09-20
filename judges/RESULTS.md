# Verb Ranking by Five Simulated SteelHacks XIII Judges

Generated Sept 15, 2026. Five judge personas, each modeled on a real 2026 track rubric (steelhacks.org/tracks), independently ranked 21 unique verbs (Detect and Reconcile were listed twice in the input and deduplicated) as the headline action for the Economic Drift project ("[Verb] when your ETF stops being what you bought").

Judges: PNC Compound (Best Financial Hack), NVIDIA Nemotron (Beyond the Chatbot), LANXESS Xtract (Signal-to-Insight), Seed Round VC (Most Fundable), PittCSC Organizer (general expo judging).

Aggregation: Borda count (rank 1 = 20 points, rank 21 = 0 points, summed across five judges, max 100). Ties broken by average 1-10 strength score. Per-judge columns show that judge's rank.

## Aggregate ranking

| Rank | Verb | Borda | Avg score | PNC | NVIDIA | LANXESS | Seed | PittCSC |
|---|---|---|---|---|---|---|---|---|
| 1 | Detect | 91 | 9.0 | 1 | 3 | 6 | 1 | 3 |
| 2 | Flag | 88 | 8.4 | 2 | 2 | 5 | 6 | 2 |
| 3 | Reconcile | 86 | 8.2 | 3 | 6 | 4 | 2 | 4 |
| 4 | Audit | 82 | 8.0 | 7 | 7 | 3 | 5 | 1 |
| 5 | Monitor | 71 | 6.8 | 4 | 8 | 13 | 3 | 6 |
| 6 | Diagnose | 70 | 6.8 | 6 | 4 | 9 | 7 | 9 |
| 7 | Validate | 63 | 6.4 | 5 | 5 | 15 | 9 | 8 |
| 8 | Trace | 59 | 6.2 | 10 | 10 | 1 | 12 | 13 |
| 9 | Surface | 57 | 5.8 | 9 | 17 | 2 | 15 | 5 |
| 10 | Reassess | 52 | 5.2 | 12 | 9 | 12 | 8 | 12 |
| 11 | Reclassify | 48 | 5.4 | 18 | 1 | 10 | 13 | 15 |
| 12 | Stress-test | 43 | 5.2 | 8 | 11 | 20 | 4 | 19 |
| 13 | Uncover | 41 | 4.4 | 11 | 19 | 7 | 16 | 11 |
| 14 | Interrogate | 36 | 4.4 | 17 | 16 | 8 | 10 | 18 |
| 15 | Reveal | 35 | 4.0 | 15 | 20 | 11 | 17 | 7 |
| 16 | Realign | 33 | 3.8 | 13 | 13 | 18 | 11 | 17 |
| 17 | Challenge | 32 | 3.4 | 16 | 15 | 14 | 14 | 14 |
| 18 | Expose | 29 | 3.4 | 14 | 18 | 16 | 18 | 10 |
| 19 | Update | 20 | 2.8 | 19 | 14 | 17 | 19 | 16 |
| 20 | Correct | 14 | 2.4 | 20 | 12 | 19 | 20 | 20 |
| 21 | Prevent | 0 | 1.0 | 21 | 21 | 21 | 21 | 21 |

## Individual judge rankings with rationale

### PNC Compound

| Rank | Verb | Score | Rationale |
|---|---|---|---|
| 1 | Detect | 10 | Concrete, tech-credible verb that promises an automated system users can trust to catch drift before it costs them. |
| 2 | Flag | 9 | Implies a clear, actionable output like a fraud alert, exactly the UX pattern a fintech judge wants to see. |
| 3 | Reconcile | 9 | Real finance term for comparing claimed vs actual holdings, maps directly to the ETF-label problem and is buildable in 24 hours. |
| 4 | Monitor | 8 | Signals a continuous, product-grade system rather than a one-off analysis, showing awareness of ongoing risk. |
| 5 | Validate | 8 | Concrete verification framing against a stated benchmark, credible and testable within a hackathon timeframe. |
| 6 | Diagnose | 7 | Implies root-cause analysis beyond a simple alert, showing depth, though slightly more academic than action-oriented. |
| 7 | Audit | 7 | Strong finance credibility but implies more rigor and completeness than a 24-hour prototype can honestly deliver. |
| 8 | Stress-test | 7 | Familiar banking term signaling risk awareness, though better suited to resilience testing than steady drift tracking. |
| 9 | Surface | 6 | Reasonable, non-overclaiming verb for showing hidden mismatches, but softer and less specific than detect or flag. |
| 10 | Trace | 6 | Methodical and investigative, evokes following holdings, but less clear about the resulting user benefit. |
| 11 | Uncover | 5 | Suggests a one-time discovery rather than a repeatable, monitorable product feature. |
| 12 | Reassess | 5 | Vague and passive, describes an internal judgment rather than a concrete deliverable users can rely on. |
| 13 | Realign | 4 | Implies corrective action a hackathon team has no authority to actually perform on a fund's holdings. |
| 14 | Expose | 4 | Dramatic and journalistic tone reads as accusatory rather than as a usable financial product. |
| 15 | Reveal | 4 | Vague and dramatic like expose, lacks the concrete mechanism a fintech judge wants to see. |
| 16 | Challenge | 3 | Confrontational but not a describable action or deliverable, unclear what the product actually does. |
| 17 | Interrogate | 3 | Unusual, gimmicky word choice for a financial tool that reads as hype rather than substance. |
| 18 | Reclassify | 3 | Overclaims authority; only fund managers or regulators can actually reclassify an ETF's category. |
| 19 | Update | 2 | Generic and low-energy, fails to communicate any specific value or awareness of failure modes. |
| 20 | Correct | 2 | Overclaims fixing a market or fund; no hackathon can actually correct an ETF's holdings. |
| 21 | Prevent | 1 | Clear overclaim; a 24-hour prototype cannot prevent economic drift or market behavior. |

### NVIDIA Nemotron

| Rank | Verb | Score | Rationale |
|---|---|---|---|
| 1 | Reclassify | 10 | Directly names Nemotron's actual job of re-labeling economic identity from filings text, trivially evaluable against ground-truth labels. |
| 2 | Flag | 9 | Concrete binary classifier output where precision and recall are obvious eval metrics, and it fits a pipeline role cleanly. |
| 3 | Detect | 9 | Classic detection framing invites a benchmark against known-drift cases and matches anomaly-detection framing well. |
| 4 | Diagnose | 8 | Frames Nemotron as assigning a cause or category to drift, directly evaluable against labeled failure modes. |
| 5 | Validate | 8 | Maps to a verification or judging task with a clear pass or fail eval, though less specific than reclassify. |
| 6 | Reconcile | 7 | Finance-native term for comparing label to holdings, evaluable via a reconciliation-error metric, credible pipeline role. |
| 7 | Audit | 7 | Describes a judging pipeline role well but implies more rigor and coverage than a 24-hour prototype likely delivers. |
| 8 | Monitor | 6 | Fits a continuous pipeline role but is generic and undersells the specific classification happening inside. |
| 9 | Reassess | 6 | Implies re-running classification over time, evaluable via label-change accuracy, but wordier and less crisp than reclassify. |
| 10 | Trace | 6 | Leans toward extraction or lineage rather than classification, evaluable but doesn't showcase the judging role as clearly. |
| 11 | Stress-test | 5 | Useful as an eval methodology description, but an odd headline verb for what the product does to a fund. |
| 12 | Correct | 4 | Overclaims an active-fix capability the system doesn't have, and no eval can confirm a correction actually happened. |
| 13 | Realign | 4 | Implies the system changes fund composition rather than reporting drift, an overclaim no eval could support. |
| 14 | Update | 4 | Too generic to signal any model task, could mean anything from a UI refresh to a relabeling. |
| 15 | Challenge | 3 | Adversarial-sounding but not tied to any concrete, measurable model behavior or output. |
| 16 | Interrogate | 3 | Dramatic framing with no corresponding model task, nothing you could actually benchmark. |
| 17 | Surface | 3 | Vague surfacing language common in marketing decks, with no specific evaluable action behind it. |
| 18 | Expose | 2 | Investigative, marketing-coded verb implying wrongdoing, and no eval design maps cleanly onto exposing. |
| 19 | Uncover | 2 | Same investigative-journalism flavor as expose, sounds compelling but names no testable model function. |
| 20 | Reveal | 2 | Purely narrative verb that doesn't correspond to classification, extraction, or judging in any checkable way. |
| 21 | Prevent | 1 | Guarantees an outcome a classifier-plus-metric pipeline cannot deliver or prove in a 24-hour build. |

### LANXESS Xtract

| Rank | Verb | Score | Rationale |
|---|---|---|---|
| 1 | Trace | 10 | Directly names provenance, matching the system's core value of citing exact filing passages behind every drift finding. |
| 2 | Surface | 9 | Implies extracting a specific signal from unreadable volume without asserting more than the evidence shows. |
| 3 | Audit | 9 | Signals rigorous, evidence-based verification against source documents, exactly the traceability an industrial analytics lead expects. |
| 4 | Reconcile | 8 | Financial term for matching stated label against actual evidence, a precise fit for measuring fund drift. |
| 5 | Flag | 8 | Modest, alert-style claim triggered by evidence in bulk text, credible for a 24-hour extraction prototype. |
| 6 | Detect | 8 | Implies pattern recognition across a large corpus grounded in data rather than unsupported opinion. |
| 7 | Uncover | 7 | Suggests hidden signal found in noise, though slightly more dramatic than the evidence it can show. |
| 8 | Interrogate | 7 | Evokes deep querying of dense filings for answers, though an unusual and less polished headline verb. |
| 9 | Diagnose | 6 | Implies analytical conclusion from evidence but underweights the visible citation trail that matters most. |
| 10 | Reclassify | 6 | Names the actual output well but risks sounding like the system claims classification authority, not just evidence. |
| 11 | Reveal | 5 | Leans dramatic and assertion-heavy, less clearly tied to a documented evidence trail. |
| 12 | Reassess | 5 | Vague re-evaluation term that does not clearly imply mining a large corpus for a specific finding. |
| 13 | Monitor | 4 | Suggests passive ongoing tracking rather than delivering a sharp, sourced insight from filings. |
| 14 | Challenge | 4 | Confrontational tone risks sounding like an opinion rather than a cited, evidence-backed finding. |
| 15 | Validate | 4 | Implies confirming correctness, which sits awkwardly against a headline about drift and discrepancy. |
| 16 | Expose | 3 | Journalistic and accusatory, overclaims certainty without emphasizing the underlying citation trail. |
| 17 | Update | 3 | Mundane and undersells the insight-extraction angle central to this track. |
| 18 | Realign | 3 | Implies the system takes corrective action on the fund itself, well beyond a 24-hour prototype's scope. |
| 19 | Correct | 2 | Overclaims by asserting a fix rather than presenting sourced evidence for a human to judge. |
| 20 | Stress-test | 2 | Implies scenario-based robustness testing the described text-extraction system does not actually perform. |
| 21 | Prevent | 1 | Claims a causal, forward-looking capability the system cannot deliver, the clearest overclaim on the list. |

### Seed Round VC

| Rank | Verb | Score | Rationale |
|---|---|---|---|
| 1 | Detect | 10 | Names the literal problem, drift detection is a proven fundable category, implies always-on monitoring a CIO would pay for. |
| 2 | Reconcile | 9 | Reconciliation is an established enterprise finance category with recurring subscription spend and a clear budget line. |
| 3 | Monitor | 9 | Implies an ongoing paid relationship, but risks reading as a commodity dashboard rather than a defensible product. |
| 4 | Stress-test | 9 | Regulator-driven category banks already budget for, rigorous connotation, safe claim that avoids overpromising outcomes. |
| 5 | Audit | 8 | Continuous audit is a recognized paid category with authority and recurring engagement, slightly back-office in flavor. |
| 6 | Flag | 7 | Concrete recurring workflow action a compliance team would search for, though it reads more like a feature than a platform. |
| 7 | Diagnose | 7 | Medical framing implies periodic checkup and ongoing relationship, resonates in fintech without overclaiming a fix. |
| 8 | Reassess | 6 | Signals recurring re-evaluation, but sounds like an advisory service rather than a category-defining product. |
| 9 | Validate | 6 | Safe and precise, but reads as a one-time checkpoint unless explicitly framed as continuous. |
| 10 | Interrogate | 6 | Memorable and edgy for a data product, but doesn't map to an existing buyer category or budget line. |
| 11 | Realign | 5 | Implies a helpful corrective nudge without claiming to execute trades, decent but vague as a category name. |
| 12 | Trace | 5 | Useful forensic root-cause feature, but feels like a supporting capability rather than the headline product. |
| 13 | Reclassify | 5 | Sharp and on-thesis for ETF labels, but implies authority to reclassify that only regulators or issuers actually hold. |
| 14 | Challenge | 4 | Provocative and active, but sounds like a consulting engagement, not a recurring SaaS product a PM buys. |
| 15 | Surface | 4 | Overused SaaS buzzword that undersells differentiation and blends into every insights dashboard pitch. |
| 16 | Uncover | 3 | One-time discovery framing signals a report, not the recurring relationship investors want to see. |
| 17 | Reveal | 3 | Passive and report-like, exactly the one-time-output verb that undercuts a recurring revenue story. |
| 18 | Expose | 3 | Reads as journalism or whistleblowing, an adversarial tone mismatched to enterprise risk software buyers. |
| 19 | Update | 2 | Generic and feature-sized, doesn't imply insight or defensibility, sounds like a changelog not a company. |
| 20 | Correct | 2 | Overclaims: a startup can't actually correct another firm's classification, inviting liability and disbelief. |
| 21 | Prevent | 1 | Biggest overclaim, no risk product can guarantee prevention of drift or loss, invites regulatory and legal skepticism. |

### PittCSC Organizer

| Rank | Verb | Score | Rationale |
|---|---|---|---|
| 1 | Audit | 9 | Instantly readable finance term matching the filings based verification shown, honest and memorable in a 60 second demo. |
| 2 | Flag | 9 | One syllable, matches the verdict output exactly on screen, no overreach, easy to jot down across 40 teams. |
| 3 | Detect | 8 | Clear and honest match to the drift score, though overused across hackathons and less distinctly financial than audit. |
| 4 | Reconcile | 8 | Accounting term precisely describing comparing expected versus observed exposure, honest but slightly less punchy than audit or flag. |
| 5 | Surface | 7 | Plain honest verb for showing a hidden drift score, clear match though less memorable than the top choices. |
| 6 | Monitor | 7 | Clear and honest, but implies ongoing tracking that a single 60 second demo cannot actually show. |
| 7 | Reveal | 6 | Generic but honest, matches showing the drift verdict without overclaiming, forgettable next to sharper choices. |
| 8 | Validate | 6 | Reasonable framing of checking exposure, but the demo mostly shows invalidation, creating a slight verb mismatch. |
| 9 | Diagnose | 6 | Medical metaphor loosely matches the verdict output, understandable but slightly indirect for a financial exposure tool. |
| 10 | Expose | 5 | Sounds like scandal journalism, a dramatic overtone I will side eye given it is just a comparison chart. |
| 11 | Uncover | 5 | Implies hidden secret discovery, a mild overclaim for a straightforward holdings based calculation. |
| 12 | Reassess | 4 | Honest description of the action but clunky wording, forgettable in notes across 40 projects. |
| 13 | Trace | 4 | Suggests following a lineage or path, mismatched since the demo compares one snapshot, not a trail. |
| 14 | Challenge | 3 | Vague verb that does not describe any visible action, leaves me asking what actually happens on screen. |
| 15 | Reclassify | 3 | Overclaims changing the ETF's classification, something the tool never actually does on screen. |
| 16 | Update | 3 | Sounds like refreshing data rather than an analytical verdict, undersells the actual mechanism shown. |
| 17 | Realign | 3 | Implies fixing the portfolio itself, an action far beyond what a static comparison demo delivers. |
| 18 | Interrogate | 3 | Overly aggressive tone mismatched with a calm bar chart and drift score, feels like a stretch. |
| 19 | Stress-test | 3 | Implies scenario simulation under adverse conditions, a different feature than the simple exposure comparison shown. |
| 20 | Correct | 2 | Overclaims fixing the ETF's exposure, something never performed, exactly the overpromise I penalize. |
| 21 | Prevent | 1 | Nothing built in 24 hours prevents anything, the textbook overclaim that instantly loses my trust. |

