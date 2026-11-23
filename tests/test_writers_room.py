"""Offline regression tests for the Atlas writers' room (stdlib only)."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_writers_room import validate_room

FIXTURE = ROOT / "tests" / "fixtures" / "aoc004-writers-room-v1.json"

class WritersRoomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.good = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_aoc004_fixture_passes_structure(self):
        errors, warnings = validate_room(self.good)
        self.assertEqual(errors, [])

    def test_unverified_cannot_be_claimed_as_verified_edition(self):
        data = copy.deepcopy(self.good)
        data["release_kind"] = "VERIFIED_EDITION"
        self.assertTrue(any("verified edition" in x for x in validate_room(data)[0]))

    def test_unverified_demonstration_needs_disclosure(self):
        data = copy.deepcopy(self.good)
        data["visible_demo_disclosure"] = False
        self.assertTrue(any("disclose" in x for x in validate_room(data)[0]))

    def test_no_unlabelled_fiction(self):
        data = copy.deepcopy(self.good)
        data["scenes"][0]["fiction_label"] = "FACT"
        self.assertTrue(any("fiction label" in x for x in validate_room(data)[0]))

    def test_no_invented_incident_causal_findings(self):
        data = copy.deepcopy(self.good)
        data["scenes"][0]["prohibited_claims"] = ["ACTUAL_CAUSE_ESTABLISHED"]
        self.assertTrue(any("unsupported" in x for x in validate_room(data)[0]))

    def test_every_character_has_a_scene(self):
        data = copy.deepcopy(self.good)
        data["scenes"] = [s for s in data["scenes"] if s["pov"] != "boma"]
        self.assertTrue(any("not every" in x for x in validate_room(data)[0]))

    def test_unknown_local_reference_blocks(self):
        data = copy.deepcopy(self.good)
        data["scenes"][0]["context_refs"].append("MADE_UP_VILLAGE")
        self.assertTrue(any("unknown context" in x for x in validate_room(data)[0]))

    def test_no_self_approval(self):
        data = copy.deepcopy(self.good)
        data["review"]["writer_is_sole_approver"] = True
        self.assertTrue(any("self-approve" in x for x in validate_room(data)[0]))

    def test_scene_requires_choice_cost_and_revelation(self):
        data = copy.deepcopy(self.good)
        data["scenes"][0]["choice"] = ""
        self.assertTrue(any("missing choice" in x for x in validate_room(data)[0]))
        data = copy.deepcopy(self.good)
        for scene in data["scenes"]:
            scene["reveal_to"] = []
        self.assertTrue(any("reveal" in x for x in validate_room(data)[0]))

    def test_region_only_does_not_imply_verified_community(self):
        data = copy.deepcopy(self.good)
        data["world_scope"]["no_unverified_local_identities"] = False
        self.assertTrue(any("region-only" in x for x in validate_room(data)[0]))

if __name__ == "__main__":
    unittest.main()
