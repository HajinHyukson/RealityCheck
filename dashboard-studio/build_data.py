"""Export saved RealityCheck evidence without importing or running the application.

Run: python dashboard-studio/build_data.py
Only dataset.js and DATA.md are written. Source files and SQLite stay read-only.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
READS: dict[Path, str] = {}


def read(path: Path) -> str:
    raw = path.read_bytes()
    READS[path] = hashlib.sha256(raw).hexdigest()
    return raw.decode("utf-8-sig")


def load(path: Path):
    return json.loads(read(path))


def scalar(value) -> str:
    return "" if value is None else str(value)


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def evidence(items: list) -> list:
    return [{"sourceId": scalar(x.get("document_id")), "quote": scalar(x.get("quote")),
             "locator": scalar(x.get("locator")),
             "verified": x.get("verified") is True} for x in items]


def build_company(code: str, folder: str = "") -> dict:
    public = bool(folder)
    case_dir = ROOT / "real-credit-cases" / folder
    if public:
        rolling = ROOT / "realitycheck" / "benchmark" / code / "rolling"
        seed = load(rolling / "seed.json")
        notes = load(rolling / "review_notes.json")
        manifest = {d["id"]: d for d in load(case_dir / "manifest.json")["documents"]}
    else:
        db = ROOT / "realitycheck" / "b01.sqlite"
        READS[db] = hashlib.sha256(db.read_bytes()).hexdigest()
        with sqlite3.connect(db.as_uri() + "?mode=ro", uri=True) as connection:
            seed = {key: json.loads(value) for key, value in connection.execute("SELECT key,value FROM metadata")}
            seed["events"] = [json.loads(row[0]) for row in connection.execute("SELECT payload FROM events ORDER BY seq")]
        notes, manifest = {}, {}

    profile = seed["profile"]
    model = scalar(seed.get("analysis_model"))
    company = {"id": code, "name": seed["borrower"]["name"], "sector": seed["borrower"]["sector"],
               "provenance": ("Real public SEC filings; AI assumptions reconstructed from public evidence. "
                              "Recorded Nemotron findings are model interpretations with reviewer corrections, "
                              "not the lender's actual underwriting thesis. Historical amendments are observed public disclosures."
                              if public else "Synthetic demonstration: fictional company, reports, agreement and amendments. "
                              "Recorded Nemotron findings; unsigned candidate terms remain proposed."),
               "asOf": scalar(seed.get("presentation", {}).get("as_of", profile.get("as_of"))),
               "summary": "\n\n".join([profile["summary"], *notes.get("profile", []),
                                         *seed["borrower"].get("missing_inputs", [])]),
               "model": model, "sources": [], "assumptions": [], "events": [], "covenants": [], "versions": []}
    if not public:
        short_titles = ["Reliable connectors support renewals", "Reusable implementation templates",
                        "Cash conversion after investment", "Leverage and transaction headroom",
                        "Stable receivable collection", "Connector support continuity"]
    for index, original in enumerate(profile["assumptions"]):
        company["assumptions"].append({"id": original["id"],
            "title": original["title"] if public else short_titles[index],
            "claim": original["claim"], "basis": scalar(original.get("basis")) + " · baseline: " + scalar(original.get("baseline_status")),
            "status": scalar(original.get("baseline_status")),
            "covenantIds": original.get("covenant_ids", []), "evidence": evidence(original.get("evidence", []))})
    assumptions = {a["id"]: a for a in company["assumptions"]}
    source_parts: dict[str, dict[str, str]] = {}
    source_event: dict[str, dict] = {}

    for event in seed["events"]:
        analysis = event.get("analysis", {})
        review_notes = list(dict.fromkeys(notes.get("events", {}).get(event["id"], []) + analysis.get("review_notes", [])))
        findings = []
        for attribution in analysis.get("attributions", []):
            if attribution.get("target_type") != "assumption" or attribution.get("target_id") not in assumptions:
                continue
            if attribution.get("proposed_status"):
                assumptions[attribution["target_id"]]["status"] = attribution["proposed_status"]
            findings.append({"assumptionId": attribution["target_id"],
                "status": scalar(attribution.get("proposed_status") or "unassessed"),
                "implication": ("Recorded risk direction: " + scalar(attribution.get("risk_direction")) + ". "
                                + scalar(attribution.get("proposed_adjustment") or attribution.get("rationale"))),
                "rationale": "\n\n".join([scalar(attribution.get("rationale")), *review_notes]),
                "action": scalar(attribution.get("suggested_action")),
                "evidence": evidence(attribution.get("evidence", [])),
                "covenantIds": assumptions[attribution["target_id"]]["covenantIds"][:]})
        source_ids = list(dict.fromkeys(part["document_id"] for part in event.get("sources", [])))
        event_date = scalar(event.get("review_date") or event.get("available_at"))
        for part in event.get("sources", []):
            source_parts.setdefault(part["document_id"], {})[part["locator"]] = part["text"]
            source_event.setdefault(part["document_id"], {"title": event["title"], "date": event_date})
        status = ["Recorded " + scalar(analysis.get("engine", "analysis")), scalar(event.get("status"))]
        if review_notes:
            status.append("Reviewer notes included")
        if analysis.get("warnings"):
            status.append(str(len(analysis["warnings"])) + " stored validation/review warnings")
        if analysis.get("error"):
            status.append(scalar(analysis["error"]))
        summary = scalar(event.get("presentation_summary") or analysis.get("summary"))
        if not public and analysis.get("summary"):
            summary = "Recorded model summary: " + summary
        company["events"].append({"id": event["id"], "title": event["title"], "date": event_date,
            "eventDate": scalar(event.get("event_date") or event_date),
            "availableAt": scalar(event.get("available_at") or event_date),
            "packageVersion": scalar(event.get("package_version")),
            "decisionAction": scalar((event.get("decision") or {}).get("action")),
            "summary": "\n\n".join([summary, *review_notes]), "sourceIds": source_ids,
            "findings": findings, "model": scalar(analysis.get("model") or model),
            "analysisStatus": " · ".join(filter(None, status))})

    versions = list(seed["versions"])
    if seed.get("pending_proposal"):
        versions.append(seed["pending_proposal"])
    clauses = {}
    # The covenant reference is the original package; changes remain in dated versions.
    for version in versions:
        for clause in version.get("clauses", []) + version.get("add_clauses", []):
            clauses.setdefault(clause["id"], clause)
        changes = []
        for change in version.get("changes", []):
            changes.append("\n\n".join(filter(None, [scalar(change.get("clause_id")),
                scalar(change.get("summary")), "Before: " + scalar(change.get("before")),
                "After: " + scalar(change.get("after"))])))
        for clause in version.get("add_clauses", []):
            changes.append(clause["id"] + " · " + clause["title"] + "\n\n" + clause["clause"])
        company["versions"].append({"id": scalar(version.get("id") or code + "-V" + version["version"]),
            "version": version["version"], "title": version["title"],
            "effectiveAt": scalar(version.get("effective_at")),
            "parentVersion": scalar(version.get("parent_version")),
            "triggerEventId": scalar(version.get("trigger_event_id")),
            "isProposal": version.get("status") == "proposed",
            "clauses": [{"id": clause["id"], "title": clause["title"], "text": clause["clause"]}
                        for clause in version.get("clauses", []) + version.get("add_clauses", [])],
            "date": scalar(version.get("publicly_available_at") or version.get("decision_at")
                           or version.get("draft_at") or version.get("effective_at"))[:10],
            "status": scalar(version.get("status")),
            "summary": "\n\n".join(filter(None, [scalar(version.get("description")),
                scalar(version.get("rationale")), scalar(version.get("waiver_scope")),
                ("Executed/effective: " + version["effective_at"]) if version.get("effective_at") else ""])),
            "changes": changes})
    company["covenants"] = [{"id": c["id"], "title": c["title"], "text": c["clause"]} for c in clauses.values()]

    all_evidence = [e for a in company["assumptions"] for e in a["evidence"]]
    all_evidence += [e for event in company["events"] for f in event["findings"] for e in f["evidence"]]
    wanted = set(source_parts) | {e["sourceId"] for e in all_evidence}
    wanted |= {c["source"]["document_id"] for c in clauses.values() if c.get("source", {}).get("document_id")}
    if not public:
        wanted |= {"underwriting-memo.md", "credit-agreement.md", "origination-financial-model.json"}

    for source_id in sorted(wanted):
        metadata = manifest.get(source_id, {})
        event_context = source_event.get(source_id, {})
        parts = source_parts.get(source_id, {}).copy()
        locator = "Complete stored event source"
        if public:
            extracted = load(case_dir / "extracted" / (source_id + ".json"))
            full_text = "\n\n".join(p["locator"] + "\n" + p["text"] for p in extracted)
            if len(full_text) <= 100_000:
                text = full_text
                locator = "Full cached paragraph extraction"
            else:
                # Large agreements/10-Qs use complete cited paragraphs plus adjacent context.
                selected = set()
                citations = [e for e in all_evidence if e["sourceId"] == source_id]
                for index, paragraph in enumerate(extracted):
                    if paragraph["locator"] in parts or any(
                        e["locator"] == paragraph["locator"] or norm(e["quote"]) in norm(paragraph["text"])
                        for e in citations):
                        selected.update(range(max(0, index - 1), min(len(extracted), index + 2)))
                text = "\n\n".join(extracted[i]["locator"] + "\n" + extracted[i]["text"] for i in sorted(selected))
                locator = "Complete cited paragraphs with adjacent context; full filing at source URL"
            # Section citations in the saved profile point into the extracted clause record.
            section_text = [c.get("section", "") + "\n" + c["clause"] for c in clauses.values()
                            if c.get("source", {}).get("document_id") == source_id]
            if section_text:
                text += "\n\nCached agreement clause record\n\n" + "\n\n".join(section_text)
        else:
            original = ROOT / "synthetic-credit-portfolio" / "model_inputs" / "B01-fluxrail-workflow-inc" / source_id
            if original.is_file():
                text, locator = read(original), "Full synthetic source document"
            else:
                text = "\n\n".join(k + "\n" + v for k, v in parts.items())
        company["sources"].append({"id": source_id,
            "title": scalar(metadata.get("title") or event_context.get("title") or source_id),
            "date": scalar(metadata.get("filing_date") or event_context.get("date") or profile.get("as_of")),
            "kind": ("Public SEC filing · " + scalar(metadata.get("type"))) if public else "Synthetic demonstration source",
            "text": text, "url": scalar(metadata.get("url")), "locator": locator})
    return company


def check(data: dict) -> dict:
    counts = {}
    assert [c["id"] for c in data["companies"]] == ["R01", "B01", "R02"]
    for company in data["companies"]:
        sources = {s["id"]: s for s in company["sources"]}
        assumptions = {a["id"] for a in company["assumptions"]}
        covenants = {c["id"] for c in company["covenants"]}
        assert len(sources) == len(company["sources"])
        for key in ["sources", "assumptions", "events", "covenants", "versions"]:
            assert company[key], (company["id"], key)
        for event in company["events"]:
            assert event["date"] and set(event["sourceIds"]) <= sources.keys()
            assert all(f["assumptionId"] in assumptions for f in event["findings"])
        records = company["assumptions"] + [f for event in company["events"] for f in event["findings"]]
        for record in records:
            assert set(record["covenantIds"]) <= covenants
            for citation in record["evidence"]:
                assert citation["sourceId"] in sources, citation
                assert norm(citation["quote"]) in norm(sources[citation["sourceId"]]["text"]), citation
        counts[company["id"]] = {key: len(company[key]) for key in ["sources", "assumptions", "events", "covenants", "versions"]}
        counts[company["id"]]["findings"] = sum(len(e["findings"]) for e in company["events"])
        assert counts[company["id"]]["findings"] > 0
    def strings_only(value):
        if isinstance(value, dict):
            for child in value.values(): strings_only(child)
        elif isinstance(value, list):
            for child in value: strings_only(child)
        else:
            assert isinstance(value, (str, bool)), (type(value), value)
    strings_only(data)
    for path, digest in READS.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, "Source changed during build: " + str(path)
    return counts


def main():
    data = {"generatedAt": datetime.now(timezone.utc).isoformat(), "companies": [
        build_company("R01", "R01-irobot-carlyle"), build_company("B01"),
        build_company("R02", "R02-rumbleon-oaktree")]}
    counts = check(data)
    HERE.mkdir(exist_ok=True)
    (HERE / "dataset.js").write_text("// Generated from local saved evidence; rebuild with build_data.py.\nwindow.RC_DATA = "
                                    + json.dumps(data, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
    table = "\n".join("| " + " | ".join([code, *[str(v) for v in values.values()]]) + " |" for code, values in counts.items())
    (HERE / "DATA.md").write_text("""# Dashboard dataset provenance

