# Round 3: Panel Consensus Sentence

Generated Sept 15, 2026. The same five judge personas (PNC Compound, NVIDIA Nemotron, LANXESS Xtract, Seed Round VC, PittCSC Organizer) worked in three steps to agree on one "Detect" sentence that beats all 20 originals from round 2.

## Result: unanimous

**Detect when a fund's labeled exposure drifts from what it actually holds.**

All five judges voted YES. Round-3B score 44/50, minimum individual score 8, versus 39/50 for the round-2 winner ("Detect when portfolio exposure drifts unnoticed"). Every judge scored it higher than the round-2 winner.

Optional demo-day variant proposed by PNC and the organizer (not put to a vote; NVIDIA, LANXESS, and the VC chose no edit, and the VC earlier scored the ETF-literal line as "one feature, not a platform"):
*Detect when an ETF's labeled exposure drifts from what it actually holds.*

## Step A: proposals (2 per judge)

- PNC-P1|Detect when a fund's holdings drift from what its label promises.
- PNC-P2|Detect when an investment's exposure drifts from its stated identity.
- XTRACT-P1|Detect when a holding's economic identity drifts from the label investors bought.
- XTRACT-P2|Detect when portfolio exposure drifts silently from the thesis it was sold on.
- NVIDIA-P1|Detect when your fund's real exposure drifts from its stated identity.
- NVIDIA-P2|Detect when a fund's classified identity no longer matches its filings.
- VC-P1|Detect when a fund's labeled exposure drifts from what it actually holds.
- VC-P2|Detect when a holding's economic identity drifts from its label.
- ORG-P1|Detect when an ETF's label no longer matches what it actually holds.
- ORG-P2|Detect when a holding's economic identity drifts from your investment thesis.

## Step B: every judge scores every candidate (C0 = round-2 winner baseline)

| ID | Sentence | Total /50 | Min | PNC | NVIDIA | LANXESS | Seed | PittCSC |
|---|---|---|---|---|---|---|---|---|
| C7 | Detect when a fund's labeled exposure drifts from what it actually holds. | 44 | 8 | 9 | 8 | 9 | 9 | 9 |
| C8 | Detect when a holding's economic identity drifts from its label. | 43 | 8 | 8 | 9 | 9 | 9 | 8 |
| C9 | Detect when an ETF's label no longer matches what it actually holds. | 43 | 8 | 9 | 8 | 9 | 8 | 9 |
| C1 | Detect when a fund's holdings drift from what its label promises. | 42 | 8 | 8 | 8 | 9 | 9 | 8 |
| C3 | Detect when a holding's economic identity drifts from the label investors bought. | 42 | 8 | 8 | 9 | 9 | 8 | 8 |
| C0 | Detect when portfolio exposure drifts unnoticed. | 39 | 7 | 8 | 7 | 8 | 8 | 8 |
| C5 | Detect when your fund's real exposure drifts from its stated identity. | 39 | 6 | 8 | 8 | 8 | 9 | 6 |
| C2 | Detect when an investment's exposure drifts from its stated identity. | 36 | 6 | 7 | 8 | 7 | 8 | 6 |
| C4 | Detect when portfolio exposure drifts silently from the thesis it was sold on. | 33 | 5 | 8 | 5 | 7 | 6 | 7 |
| C10 | Detect when a holding's economic identity drifts from your investment thesis. | 33 | 5 | 7 | 6 | 7 | 5 | 8 |
| C6 | Detect when a fund's classified identity no longer matches its filings. | 27 | 4 | 4 | 6 | 7 | 6 | 4 |

ACCEPT votes: PNC C9, NVIDIA C7, LANXESS C8, Seed C5, PittCSC C3

OBJECT votes: PNC C6, NVIDIA C6, LANXESS C6, Seed C4, PittCSC C6

### Per-judge rationale

#### PNC Compound

| ID | Score | Rationale |
|---|---|---|
| C0 | 8 | Concrete and memorable, "unnoticed" adds risk awareness, but stays a bit abstract about what actually changed. |
| C1 | 8 | Clear fund-and-label framing, plain language, easy to grasp in a single hearing. |
| C2 | 7 | Solid but "stated identity" pairs two abstract nouns, slightly less concrete than the label-based lines. |
| C3 | 8 | Strong synthesis of identity and label with "investors bought" giving real personal stake, if a bit long. |
| C4 | 8 | Vivid "sold on" phrasing ties exposure to thesis nicely but leans slightly sales-pitchy for a risk tool. |
| C5 | 8 | Personal "your fund's real exposure" is direct and relatable, reads like something a business would actually use. |
| C6 | 4 | Reads like an internal QA log about filings and classification, not a user-facing benefit statement. |
| C7 | 9 | Very concrete, plain English, "actually holds" nails the core insight without any jargon. |
| C8 | 8 | Clean and tight, ties economic identity to label without overexplaining, easy to say in a pitch. |
| C9 | 9 | Simplest and most concrete line here, matches the ETF-wedge story exactly, zero jargon, instantly clear. |
| C10 | 7 | Identity-plus-thesis combo works but narrows the audience to individual investor theses over business use. |

