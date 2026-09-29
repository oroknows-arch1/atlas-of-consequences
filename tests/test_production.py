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
 def test_visual_review_allows_labelled_contextual_ai_art_but_blocks_generic_failures(self):
  review=(state.ROOT/'tools/review_rendered.py').read_text()
  self.assertIn('Atlas permits clearly labelled AI-generated contextual illustrations',review)
  self.assertIn('block solely because an image is AI-generated',review)
 def test_css_repair_ignores_non_css_defects_in_mixed_review(self):
  repair=(state.ROOT/'tools/repair_reader.py').read_text()
  self.assertIn('[d for d in visual["defects"] if any(word in str(d).lower() for word in allowed)]',repair)
  self.assertIn('if not faults:',repair)
 def test_visual_review_retries_malformed_provider_output(self):
  review=(state.ROOT/'tools/review_rendered.py').read_text()
  self.assertIn('json.JSONDecodeError',review)
  self.assertIn('time.sleep(2)',review)
 def test_repair_router_maps_route_defects_and_runs_mixed_workers(self):
  loop=(state.ROOT/'tools/review_loop.py').read_text()
  self.assertIn('affected_scene_ids',loop)
  self.assertIn("owners & {'visual_factory','asset_persistence','editorial_factory','reader_builder'}",loop)
  self.assertIn("if 'reader_treatment' in owners",loop)
  import review_loop
  self.assertEqual(review_loop.affected_scene_ids([{'scene_id':'phone-route-H4–H6'}],['H1-S1','H4-S1','H6-S2']),{'H4-S1','H6-S2'})
 def test_publication_gate_retries_stale_deployed_bytes(self):
  gate=(state.ROOT/'tools/publication_gate.py').read_text()
  self.assertIn("Cache-Control':'no-cache'",gate)
  self.assertIn('atlas_verify',gate)
  self.assertIn('range(1,4)',gate)
 def test_deployment_worker_verifies_live_asset_hashes(self):
  deploy=(state.ROOT/'tools/deploy_review.py').read_text()
  self.assertIn('asset_integration_status',deploy)
  self.assertIn('deployed bytes differ',deploy)
  self.assertIn('Cache-Control',deploy)
  self.assertIn('receipt["reader_hashes"].items()',deploy)
 def test_production_workflow_resumes_from_branch_tip(self):
  workflow=(state.ROOT/'.github/workflows/atlas-edition-production.yml').read_text()
  self.assertIn('ref: test/automated-edition-1',workflow)
  self.assertIn('cancel-in-progress: true',workflow)
 def test_integration_workflow_stops_before_deployment_and_publication(self):
  workflow=(state.ROOT/'.github/workflows/atlas-edition-production.yml').read_text()
  self.assertIn('name: Store full-reader evidence for visual veto\n        if: always()',workflow)
  self.assertNotIn('produce_edition.py',workflow)
  self.assertIn('assemble_verified_reader.py',workflow)
  self.assertIn('full_render_gate.cjs',workflow)
  self.assertNotIn('deploy_review.py',workflow)
  self.assertNotIn('review_inherited_live.py',workflow)
  self.assertNotIn('publication_gate_inherited.py',workflow)
  self.assertNotIn('git push',workflow)
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
  self.assertIn('for i in range(0,len(candidate),4)',review)
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
  selected=state.read(self.run/'selected-edition-perspectives.json')
  selected['output']['perspectives'][-1]['primary_domain']='markets_finance'
  selected['output']['perspectives'][-1]['entry_label']='Finance and adaptation'
  state.write(self.run/'selected-edition-perspectives.json',selected)
  routes=state.read(self.run/'causal_boundary_gate.json')
  for scene,mechanism in zip(routes['output']['routes'][-1]['scenes'][1:],
                             ['capital_and_payback','allocation_and_uncertainty']):
   scene['domains']=['markets_finance'];scene['finance_mechanism']=mechanism
  state.write(self.run/'causal_boundary_gate.json',routes)
  self.bind=state.binding(self.run)
  assets=[]
  for r in state.read(self.run/'visual_requirements.json')['output']['requirements']:
   if not r['required']:continue
   p=self.root/'public/assets'/f"{r['scene_id']}.png";p.parent.mkdir(parents=True,exist_ok=True)
   p.write_bytes(b'synthetic gate fixture, not an image')
   assets.append({'scene_id':r['scene_id'],'path':'/assets/'+p.name,'sha256':state.digest(p),'bytes':p.stat().st_size,
                  'provenance':'synthetic test','provider':'fixture','visual_qa':{'pass':True}})
   from visual_coverage import beats_for
   editorial=state.read(state.ROOT/'content/AUTOMATED-TEST-001/editorial-copy.json')
   for i,(_,beat_text) in enumerate(beats_for(editorial['scenes'][r['scene_id']]),1):
    if i==1:continue
    beat=f"{r['scene_id']}-B{i}"
    extra=self.root/'public/assets'/f'{beat}.png';extra.write_bytes(b'synthetic independent beat')
    assets.append({'scene_id':r['scene_id'],'beat_id':beat,'path':'/assets/'+extra.name,
                   'beat_text_sha256':__import__('hashlib').sha256(beat_text.encode()).hexdigest(),
                   'sha256':state.digest(extra),'bytes':extra.stat().st_size,
                   'provenance':'synthetic test','provider':'fixture','visual_qa':{'pass':True}})
  reader=self.root/'public/review/test/index.html';reader.parent.mkdir(parents=True)
  reader.write_text(' '.join(a['path'] for a in assets))
  hashes={'public/review/test/index.html':state.digest(reader)}
  state.write(self.run/'editorial-copy.json',editorial)
  from visual_coverage import plan as visual_plan
  routes=state.read(self.run/'causal_boundary_gate.json')['output']['routes']
  specs=state.read(self.run/'visual_requirements.json')['output']['requirements']
  for gap in visual_plan(self.run,routes,specs,assets,editorial)['gaps']:
   beat=gap['beat_id'];p=self.root/'public/assets'/f'{beat}.png';p.write_bytes(b'synthetic missing-beat visual')
   assets.append({'scene_id':gap['scene'],'beat_id':beat,'path':'/assets/'+p.name,
                  'beat_text_sha256':__import__('hashlib').sha256(gap['intent']['beat_text'].encode()).hexdigest(),
                  'sha256':state.digest(p),'bytes':p.stat().st_size,'provenance':'synthetic test',
                  'provider':'fixture','visual_qa':{'pass':True}})
  reader.write_text(' '.join(a['path'] for a in assets))
  hashes={'public/review/test/index.html':state.digest(reader)}
  shot=self.run/'screenshots/phone.png';shot.parent.mkdir();shot.write_bytes(b'synthetic screenshot')
  shots=[{'path':'screenshots/phone.png','sha256':state.digest(shot)}]
  common={**self.bind,'status':'PASS','reader_hashes':hashes,'deploy_id':'synthetic-deploy'}
  grammar=self.root/'atlas/contracts/reader-grammar.json';grammar.parent.mkdir(parents=True);state.write(grammar,{'version':'atlas-reader-v2','opening_modes':['approved_film','verified_image_sequence'],'viewports':[1,2,3]})
  film=self.root/'public/assets/opening.mp4';film.write_bytes(b'synthetic motion fixture')
  state.write(self.run/'opening-media.json',{**self.bind,'status':'PASS','kind':'motion_video','path':'/assets/opening.mp4','sha256':state.digest(film),'visual_qa':{'status':'PASS'}})
  state.write(self.run/'opening-system.json',{**self.bind,'status':'PASS','mode':'verified_image_sequence','assets':[{'path':a['path'],'sha256':a['sha256']} for a in assets[:2]],'film':None})
  data={
   'production-receipt':{**common,'state':'ASSEMBLED','defects':[],'reader':'public/review/test/index.html'},
   'asset-persistence-receipt':{**common,'assets':assets},
   'editorial-qa':{**common,'copy_sha256':state.digest(self.run/'editorial-copy.json')},
   'deployment-receipt':{**common,'branch':'test/automated-edition-1','commit':'synthetic','deployment_result':'live','url':'https://review.example/review/test/','base_url':'https://review.example'},
   'source-qa':common,
   'rendered-qa':{**common,'url':'https://review.example/review/test/','observations':[{'device':'fixture'}],'screenshots':shots},
   'visual-review':{**common,'screenshots':shots},'benchmark-parity':{**common,'screenshots':shots,'contract_version':'atlas-reader-v2','contract_status':'PASS'},'reader-contract-qa':{**common,'version':'atlas-reader-v2','screenshots':shots,'measurements':[{'synthetic':True}],'motion':[{'mode':'verified_image_sequence','skip':True,'natural':True} for _ in range(3)],'canonical':[{'synthetic':True}]}}
  for name,value in data.items():state.write(self.run/(name+'.json'),value)
 def evaluate(self):
  from urllib.parse import urlparse
  def local(url,timeout):
   if hasattr(url,'full_url'): url=url.full_url
   return (self.root/'public'/urlparse(url).path.lstrip('/')).open('rb')
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
  source=state.ROOT/'public/assets/aet1-wc-002/h1-s1.png'
  source2=state.ROOT/'public/assets/aet1-wc-002/h2-s1.png'
  assets=[{'scene_id':'S1','provider':'fixture','path':'/assets/aet1-wc-002/h1-s1.png','sha256':state.digest(source),'truth_boundary':'Synthetic contextual visual','visual_qa':{'pass':True}}, {'scene_id':'S2','provider':'fixture','path':'/assets/aet1-wc-002/h2-s1.png','sha256':state.digest(source2),'truth_boundary':'Another contextual visual','visual_qa':{'pass':True}}]
  graphic=state.ROOT/'public/assets/aet1-wc-002/h1-s2.svg'
  assets.append({'scene_id':'S1','beat_id':'S1-B1','provider':'ATLAS_DETERMINISTIC_GRAPHIC','path':'/assets/aet1-wc-002/h1-s2.svg','sha256':state.digest(graphic),'truth_boundary':'Synthetic explanatory chart','visual_qa':{'pass':True}})
  state.write(self.run/'visual_requirements.json',{'output':{'requirements':[
   {'scene_id':'S1','required':True,'purpose':'Synthetic scene','truth_boundary':'No claim','visual_type':'editorial contextual still'},
   {'scene_id':'S2','required':True,'purpose':'Synthetic other scene','truth_boundary':'No claim','visual_type':'editorial contextual still'}]}})
  target=self.root/'public/review';target.mkdir(parents=True)
  for name in ('adaptive.js','edition.css'):shutil.copyfile(state.ROOT/'public/review'/name,target/name)
  with patch.object(builder,'ROOT',self.root), patch('market_finance.validate',return_value={'status':'PASS'}):
   page=builder.build_reader(self.run,'SYNTHETIC',{'working_title':'Synthetic title','geographic_core':'Synthetic place','world_change':'Synthetic change'},[route,second],{'title':'Synthetic story','boundary':'Fiction, invented','story':['Synthetic story']},assets,copy,structural=True)
  text=page.read_text()
  self.assertEqual(text.count('data-perspective="P'),2)
  self.assertIn('class="menu visual-perspective-menu"',text)
  self.assertEqual(text.count('class="perspective-hotspot"'),2)
  self.assertEqual(text.count('class="edition-menu-art"'),1)
  self.assertNotIn('perspective-row',text)
  self.assertEqual(text.count('class="edition-menu-slice"'),2)
  self.assertEqual(text.count('<h2>Synthetic publication heading</h2>'),5)
  self.assertNotIn('text-scene',text)
  self.assertIn('id="route-P1" class="route perspective-route" data-route="P1"',text)
  self.assertIn('id="route-P2" class="route perspective-route" data-route="P2"',text)
  self.assertIn('AI-generated contextual illustration',text)
  self.assertIn('data-graphic-path="/assets/aet1-wc-002/h1-s2.svg"',text)
  self.assertNotIn('<img src="/assets/aet1-wc-002/h1-s2.svg"',text)
  self.assertIn('Preview the evidence',text)
  self.assertIn('href="#source-WB-HEAT-2025"',text)
  self.assertNotIn('PUBLICATION CANDIDATE',text)
  self.assertIn('adaptive.js',text)
  self.assertEqual(state.digest(page.parent/'adaptive.css'),state.digest(state.ROOT/'public/adaptive/adaptive.css'))
  canonical=(state.ROOT/'public/adaptive/index.html').read_text()
  inherited=(page.parent/'adaptive.js').read_text()
  start="  const routes = [...document.querySelectorAll('.perspective-route')];"
  end='\n\n  const hero ='
  controller=lambda source:source[source.index(start):source.index(end,source.index(start))]
  self.assertEqual(controller(inherited),controller(canonical))
 def test_path_escape_rejected(self):
  with self.assertRaises(ValueError):state.public_path('/../../outside')

if __name__=='__main__':unittest.main()
