"""Behavior checks for event preparation, profile selection, and model-output validation."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import attribution


class AttributionTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.registry_path = Path(self.tempdir.name) / "assumption_registry.json"
        self.registry_path.write_text(json.dumps({
            "version": "1.0",
            "assumptions": [
                {"id": "T01", "title": "Customer commitment", "claim": "Atlas remains committed.",
                 "baseline_status": "approved_synthetic", "criticality": "high", "covenant_ids": ["PC08"], "source": "memo"},
                {"id": "T02", "title": "Retention", "claim": "Customer retention remains stable.",
                 "baseline_status": "working", "criticality": "high", "covenant_ids": [], "source": "register"},
                {"id": "T03", "title": "Liquidity", "claim": "Liquidity remains adequate.",
                 "baseline_status": "working", "criticality": "medium", "covenant_ids": ["PC24"], "source": "register"},
            ],
            "relationships": [
                {"source": "T01", "target": "T02", "type": "economic_dependency"},
                {"source": "T02", "target": "T03", "type": "economic_dependency"},
            ],
        }), encoding="utf-8")
        self.registry_patch = patch.object(attribution, "REGISTRY_PATH", self.registry_path)
        self.registry_patch.start()
        self.addCleanup(self.registry_patch.stop)
        self.addCleanup(self.tempdir.cleanup)

    @staticmethod
    def event(text="Atlas may terminate its agreement on 30 days' notice."):
        return attribution.prepare_event({
            "title": "Atlas amendment",
            "text": text,
            "available_at": "2027-08-12",
            "review_date": "2027-08-12",
            "profiles": ["CORE"],
        })

    @staticmethod
    def citation(quote="Atlas may terminate its agreement on 30 days' notice.", locator="Event description"):
        return {"document_id": "event-input", "locator": locator, "quote": quote}

    def run_model(self, response, profiles=None):
        return attribution.analyze_event(
            self.event(), profiles or ["CORE"], api_key="test", model="test-model",
            completion=lambda _system, _user: response,
        )

    def test_profiles_include_core_and_enforce_elections(self):
        core = attribution.selected_covenants([])
        self.assertIn("PC01", core)
        self.assertNotIn("PC24", core)
        self.assertEqual(["PC24", "PC25"], [c for c in attribution.selected_covenants(["LIQUIDITY"]) if c in {"PC24", "PC25"}])
        self.assertTrue({"PC22", "PC23"}.issubset(attribution.selected_covenants(["GOVERNANCE"])))
        revolver = attribution.selected_covenants(["REVOLVER"])
        self.assertNotIn("PC01", revolver)
        self.assertIn("PC30", revolver)
        with self.assertRaisesRegex(ValueError, "mutually exclusive"):
            attribution.selected_covenants(["INTEREST", "CASH-COVERAGE"])
        with self.assertRaisesRegex(ValueError, "unknown profile"):
            attribution.selected_covenants(["SURPRISE"])

    def test_prepare_event_rejects_evidence_unavailable_at_cutoff(self):
        packet = {
            "id": "pkt-future", "period": "Q3", "available_at": "2027-11-20",
            "text": {"Management update, para 1": "Atlas volumes were stable."},
        }
        with self.assertRaisesRegex(ValueError, "review_date"):
            attribution.prepare_event({"review_date": "2027-11-19", "profiles": ["CORE"]}, packet)
        with self.assertRaisesRegex(ValueError, "unknown profile"):
            attribution.prepare_event({"text": "A valid event.", "profiles": ["SURPRISE"]})

    def test_quote_tolerance_is_limited_to_a_closing_period_at_a_cut(self):
        source = {('DOC', 'P1'): 'Inventory older than 180 days was 14.2% of inventory at cost, compared with 5.5% at origination, mostly winter product.'}
        cite = lambda quote: attribution._citations([{'document_id': 'DOC', 'locator': 'P1', 'quote': quote}], source, required=True)
        exact = cite('Inventory older than 180 days was 14.2% of inventory at cost')
        self.assertTrue(exact[0]['verified'])
        self.assertNotIn('verification_note', exact[0])
        cut = cite('Inventory older than 180 days was 14.2% of inventory at cost, compared with 5.5% at origination.')
        self.assertTrue(cut[0]['verified'])
        self.assertIn('closing period', cut[0]['verification_note'])                     # the tolerance is recorded, not silent
        self.assertIsNone(cite('Inventory older than 180 days was 41.2% of inventory at cost.'))   # a changed number never passes
        self.assertIsNone(cite('Inventory older than 180 days was 14.2% of stock at cost.'))        # a changed word never passes
        self.assertIsNone(cite('at cost.'))                                               # too short to be meaningful once trimmed

    def test_wrong_page_locator_is_corrected_only_for_a_unique_verbatim_match_in_the_same_document(self):
        source = {('DOC', 'p1'): 'Hosting expenditure is assumed at $3.15 million per month.', ('DOC', 'p2'): 'Renewal is assumed at 92.00%.',
                  ('DOC', 'p3'): 'Renewal is assumed at 92.00%. Repeated.', ('OTHER', 'p1'): 'Trial conversion is assumed at 8.00%.'}
        cite = lambda quote, relocate=True: attribution._citations([{'document_id': 'DOC', 'locator': 'p2', 'quote': quote}], source, required=True, relocate=relocate)
        moved = cite('Hosting expenditure is assumed at $3.15 million per month.')
        self.assertEqual(moved[0]['locator'], 'p1')
        self.assertIn('the model cited p2', moved[0]['verification_note'])               # the correction is recorded, not silent
        self.assertIsNone(cite('Trial conversion is assumed at 8.00%.'))                  # never relocated across documents
        self.assertIsNone(attribution._citations([{'document_id': 'DOC', 'locator': 'p1', 'quote': 'Renewal is assumed at 92.00%.'}],
                                                 source, required=True, relocate=True))   # ambiguous match is not guessed
        self.assertIsNone(cite('Hosting expenditure is assumed at $3.15 million per month.', relocate=False))   # off unless a caller opts in

    def test_fake_quote_wrong_locator_and_unknown_target_are_excluded(self):
        response = {"attributions": [
            {"target_type": "assumption", "target_id": "T01", "relation_type": "direct_assumption_evidence",
             "risk_direction": "adverse", "proposed_status": "weakened", "rationale": "Fabricated quote.",
             "evidence": [self.citation("Atlas already terminated.")], "counterevidence": [], "missing_information": [],
             "suggested_action": "review_assumption", "proposed_adjustment": "Revisit renewal expectations.", "path": []},
            {"target_type": "assumption", "target_id": "T01", "relation_type": "direct_assumption_evidence",
             "risk_direction": "adverse", "proposed_status": "weakened", "rationale": "Wrong locator.",
             "evidence": [self.citation(locator="Missing paragraph")], "counterevidence": [], "missing_information": [],
             "suggested_action": "review_assumption", "proposed_adjustment": "Revisit renewal expectations.", "path": []},
            {"target_type": "assumption", "target_id": "T99", "relation_type": "direct_assumption_evidence",
             "risk_direction": "adverse", "proposed_status": "weakened", "rationale": "Unknown target.",
             "evidence": [self.citation()], "counterevidence": [], "missing_information": [],
             "suggested_action": "monitor", "proposed_adjustment": "None.", "path": []},
        ], "candidates": []}
        result = self.run_model(response)
        self.assertEqual([], result["attributions"])
        self.assertGreaterEqual(len(result["warnings"]), 3)
        self.assertEqual("unaddressed", next(x for x in result["coverage"] if x["assumption_id"] == "T01")["status"])

    def test_invalid_downstream_status_path_and_root_are_rejected(self):
        common = {"target_type": "assumption", "risk_direction": "adverse", "rationale": "Conditional exposure.",
                  "evidence": [self.citation()], "counterevidence": [], "missing_information": ["Customer response"],
                  "suggested_action": "monitor", "proposed_adjustment": "Run a downside case."}
        response = {"attributions": [
            {**common, "target_id": "T01", "relation_type": "direct_assumption_evidence", "proposed_status": "weakened", "path": []},
            {**common, "target_id": "T02", "relation_type": "downstream_exposure", "proposed_status": "contradicted", "path": ["T01", "T02"]},
            {**common, "target_id": "T03", "relation_type": "downstream_exposure", "proposed_status": None, "path": ["T01", "T03"]},
            {**common, "target_id": "T02", "relation_type": "downstream_exposure", "proposed_status": None, "path": ["T03", "T02"]},
        ], "candidates": []}
        result = self.run_model(response)
        self.assertEqual(["T01"], [x["target_id"] for x in result["attributions"]])
        self.assertEqual(3, len(result["warnings"]))

    def test_missing_key_and_outage_leave_every_assumption_unassessed(self):
        missing = attribution.analyze_event(self.event(), ["CORE"], api_key="", model="test-model")
        self.assertEqual("unavailable", missing["engine"])
        self.assertTrue(missing["error"])
        self.assertEqual([], missing["attributions"])
        self.assertTrue(all(x["status"] == "unassessed" for x in missing["coverage"]))

        def outage(_system, _user):
            raise TimeoutError("endpoint timed out")

        failed = attribution.analyze_event(self.event(), ["CORE"], api_key="test", model="test-model", completion=outage)
        self.assertEqual("unavailable", failed["engine"])
        self.assertIn("endpoint timed out", failed["error"])
        self.assertTrue(all(x["status"] == "unassessed" for x in failed["coverage"]))

    def test_valid_multi_target_event_is_verified_without_asserting_a_breach(self):
        response = {"attributions": [
            {"target_type": "assumption", "target_id": "T01", "relation_type": "direct_assumption_evidence",
             "risk_direction": "adverse", "proposed_status": "weakened", "rationale": "The new cancellation right weakens commitment.",
             "evidence": [self.citation()], "counterevidence": [], "missing_information": ["Atlas intent"],
             "suggested_action": "review_assumption", "proposed_adjustment": "Review the commitment wording.", "path": []},
            {"target_type": "covenant", "target_id": "PC08", "relation_type": "covenant_trigger",
             "risk_direction": "unclear", "proposed_status": None, "rationale": "A cancellation right is not an actual notice.",
             "evidence": [self.citation()], "counterevidence": [], "missing_information": ["Actual termination notice"],
             "suggested_action": "request_information", "proposed_adjustment": "Obtain any notice sent by Atlas.", "path": []},
        ], "candidates": []}
        result = self.run_model(response)
        self.assertEqual("nemotron", result["engine"])
        self.assertIsNone(result["error"])
        self.assertEqual(2, len(result["attributions"]))
        assumption, covenant = result["attributions"]
        self.assertTrue(assumption["verified"])
        self.assertEqual("approved_synthetic", assumption["baseline_status"])
        self.assertEqual("Customer commitment", assumption["target_title"])
        self.assertTrue(covenant["verified"])
        self.assertEqual("selected", covenant["applicability"])
        self.assertEqual("1.0", covenant["target_version"])
        self.assertIsNone(covenant["proposed_status"])
        self.assertEqual("addressed", next(x for x in result["coverage"] if x["assumption_id"] == "T01")["status"])
        self.assertEqual("unaddressed", next(x for x in result["coverage"] if x["assumption_id"] == "T02")["status"])

    def test_unhashable_model_fields_withhold_only_the_malformed_findings(self):
        valid = {"target_type": "assumption", "target_id": "T01", "relation_type": "direct_assumption_evidence",
                 "risk_direction": "adverse", "proposed_status": "weakened", "rationale": "Verified event evidence.",
                 "evidence": [self.citation()], "counterevidence": [], "missing_information": [],
                 "suggested_action": "review_assumption", "proposed_adjustment": "Review the assumption.", "path": []}
        response = {"attributions": [
            {**valid, "target_id": ["T01"]},
            {**valid, "relation_type": ["direct_assumption_evidence"]},
            valid,
        ], "candidates": []}
        result = self.run_model(response)
        self.assertEqual("nemotron", result["engine"])
        self.assertEqual(["T01"], [item["target_id"] for item in result["attributions"]])
        self.assertEqual(2, len(result["warnings"]))

    def test_evidence_gap_cannot_claim_supported_or_contradicted_status(self):
        common = {"target_type": "assumption", "target_id": "T02", "relation_type": "evidence_gap",
                  "risk_direction": "unclear", "rationale": "The event omits retention evidence.",
                  "evidence": [self.citation()], "counterevidence": [], "missing_information": ["Retention data"],
                  "suggested_action": "request_information", "proposed_adjustment": "Obtain retention data.", "path": []}
        response = {"attributions": [
            {**common, "proposed_status": "supported"},
            {**common, "proposed_status": "contradicted"},
            {**common, "proposed_status": "insufficient_evidence"},
        ], "candidates": []}
        result = self.run_model(response)
        self.assertEqual(["insufficient_evidence"], [item["proposed_status"] for item in result["attributions"]])
        self.assertEqual(2, len(result["warnings"]))

    def test_candidate_requires_verified_event_evidence(self):
        response = {"attributions": [], "candidates": [{
            "claim": "A new assumption", "rationale": "The model proposes it without a citation.", "evidence": [],
        }]}
        result = self.run_model(response)
        self.assertEqual([], result["candidates"])
        self.assertEqual(1, len(result["warnings"]))

    def test_prompt_gives_target_specific_relations_and_a_valid_shape(self):
        captured = {}

        def completion(system, user):
            captured["system"] = system
            captured["user"] = json.loads(user)
            return {"attributions": [], "candidates": []}

        attribution.analyze_event(self.event(), ["CORE"], api_key="test", model="test-model", completion=completion)
        payload = captured["user"]
        self.assertEqual(
            ["direct_assumption_evidence", "downstream_exposure", "evidence_gap"],
            payload["response_schema"]["relation_type_by_target"]["assumption"],
        )
        self.assertEqual(
            ["covenant_input", "covenant_trigger", "covenant_permission", "evidence_gap"],
            payload["response_schema"]["relation_type_by_target"]["covenant"],
        )
        guidance = payload["attribution_guidance"]
        self.assertEqual("T01", guidance["executed_customer_termination_amendment"]["direct_target"])
        self.assertFalse(guidance["no_termination_notice"]["covenant_triggered"])
        self.assertIn("every materially justified", guidance["coverage_pass"]["instruction"])
        self.assertIn("literal truth", guidance["literal_claim_vs_economic_harm"]["instruction"])
        self.assertIn("explicitly supplied", guidance["missing_information"]["instruction"])
        example = payload["minimal_valid_response_example"]["attributions"][0]
        self.assertEqual(("assumption", "direct_assumption_evidence"),
                         (example["target_type"], example["relation_type"]))
        self.assertIn("not a default", payload["minimal_valid_response_example"]["example_scope"])
        self.assertIn("do not copy", captured["system"].lower())


if __name__ == "__main__":
    unittest.main()
