"""Event API behavior. Run: python -m unittest test_event_api (no external calls)."""
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch

import app


class EventAPITests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.state_patch = patch.object(app, "STATE", Path(self.tmp.name) / "state.json")
        self.state_patch.start()
        self.env_patch = patch.dict(app.os.environ, {"NVIDIA_API_KEY": ""})
        self.env_patch.start()
        self.server = app.ThreadingHTTPServer(("127.0.0.1", 0), app.H)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.env_patch.stop()
        self.state_patch.stop()
        self.tmp.cleanup()

    def request(self, route, body=None):
        req = urllib.request.Request(self.base + route,
            data=None if body is None else json.dumps(body).encode(),
            headers={"Content-Type": "application/json"})
        try:
            response = urllib.request.urlopen(req, timeout=5)
        except urllib.error.HTTPError as e:
            response = e
        with response:
            return response.status, json.load(response)

    def test_event_text_is_required(self):
        status, result = self.request("/api/attribute", {"text": "  "})
        self.assertEqual(status, 400)
        self.assertIn("error", result)

    def test_context_exposes_full_catalog_without_evaluator_answers(self):
        status, result = self.request("/api/attribution-context")
        self.assertEqual(status, 200)
        self.assertEqual({a["id"] for a in result["assumptions"]}, {f"T{i:02}" for i in range(1, 25)})
        self.assertEqual(len(result["covenants"]), 30)
        self.assertNotIn("ground_truth_location", json.dumps(result))

    def test_conflicting_profiles_and_unknown_packets_rejected(self):
        status, _ = self.request("/api/attribute", {"text": "Customer update.", "profiles": ["INTEREST", "CASH-COVERAGE"]})
        self.assertEqual(status, 400)
        status, _ = self.request("/api/attribute", {"packet_id": "missing"})
        self.assertEqual(status, 400)

    def test_unavailable_model_is_saved_unassessed_without_losing_old_history(self):
        app.save({"assessments": [{"id": "old"}], "uploaded": [{"id": "old-upload"}]})
        status, result = self.request("/api/attribute", {"text": "Atlas received a cancellation right.", "profiles": ["CORE"]})
        self.assertEqual(status, 200)
        self.assertEqual(result["engine"], "unavailable")
        self.assertTrue(result["error"])
        self.assertEqual(result["attributions"], [])
        _, history = self.request("/api/history")
        self.assertEqual(history["assessments"], [{"id": "old"}])
        self.assertEqual(history["uploaded"], [{"id": "old-upload"}])
        self.assertEqual(history["events"][0]["id"], result["id"])

    def test_review_decision_requires_real_target_and_preserves_baseline(self):
        app.save({"events": [{"id": "ev1", "attributions": [{"id": "link1", "target_id": "T01"}], "decisions": {}}]})
        status, _ = self.request("/api/attribution-decision", {"event_id": "ev1", "attribution_id": "bad", "decision": "accept"})
        self.assertEqual(status, 400)
        status, _ = self.request("/api/attribution-decision", {"event_id": "ev1", "attribution_id": "link1", "decision": "rewrite"})
        self.assertEqual(status, 400)
        status, rec = self.request("/api/attribution-decision", {"event_id": "ev1", "attribution_id": "link1", "decision": "accept", "reason": "Verified amendment."})
        self.assertEqual(status, 200)
        self.assertEqual(rec["decisions"]["link1"]["reason"], "Verified amendment.")
        _, history = self.request("/api/history")
        self.assertEqual(history["events"][0]["decisions"]["link1"]["decision"], "accept")
        self.assertNotIn("assumptions", app.load())

    def test_future_packet_cannot_be_analyzed_before_available_date(self):
        status, _ = self.request("/api/attribute", {"packet_id": "pkt-2027q2", "review_date": "2026-01-01"})
        self.assertEqual(status, 400)

    def test_packet_reset_preserves_event_reviews(self):
        event = {"id": "ev1", "attributions": [], "decisions": {"link1": {"decision": "accept"}}}
        app.save({"events": [event], "assessments": [{"id": "old"}], "uploaded": [{"id": "upload"}]})
        status, _ = self.request("/api/reset", {})
        self.assertEqual(status, 200)
        _, history = self.request("/api/history")
        self.assertEqual(history["events"], [event])
        self.assertEqual(history["assessments"], [])
        self.assertEqual(history["uploaded"], [])

    def test_malformed_json_returns_error_without_dropping_connection(self):
        req = urllib.request.Request(self.base + "/api/attribute", data=b"[invalid", headers={"Content-Type": "application/json"})
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(req, timeout=5)
        self.assertEqual(caught.exception.code, 400)
        caught.exception.close()


if __name__ == "__main__":
    unittest.main()