**ACCEPT C9:** It needs no explanation, matches the ETF-wedge entry point the team already chose, and no judge is likely to object to it as too jargon-heavy or too salesy.

**OBJECT C6:** It describes an internal classification step, not a benefit to a person or business, which is exactly the chatbot-wrapper-adjacent vagueness I score down.

#### NVIDIA Nemotron

| ID | Score | Rationale |
|---|---|---|
| C0 | 7 | Exposure and drift are concrete, but it omits classification or labels, Nemotron's actual role. |
| C1 | 8 | Holdings versus label promise is concrete and benchmarkable, with a mild stakes framing that isn't overclaiming. |
| C2 | 8 | Exposure drifting from stated identity is precise, evaluable, and mirrors the pipeline's compare-and-measure design. |
| C3 | 9 | Economic identity and label investors bought hits classification, ground truth, and stakes in one clean line. |
| C4 | 5 | Portfolio exposure is strong, but thesis sold on is subjective and hard for any eval to confirm. |
| C5 | 8 | Exposure drifting from stated identity is concrete and benchmarkable, matches the pipeline's own vocabulary well. |
| C6 | 6 | Classified identity and filings sound precise, but filings are the model's input, not independent ground truth. |
| C7 | 8 | Labeled exposure versus actual holdings names two of the panel's favorite concepts in one testable claim. |
| C8 | 9 | Economic identity drifting from its label is tight, precise, and maps directly onto a classification eval. |
| C9 | 8 | ETF label versus actual holdings is plain, concrete, and fits the ETF wedge without any jargon. |
| C10 | 6 | Economic identity is strong, but investment thesis reintroduces the subjective, hard-to-benchmark language I'd flag elsewhere. |

**ACCEPT C7:** It fuses the panel's two highest-scoring concepts, labeled and exposure, into one concrete, benchmarkable claim without leaning on subjective thesis language only the VC favored.

**OBJECT C6:** Comparing a fund's classified identity to its own filings is circular, since filings are Nemotron's input text, not the independent ground truth the eval actually checks against.

#### LANXESS Xtract

| ID | Score | Rationale |
|---|---|---|
| C0 | 8 | Concrete and implies a hidden signal, but doesn't name the label or identity source of truth. |
| C1 | 9 | Concrete holdings-versus-label-promise framing, plain English, no overclaim, easy for any judge to accept. |
| C2 | 7 | Solid but generic, investment and stated identity feel slightly redundant and less vivid than alternatives. |
| C3 | 9 | Combines identity, label, and bought cleanly, ties directly to the ETF wedge and ownership framing. |
| C4 | 7 | Thesis is a softer, less evidence-grounded anchor than label or filings for a traceability-focused judge. |
| C5 | 8 | Personal your fund voice works, stated identity concrete, but slightly less crisp than the label-based lines. |
| C6 | 7 | Uniquely names filings, strong on traceability, but comparing a filings-derived classification to filings itself reads circular. |
| C7 | 9 | Labeled exposure versus what it actually holds is concrete, plain, and mirrors the ETF wedge well. |
| C8 | 9 | Tight, concrete, and fuses identity and label in the fewest words with zero overclaim. |
| C9 | 9 | Names the ETF wedge directly and stays maximally plain English, very accessible to a mixed panel. |
| C10 | 7 | Identity plus thesis skips the label concept entirely, weaker anchor to filings-based evidence. |

**ACCEPT C8:** It is the shortest line that fuses PNC's label and NVIDIA's identity without overclaiming, so all five judges can read their own preferred concept into it.

**OBJECT C6:** Classified identity is derived from filings, so saying it no longer matches its filings reads as circular or factually confused to a technical panel.

#### Seed Round VC

