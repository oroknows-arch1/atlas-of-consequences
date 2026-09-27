"""Synthetic fixtures test fail-closed behavior; they are never publication evidence."""
import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import production_state as state
import publication_gate as gate
import produce_edition as producer
import reader_builder as builder
import source_qa
from validate_manufacturing_trace import validate as trace_validate
from editorial_factory import validate_copy

class ProductionRegression(unittest.TestCase):
 def setUp(self):
  # Unit fixtures must never inherit production provider policy or live credentials.
  environment=patch.dict('os.environ',{'ATLAS_SAFE_VISUAL_REEXPRESSION':'0','OPENAI_API_KEY':'','RENDER_API_KEY':''})
  environment.start()
  self.addCleanup(environment.stop)
  self.temp=tempfile.TemporaryDirectory()
  self.root=Path(self.temp.name)
  self.run=self.root/'run'
  source=state.ROOT/'content/AUTOMATED-TEST-001'
  self.run.mkdir()
  for name in state.INPUTS: shutil.copyfile(source/name,self.run/name)
  self.bind=state.binding(self.run)
 def tearDown(self): self.temp.cleanup()
 def change(self,name,fn):
  value=state.read(self.run/name);fn(value);state.write(self.run/name,value)
 def test_valid_heat_input_is_separate_from_legacy_candidate(self):
  routes,requirements,story=producer.facts(self.run,'AET1-WC-002')
  self.assertTrue(routes and requirements and story)
 def test_gate_rejects_unbound_selection(self):
  self.change('selected-edition-gate.json',lambda x:x['output'].pop('candidate_id'))
  with self.assertRaisesRegex(RuntimeError,'identity'):producer.facts(self.run,'AET1-WC-002')
 def test_gate_rejects_lost_required_perspective(self):
  self.change('causal_boundary_gate.json',lambda x:x['output']['routes'].pop())
  with self.assertRaises(RuntimeError):producer.facts(self.run,'AET1-WC-002')
 def test_gate_rejects_unknown_scene_source(self):
  self.change('causal_boundary_gate.json',lambda x:x['output']['routes'][0]['scenes'][0]['evidence_refs'].append('FAKE'))
  with self.assertRaisesRegex(RuntimeError,'unregistered'):producer.facts(self.run,'AET1-WC-002')
 def test_receipt_invalidated_by_story_change(self):
  self.change('story_synthesis.json',lambda x:x['output'].update(title='Changed'))
  with self.assertRaises(ValueError):state.require_current(self.run,self.bind)
 def test_internal_meanings_are_not_publication_copy(self):
  routes=state.read(self.run/'causal_boundary_gate.json')['output']['routes']
  with self.assertRaises(ValueError):validate_copy({'scenes':{}},routes,{'WB-HEAT-2025'})
 def test_malformed_editorial_paragraph_is_repairable_validation_error(self):
  routes=state.read(self.run/'causal_boundary_gate.json')['output']['routes']
  source_ids={x['id'] for x in state.read(self.run/'source-register.json')}
  block={'heading':'Synthetic','paragraphs':['plain text is invalid here']}
  malformed={'opening':block,'place':block,'consequences':block,
             'scenes':{s['scene_id']:block for r in routes for s in r['scenes']}}
  with self.assertRaisesRegex(ValueError,'structured object'):validate_copy(malformed,routes,source_ids)
 def test_malformed_editorial_section_is_repairable_validation_error(self):
  routes=state.read(self.run/'causal_boundary_gate.json')['output']['routes']
  source_ids={x['id'] for x in state.read(self.run/'source-register.json')}
  malformed={'opening':'plain text','place':'plain text','consequences':'plain text',
             'scenes':{s['scene_id']:'plain text' for r in routes for s in r['scenes']}}
  with self.assertRaisesRegex(ValueError,'structured object'):validate_copy(malformed,routes,source_ids)
 def test_editorial_api_schema_covers_exact_scene_ids_and_nested_objects(self):
  from editorial_factory import copy_schema
  routes=[{'scenes':[{'scene_id':'ONE'},{'scene_id':'TWO'}]}]
  schema=copy_schema(routes,{'SOURCE'})
  self.assertEqual(schema['properties']['scenes']['required'],['ONE','TWO'])
  section=schema['properties']['scenes']['properties']['ONE']
  self.assertEqual(section['type'],'object')
  self.assertFalse(section['additionalProperties'])
  paragraph=section['properties']['paragraphs']['items']
  self.assertEqual(paragraph['properties']['evidence_refs']['items']['enum'],['SOURCE'])
  self.assertEqual(set(paragraph['required']),{'text','state','evidence_refs'})
 def test_provider_error_keeps_diagnosis_and_redacts_key(self):
  import io
  from urllib.error import HTTPError
  from provider_errors import describe
  error=HTTPError('https://api.openai.com',400,'Bad Request',{},io.BytesIO(b'{"error":{"code":"invalid_request","message":"problem with sk-secret"}}'))
  text=describe(error)
  self.assertIn('invalid_request',text)
  self.assertNotIn('sk-secret',text)
 def test_repair_router_maps_route_defects_and_runs_mixed_workers(self):
  loop=(state.ROOT/'tools/review_loop.py').read_text()
  self.assertIn('affected_scene_ids',loop)
  self.assertIn("owners & {'visual_factory','asset_persistence','editorial_factory'}",loop)
  self.assertIn("if 'reader_treatment' in owners",loop)
  import review_loop
  self.assertEqual(review_loop.affected_scene_ids([{'scene_id':'phone-route-H4–H6'}],['H1-S1','H4-S1','H6-S2']),{'H4-S1','H6-S2'})
 def test_deployment_worker_verifies_live_asset_hashes(self):
  deploy=(state.ROOT/'tools/deploy_review.py').read_text()
  self.assertIn('asset_integration_status',deploy)
  self.assertIn('deployed bytes differ',deploy)
  self.assertIn('Cache-Control',deploy)
 def test_production_workflow_resumes_from_branch_tip(self):
  workflow=(state.ROOT/'.github/workflows/atlas-edition-production.yml').read_text()
  self.assertIn('ref: test/automated-edition-1',workflow)
  self.assertIn('cancel-in-progress: false',workflow)
 def test_partial_asset_persistence_runs_after_failure(self):
  workflow=(state.ROOT/'.github/workflows/atlas-edition-production.yml').read_text()
  partial=workflow.split('name: Persist partial assets and production receipts')[1].split('- name:')[0]
  self.assertIn('if: always()',partial)
  self.assertIn('git add public/assets public/review',partial)
 def test_provider_safety_rejection_is_not_automatically_retried(self):
  routes,requirements,story=producer.facts(self.run,'AET1-WC-002')
  candidate=state.read(self.run/'selected-edition-candidate.json')
  with patch.object(producer,'ROOT',self.root), patch.dict('os.environ',{'ATLAS_IMAGE_COMMAND':'generator','ATLAS_VISUAL_QA_COMMAND':'verifier'}):
   with patch.object(producer,'invoke',side_effect=RuntimeError('Provider HTTP 400: code=moderation_blocked')) as invoke:
    assets,defects=producer.produce_assets(self.run,'AET1-WC-002',routes,requirements[:1],candidate)
  self.assertEqual(invoke.call_count,1)
  self.assertEqual(assets,[])
  self.assertTrue(defects[0]['external_action_required'])
 def test_provider_alternative_preserves_original_rejection_and_job(self):
  import provider_routing as routing
  job={'scene_id':'TEST','meaning':'unchanged meaning','truth_boundary':'unchanged boundary'}
  proposal={'decision':'SAFE_ALTERNATIVE','composition':'ordinary empty room','reason':'safer environment'}
  verdict={'safe':True,'meaning_preserved':True,'boundary_preserved':True,'reason':'same purpose'}
  with patch.dict('os.environ',{'ATLAS_SAFE_VISUAL_REEXPRESSION':'1'}), patch.object(routing,'model_json',side_effect=[proposal,verdict]):
   invoke=unittest.mock.Mock(side_effect=[RuntimeError('moderation_blocked request_id=original'),{'path':'binary'}])
   result=routing.request_asset(self.run,job,'primary',invoke)
  self.assertEqual(invoke.call_count,2)
  replacement=invoke.call_args.args[1]
  self.assertEqual(replacement['meaning'],job['meaning'])
  self.assertEqual(replacement['truth_boundary'],job['truth_boundary'])
  saved=state.read(self.run/'provider-routing-receipt.json')['scenes']['TEST']
  self.assertIn('request_id=original',saved['events'][0]['reason'])
  self.assertEqual(result['routing_provenance']['route'],'safe_equivalent_primary')
 def test_changed_meaning_cannot_enable_safe_alternative(self):
  import provider_routing as routing
  proposal={'decision':'SAFE_ALTERNATIVE','composition':'room','reason':'test'}
  verdict={'safe':True,'meaning_preserved':False,'boundary_preserved':True,'reason':'lost meaning'}
  with patch.dict('os.environ',{'ATLAS_SAFE_VISUAL_REEXPRESSION':'1'}), patch.object(routing,'model_json',side_effect=[proposal,verdict]):
   invoke=unittest.mock.Mock(side_effect=RuntimeError('moderation_blocked'))
   with self.assertRaisesRegex(RuntimeError,'provider_route_blocked'):routing.request_asset(self.run,{'scene_id':'TEST'},'primary',invoke)
   self.assertEqual(invoke.call_count,1)
 def test_authorized_alternate_receives_only_verified_safe_composition(self):
  import provider_routing as routing
  proposal={'decision':'SAFE_ALTERNATIVE','composition':'room','reason':'test'}
  verdict={'safe':True,'meaning_preserved':True,'boundary_preserved':True,'reason':'same purpose'}
  with patch.dict('os.environ',{'ATLAS_SAFE_VISUAL_REEXPRESSION':'1','ATLAS_APPROVED_ALTERNATE_IMAGE_COMMAND':'approved-alternate'}), patch.object(routing,'model_json',side_effect=[proposal,verdict]):
   invoke=unittest.mock.Mock(side_effect=[RuntimeError('moderation_blocked'),RuntimeError('moderation_blocked'),{'path':'binary'}])
   result=routing.request_asset(self.run,{'scene_id':'TEST'},'primary',invoke)
  self.assertEqual(invoke.call_args.args[0],'approved-alternate')
  self.assertEqual(invoke.call_args.args[1]['safe_composition'],'room')
  self.assertEqual(result['routing_provenance']['route'],'authorized_alternate')
 def test_refused_safe_alternative_is_not_resubmitted_on_restart(self):
  import provider_routing as routing
  proposal={'decision':'SAFE_ALTERNATIVE','composition':'room','reason':'test'}
  verdict={'safe':True,'meaning_preserved':True,'boundary_preserved':True,'reason':'same purpose'}
  with patch.dict('os.environ',{'ATLAS_SAFE_VISUAL_REEXPRESSION':'1','ATLAS_APPROVED_ALTERNATE_IMAGE_COMMAND':''}), patch.object(routing,'model_json',side_effect=[proposal,verdict]):
   invoke=unittest.mock.Mock(side_effect=RuntimeError('moderation_blocked'))
   for _ in range(2):
    with self.assertRaisesRegex(RuntimeError,'provider_route_blocked'):routing.request_asset(self.run,{'scene_id':'TEST'},'primary',invoke)
   self.assertEqual(invoke.call_count,2)
 def test_provider_policy_revision_reopens_cached_alternative_without_losing_rejection(self):
  import provider_routing as routing
  proposal={'decision':'SAFE_ALTERNATIVE','composition':'empty classroom with desks and exercise books','reason':'same purpose'}
  verdict={'safe':True,'meaning_preserved':True,'boundary_preserved':True,'reason':'same purpose'}
  with patch.dict('os.environ',{'ATLAS_SAFE_VISUAL_REEXPRESSION':'1'}), patch.object(routing,'model_json',side_effect=[proposal,verdict]):
   invoke=unittest.mock.Mock(side_effect=[RuntimeError('moderation_blocked'),{'path':'binary'}])
   result=routing.request_asset(self.run,{'scene_id':'TEST','meaning':'school disruption','truth_boundary':'boundary'},'primary',invoke)
  saved=state.read(self.run/'provider-routing-receipt.json')['scenes']['TEST']
  self.assertEqual(saved['policy_version'],'safe-visual-v2')
  self.assertIn('original_rejection',saved['events'][0]['kind'])
  self.assertEqual(result['routing_provenance']['route'],'safe_equivalent_primary')
 def test_visual_review_batches_screenshots_and_retries_rate_limits(self):
  review=(state.ROOT/'tools/review_rendered.py').read_text()
  self.assertIn('for i in range(0,len(candidate),8)',review)
  self.assertIn('gpt-4o-mini',review)
  self.assertIn('error.code != 429',review)
  self.assertIn('Retry-After',review)
 def test_visual_review_retries_transient_rate_limits(self):
  review=(state.ROOT/'tools/review_rendered.py').read_text()
  self.assertIn('error.code != 429',review)
  self.assertIn("Retry-After",review)
  self.assertIn('range(1,4)',review)
 def test_source_fallback_preserves_primary_failure_and_passes_declared_canonical(self):
  class Response:
   status=200
   url='https://canonical.example/source.pdf'
   def __enter__(self): return self
   def __exit__(self,*args): pass
   def read(self,n): return b'%PDF-1.7'
  def opener(request,timeout):
   if request.full_url == 'https://primary.example/source': raise RuntimeError('HTTP Error 403: Forbidden')
   return Response()
  result=source_qa.resolve_source({'id':'S','url':'https://primary.example/source','fallback_urls':['https://canonical.example/source.pdf']},opener)
  self.assertEqual(result['status'],'PASS')
  self.assertTrue(result['fallback_used'])
  self.assertEqual(result['resolved_url'],'https://canonical.example/source.pdf')
  self.assertEqual(result['attempts'][0]['status'],'BLOCKED')
 def test_source_without_declared_fallback_fails_closed(self):
  def opener(request,timeout): raise RuntimeError('HTTP Error 403: Forbidden')
  result=source_qa.resolve_source({'id':'S','url':'https://primary.example/source'},opener)
  self.assertEqual(result['status'],'BLOCKED')
  self.assertFalse(result.get('fallback_used',False))
 def test_missing_production_can_never_be_candidate(self):
  result=gate.evaluate(self.run)
  self.assertEqual(result['status'],'BLOCKED')
  self.assertNotIn('review_url',result)
 def fixture(self):
  assets=[]
  for r in state.read(self.run/'visual_requirements.json')['output']['requirements']:
   if not r['required']:continue
   p=self.root/'public/assets'/f"{r['scene_id']}.png";p.parent.mkdir(parents=True,exist_ok=True)
   p.write_bytes(b'synthetic gate fixture, not an image')
   assets.append({'scene_id':r['scene_id'],'path':'/assets/'+p.name,'sha256':state.digest(p),'bytes':p.stat().st_size,
                  'provenance':'synthetic test','provider':'fixture','visual_qa':{'pass':True}})
  reader=self.root/'public/review/test/index.html';reader.parent.mkdir(parents=True)
  reader.write_text(' '.join(a['path'] for a in assets))
  hashes={'public/review/test/index.html':state.digest(reader)}
  state.write(self.run/'editorial-copy.json',{})
  shot=self.run/'screenshots/phone.png';shot.parent.mkdir();shot.write_bytes(b'synthetic screenshot')
  shots=[{'path':'screenshots/phone.png','sha256':state.digest(shot)}]
  common={**self.bind,'status':'PASS','reader_hashes':hashes,'deploy_id':'synthetic-deploy'}
  data={
   'production-receipt':{**common,'state':'ASSEMBLED','defects':[],'reader':'public/review/test/index.html'},
   'asset-persistence-receipt':{**common,'assets':assets},
   'editorial-qa':{**common,'copy_sha256':state.digest(self.run/'editorial-copy.json')},
   'deployment-receipt':{**common,'branch':'test/automated-edition-1','commit':'synthetic','deployment_result':'live','url':'https://review.example/review/test/','base_url':'https://review.example'},
   'source-qa':common,
   'rendered-qa':{**common,'url':'https://review.example/review/test/','observations':[{'device':'fixture'}],'screenshots':shots},
   'visual-review':{**common,'screenshots':shots},'benchmark-parity':{**common,'screenshots':shots}}
  for name,value in data.items():state.write(self.run/(name+'.json'),value)
 def evaluate(self):
  from urllib.parse import urlparse
  def local(url,timeout):return (self.root/'public'/urlparse(url).path.lstrip('/')).open('rb')
  with patch.object(state,'ROOT',self.root),patch.object(gate,'ROOT',self.root):return gate.evaluate(self.run,fetch=local)
 def test_complete_synthetic_receipts_then_tampered_asset(self):
  self.fixture()
  self.assertEqual(self.evaluate()['status'],'PUBLICATION_CANDIDATE')
  next((self.root/'public/assets').iterdir()).write_bytes(b'changed')
  self.assertEqual(self.evaluate()['status'],'BLOCKED')
 def test_stale_visual_pass_cannot_survive_new_deployment(self):
  self.fixture()
  self.change('visual-review.json',lambda x:x.update(deploy_id='old'))
  self.assertEqual(self.evaluate()['status'],'BLOCKED')
 def test_reader_change_invalidates_all_rendered_passes(self):
  self.fixture();(self.root/'public/review/test/index.html').write_text('changed')
  self.assertEqual(self.evaluate()['status'],'BLOCKED')
 def test_visual_pass_with_known_defect_is_blocked(self):
  self.fixture();self.change('visual-review.json',lambda x:x.update(defects=['bad crop']))
  self.assertEqual(self.evaluate()['status'],'BLOCKED')
 def test_missing_required_image_blocks_even_if_all_pass_labels_remain(self):
  self.fixture();self.change('asset-persistence-receipt.json',lambda x:x['assets'].pop())
  self.assertEqual(self.evaluate()['status'],'BLOCKED')
 def test_trace_operation_cannot_disappear(self):
  contract=state.read(state.ROOT/'atlas/contracts/manufacturing-trace.json')
  self.assertEqual(trace_validate(contract),[])
  contract['operations'].pop(0)
  self.assertTrue(trace_validate(contract))
 def test_reader_is_not_a_fixed_six_perspective_template(self):
  route={'perspective_id':'P1','perspective':'Synthetic first','scenes':[{'scene_id':'S1','meaning':'Synthetic meaning'}]}
  second={'perspective_id':'P2','perspective':'Synthetic second','scenes':[{'scene_id':'S2','meaning':'Synthetic other meaning'}]}
  block={'heading':'Synthetic publication heading','paragraphs':[{'text':'Synthetic prose','state':'FACT','evidence_refs':['WB-HEAT-2025']}]}
  copy={'opening':block,'place':block,'consequences':block,'scenes':{'S1':block,'S2':block}}
  assets=[{'scene_id':'S1','provider':'fixture','path':'/assets/test.png','truth_boundary':'Synthetic contextual visual'}]
  target=self.root/'public/review';target.mkdir(parents=True)
  for name in ('reader-production.css','reader-production.js'):shutil.copyfile(state.ROOT/'public/review'/name,target/name)
  with patch.object(builder,'ROOT',self.root):
   page=builder.build_reader(self.run,'SYNTHETIC',{'working_title':'Synthetic title','geographic_core':'Synthetic place','world_change':'Synthetic change'},[route,second],{'title':'Synthetic story','boundary':'Fiction, invented','story':['Synthetic story']},assets,copy)
  text=page.read_text()
  self.assertEqual(text.count('data-view class="route"'),2)
  self.assertIn('AI-generated contextual illustration',text)
  self.assertNotIn('PUBLICATION CANDIDATE',text)
  self.assertIn('reader.js',text)
 def test_path_escape_rejected(self):
  with self.assertRaises(ValueError):state.public_path('/../../outside')

if __name__=='__main__':unittest.main()
