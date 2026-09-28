import sys, unittest, json, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from reader_builder import chunks
import test_production as base
class GrammarGateRegression(unittest.TestCase):
 setUp=base.ProductionRegression.setUp
 tearDown=base.ProductionRegression.tearDown
 fixture=base.ProductionRegression.fixture
 evaluate=base.ProductionRegression.evaluate
 change=base.ProductionRegression.change
 def test_old_parity_receipt_is_no_longer_sufficient(self):
  self.fixture();(self.run/'reader-contract-qa.json').unlink()
  self.assertEqual(self.evaluate()['status'],'BLOCKED')
 def test_verified_images_do_not_require_film(self):
  self.fixture();(self.run/'opening-media.json').unlink()
  self.assertEqual(self.evaluate()['status'],'PUBLICATION_CANDIDATE')
 def test_missing_opening_system_blocks_even_when_static_parity_is_pass(self):
  self.fixture();(self.run/'opening-system.json').unlink()
  self.assertEqual(self.evaluate()['status'],'BLOCKED')
 def test_unverified_opening_image_blocks(self):
  self.fixture();self.change('opening-system.json',lambda d:d['assets'][0].update(sha256='wrong'))
  self.assertEqual(self.evaluate()['status'],'BLOCKED')
 def test_approved_film_path_requires_visual_qa_and_hash(self):
  self.fixture();film=json.loads((self.run/'opening-media.json').read_text())
  self.change('opening-system.json',lambda d:d.update(mode='approved_film',film={'path':film['path'],'sha256':film['sha256']},assets=[]))
  self.change('reader-contract-qa.json',lambda d:d.update(motion=[{'mode':'approved_film','skip':True} for _ in range(3)]))
  self.assertEqual(self.evaluate()['status'],'PUBLICATION_CANDIDATE')
  self.change('opening-media.json',lambda d:d['visual_qa'].update(status='BLOCKED'))
  self.assertEqual(self.evaluate()['status'],'BLOCKED')
 def test_stale_contract_blocks(self):
  self.fixture();self.change('reader-contract-qa.json',lambda d:d.update(version='old'))
  self.assertEqual(self.evaluate()['status'],'BLOCKED')
 def test_mismatched_contract_deployment_blocks(self):
  self.fixture();self.change('reader-contract-qa.json',lambda d:d.update(deploy_id='other'))
  self.assertEqual(self.evaluate()['status'],'BLOCKED')
 def test_sentence_pagination_preserves_verbatim_copy(self):
  copy=json.loads((Path(__file__).resolve().parents[1]/'content/AUTOMATED-TEST-001/editorial-copy.json').read_text())
  for block in [copy['opening'],copy['place'],copy['consequences'],*copy['scenes'].values()]:
   for p in block['paragraphs']:
    beats=chunks(p['text']);self.assertEqual(' '.join(beats),p['text']);self.assertTrue(all(len(x.split())<=70 for x in beats))
  self.assertGreater(len(chunks(copy['place']['paragraphs'][0]['text'])),1)