Generated by `python dashboard-studio/build_data.py` using Python's standard library. The build reads existing files and opens B01 SQLite with `mode=ro`. It does not initialize the application, invoke a model, call a service, or modify source data. The generated JavaScript is serialized JSON assigned to `window.RC_DATA`; it uses no eval.

| Company | Sources | Assumptions | Events | Covenants | Versions | Findings |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
""" + table + """

## Source records

- R01 iRobot (default): `realitycheck/benchmark/R01/rolling/seed.json`, `review_notes.json`, and `real-credit-cases/R01-irobot-carlyle/{manifest.json,extracted/*.json}`. Historical public-filing replay through June 2025.
- B01 FluxRail: read-only `realitycheck/b01.sqlite` metadata and event payloads, and `synthetic-credit-portfolio/model_inputs/B01-fluxrail-workflow-inc/` source documents. This entire case is fictional, including future-dated 2027 events. Its pending version 1.3 is an unsigned synthetic proposal, not adopted terms.
- R02 RumbleOn: `realitycheck/benchmark/R02/rolling/seed.json`, `review_notes.json`, and `real-credit-cases/R02-rumbleon-oaktree/{manifest.json,extracted/*.json}`. Historical public-filing replay through August 2024.

R01/R02 public filings are real. Their assumptions were reconstructed by Nemotron and are not Carlyle's or Oaktree's private underwriting thesis. Findings are saved outputs from `nvidia/nemotron-3-super-120b-a12b`, not a fresh analysis. Existing reviewer corrections are preserved in company summaries, event summaries, and finding rationales. The model's wording and statuses remain intact; a verified quote confirms textual support, not the model's reasoning. Excluded raw/withheld model attributions are not reinstated. The normalized findings include assumption attributions only; separate covenant assessments, raw responses and benchmark scores are not relabeled as assumption findings.

