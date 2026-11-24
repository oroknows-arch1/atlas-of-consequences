"""Reusable Atlas Writers' Room smoke tests. No AOC-004 story material."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from validate_writers_room import validate_room

class WritersRoomCapabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=json.loads((ROOT/'tests/fixtures/writers-room-neutral-test.json').read_text())

    def test_neutral_manifest_is_structurally_valid(self):
        errors,_=validate_room(self.fixture)
        self.assertEqual(errors,[])
        self.assertIn('REVISE',self.fixture['review'].values())

    def test_unverified_cannot_claim_verified_edition(self):
        item=copy.deepcopy(self.fixture)
        item['release_kind']='VERIFIED_EDITION'
        self.assertTrue(validate_room(item)[0])

    def test_demo_must_disclose_unverified_status(self):
        item=copy.deepcopy(self.fixture)
        item['visible_demo_disclosure']=False
        self.assertTrue(validate_room(item)[0])

    def test_fiction_cannot_be_testimony(self):
        item=copy.deepcopy(self.fixture)
        item['scenes'][0]['fiction_label']='FACT'
        self.assertTrue(validate_room(item)[0])

    def test_no_writer_self_approval(self):
        item=copy.deepcopy(self.fixture)
        item['review']['writer_is_sole_approver']=True
        self.assertTrue(validate_room(item)[0])

if __name__=='__main__': unittest.main()