| ID | Score | Rationale |
|---|---|---|
| C0 | 8 | Solid, safe baseline, but "drifts unnoticed" doubles the project's own name and stays fairly abstract. |
| C1 | 9 | Concrete, plain English, keeps "label" language investors search for, generalizes past ETFs without overclaiming. |
| C2 | 8 | Clean generalization across asset classes, but "stated identity" feels slightly abstract for a homepage line. |
| C3 | 8 | Nicely fuses identity and label language, though "the label investors bought" reads a touch clunky. |
| C4 | 6 | Vivid, but "sold on" edges into accusing issuers of a sales pitch, a legal and tone risk. |
| C5 | 9 | Real-vs-stated framing mirrors the actual mechanism exactly, personal, safe, and generalizes cleanly beyond ETFs. |
| C6 | 6 | Ties nicely to filings-based classification, but narrows the pitch to a compliance check, not economic drift. |
| C7 | 9 | Concrete and safe, clearly names the label-versus-holdings gap without implying fault or intent. |
| C8 | 9 | Short, sharp, fuses identity and label cleanly, though it drops the exposure language some judges favored. |
| C9 | 8 | Maximally clear and ETF-literal, easy for any judge to grasp, but reads as one feature, not a platform. |
| C10 | 5 | Logically confused: an asset's identity can't coherently "drift from" a subjective investment thesis. |

**ACCEPT C5:** It fuses the panel's favorite keywords, exposure and identity, into a safe real-versus-stated frame every judge can read as both clear and platform-scale.

**OBJECT C4:** "Sold on" implies the fund or issuer deceived investors, an accusation the product can't back up and a legal liability none of the five judges should accept.

#### PittCSC Organizer

| ID | Score | Rationale |
|---|---|---|
| C0 | 8 | Clean and honest but "unnoticed" is an unprovable claim the 60 second demo cannot actually show. |
| C1 | 8 | Concrete fund, label, holdings language, honest match, "promises" is a small flourish but stays clear. |
| C2 | 6 | Exposure and identity are mismatched categories here, pairing feels awkward and slightly abstract on first read. |
| C3 | 8 | Bridges identity and label in one honest sentence, vivid "investors bought" phrase, strong compromise line. |
| C4 | 7 | Vivid but wordy, "silently" and "sold on" add flourish that risks reading like marketing copy. |
| C5 | 6 | "Real exposure" versus "stated identity" is an awkward pairing, reads like generic fintech copy. |
| C6 | 4 | Reverses the actual pipeline since filings feed the classification rather than checking it, mechanism mismatch. |
| C7 | 9 | Most literal match to the demo's two bars, plain English, honest, easy to remember at a booth. |
| C8 | 8 | Short and punchy, ties identity directly to label, matches the Nemotron classification concept cleanly. |
| C9 | 9 | Names the ETF wedge directly, plain honest phrasing, matches label versus actual holdings exactly. |
| C10 | 8 | Ties identity to thesis well and stays honest, though thesis is more abstract than label or exposure. |

**ACCEPT C3:** It uses both identity and label, the two words NVIDIA and PNC each anchored on, while keeping drift central for the rest of the panel.

**OBJECT C6:** It implies the system checks a classification against filings, but Nemotron derives the classification from filings, reversing the real pipeline.


## Step C: final vote on C7

JUDGE: PNC Compound
VOTE|YES
FALLBACK|C9
EDIT|Detect when an ETF's labeled exposure drifts from what it actually holds.
REASON|Swapping "fund's" for "ETF's" keeps C7's precise exposure language while grounding it in the concrete ETF wedge every judge already recognized favorably in C9, at no cost in clarity or scope.

JUDGE: NVIDIA Nemotron
VOTE|YES
FALLBACK|none
EDIT|none
REASON|C7 already has the highest floor and total across all five judges, names two of the panel's favorite concepts, labeled and exposure, and avoids the circularity and legal-risk objections that sank C6 and C4, so further tweaking risks trading a proven consensus for an untested one.

JUDGE: LANXESS Xtract
VOTE|YES
FALLBACK|C8
EDIT|none
REASON|C7 pairs a concrete label-versus-actual-holdings claim with no overclaim and already cleared every judge's bar, so further wordsmithing risks reopening a settled consensus for no real gain.

JUDGE: PittCSC Organizer
VOTE|YES
FALLBACK|C9
EDIT|Detect when an ETF's labeled exposure drifts from what it actually holds.
REASON|Swapping "fund's" to "ETF's" names the exact product on screen, making the strongest consensus line even more literal without losing what any judge already liked.

JUDGE: Seed Round VC
VOTE|YES
FALLBACK|none
EDIT|none
REASON|C7 has both the highest total and the highest floor score, meaning no judge on the panel actively dislikes it, which is the strongest real signal of true consensus rather than a compromise nobody loves.