## Normalization

Scalar fields are strings except evidence `verified` and version `isProposal`, which are booleans. Arrays remain arrays. Assumption claims are verbatim. B01 display titles are shortened while full claims remain available. Assumption status is the latest recorded proposed status, falling back to the baseline when no status has been proposed; the original baseline is retained in `basis`. Finding status is recorded `proposed_status`, or `unassessed` when the model did not propose one; recorded risk direction remains separately labeled in the implication. These are model assessments, with the underlying baseline and reviewer corrections preserved.

Event `date` uses the stored review/availability date; `eventDate` and `availableAt` preserve occurrence and availability separately. `packageVersion` identifies the recorded contractual context. Version `effectiveAt`, `parentVersion`, `triggerEventId`, and `clauses` preserve the original package-history relationships and clause snapshots. Version dates use public disclosure/decision dates, and the summary retains the recorded effective date. B01 proposal status stays `proposed`. `versions[].changes` contains strings with stored before/after clause text or added clause text; public amendments remain identified as observed historical lender responses. Covenant reference text is from the original package (plus later added clauses); dated changes are in versions.

Source URLs come only from the local SEC manifest. Complete extracted text is included up to 100,000 characters per filing. Larger filings use complete cited paragraphs with adjacent context plus the actual cached agreement clause records; the locator identifies this bounded selection and the source URL opens the full filing. Synthetic documents and stored event-source text are included in full. Source text is never fabricated to make a citation pass.

## Runnable verification

Re-running the builder checks nonempty counts; unique source IDs; assumption, covenant and source references; that every quoted passage is present in the exported source text after whitespace normalization; scalar types; and SHA-256 stability of every source read during the build. It fails before writing output if any check fails. No hosted calls or tests of live workflows are needed for this read-only export.
""", encoding="utf-8")
    print(json.dumps(counts, indent=2))
    print("Verified source references, exact quote coverage, scalar types and unchanged source hashes.")


if __name__ == "__main__":
    main()
